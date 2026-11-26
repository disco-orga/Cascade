import time
import shlex
import shutil
import yaml
import tempfile
import threading

from pathlib import Path
from dataclasses import dataclass

from services.netshoot import Netshoot
from backends.backend import Backend
import chi.expeca
import chi.network
import chi.container


DEBUG = True
HOSTS_PATH = "/etc/hosts"
WRAPPER_IMAGE = "samiemostafavi/sshd-dind-oai"
COMPOSE_FILE = "/tmp/compose.yaml"

def debug(message, **details):
    """Print diagnostic information only when DEBUG is enabled."""
    if not DEBUG:
        return
    timestamp = time.strftime("%H:%M:%S")
    suffix = " ".join(f"{key}={value!r}" for key, value in details.items())
    print(f"[EXPECA DEBUG {timestamp}] {message}" + (f" | {suffix}" if suffix else ""), flush=True)


@dataclass(frozen=True)
class ExpecaNode:
    worker_name: str
    days: int = 0
    hours: int = 1


@dataclass
class ExpecaNodeAllocated:
    reservation_id: str


class ExpecaBackend(Backend):
    def __init__(self, network_name="disco-net"):
        self.network_name = network_name
        self.nodes = {}
        self.allocated_nodes = []
        self.leases = []
        self.network = None
        self.hosts = {}
        self.orchestrator = None
        self.orchestrator_lock = threading.Lock()

    def format_name(self, name):
        return name.replace("_", "")

    def check(self, result, operation):
        if result["exit_code"] != 0:
            debug("Command failed", operation=operation, result=result)
            raise RuntimeError(f"{operation} failed:\n{result['output']}")
        return result

    def resolve_name(self, name):
        name = self.format_name(name)

        try:
            return self.hosts[name]
        except KeyError:
            raise RuntimeError(
                f"Cannot resolve '{name}': container has not been registered."
            )

    def setup_network(self):
        debug("Looking up network", name=self.network_name)
        for network in chi.network.list_networks():
            if network["name"] == self.network_name:
                self.network = network
                debug("Using existing network", network_id=network["id"])
                return
        self.network = chi.network.create_network(self.network_name)
        chi.network.create_subnet("disco-subnet", self.network["id"])
        debug("Created network and subnet", network_id=self.network["id"])

    def start_orchestrator(self):
        with self.orchestrator_lock:
            if self.orchestrator is not None:
                return

            if not self.nodes:
                raise RuntimeError("No nodes available")

            self.orchestrator = self.deploy(
                Netshoot(name="cascade_orchestrator"),
                next(iter(self.nodes.values()))["reserved"],
                register_host=False,
            )

    def wait_for(self, host, port, timeout):
        if self.orchestrator is None:
            self.start_orchestrator()

        resolved_host = self.resolve_name(host)

        debug(
            "Waiting for service",
            host=host,
            resolved_host=resolved_host,
            port=port,
            timeout=timeout,
        )

        deadline = time.monotonic() + timeout
        attempt = 0

        while time.monotonic() < deadline:
            attempt += 1

            command = (
                "docker exec cascadeorchestrator "
                f"nc -z -w 2 {shlex.quote(str(resolved_host))} {int(port)}"
            )

            result = chi.container.execute(
                self.orchestrator.uuid,
                command,
            )

            if result["exit_code"] == 0:
                debug(
                    "Service reachable",
                    host=host,
                    resolved_host=resolved_host,
                    port=port,
                    attempts=attempt,
                )
                return

            debug(
                "Connection attempt failed",
                attempt=attempt,
                host=resolved_host,
                port=port,
                exit_code=result["exit_code"],
                output=result.get("output"),
            )

            time.sleep(0.2)

        raise RuntimeError(
            f"Timeout waiting for {host} ({resolved_host}):{port}"
        )

    def build_hosts_file(self):
        return "\n".join(f"{ip} {name}" for name, ip in self.hosts.items()) + "\n"

    def add_host(self, name, ip):
        self.hosts[name] = ip
        debug("Registered host", name=name, ip=ip)

    def setup(self):
        def reserve(node):
            debug("Requesting reservation", worker=node.worker_name, days=node.days, hours=node.hours)
            return chi.expeca.reserve({
                "type": "device",
                "name": node.worker_name,
                "duration": {"days": node.days, "hours": node.hours},
            })

        self.leases.clear()
        for entry in self.nodes.values():
            node = entry["reserved"]
            lease_name = f"{node.worker_name}-lease"
            lease = chi.expeca.show_reservation_byname(lease_name)
            debug("Checked lease", name=lease_name, status=lease.get("status") if lease else "missing")

            if lease is None:
                lease = reserve(node)
            elif lease["status"] == "TERMINATED":
                answer = input(
                    f"The lease '{lease_name}' has been terminated.\n"
                    "Remove it and reserve a new one? [Y/n] "
                ).strip().lower()
                if answer in ("", "y", "yes"):
                    chi.expeca.remove_lease(lease["id"], lease["name"])
                    lease = reserve(node)
                else:
                    raise RuntimeError(f"Cannot continue: lease '{lease_name}' is terminated.")

            if not lease.get("reservations"):
                raise RuntimeError(f"Lease '{lease_name}' contains no reservations.")

            reservation_id = lease["reservations"][0]["id"]
            self.leases.append(lease)
            self.nodes[node.worker_name]["allocated"] = ExpecaNodeAllocated(reservation_id)
            debug("Reservation allocated", worker=node.worker_name, reservation_id=reservation_id)

        # Network setup remains disabled, as in the original implementation.
        # self.setup_network()

    def reserve_node(self, node):
        self.nodes[node.worker_name] = {"allocated": None, "reserved": node}
        debug("Added node", worker=node.worker_name)

    def allocated(self, node):
        return self.nodes[node]["allocated"]


    def delete_and_wait(self, container):
        debug("Deleting container", name=container.name, uuid=container.uuid)
        chi.clients.zun().containers.delete(container.uuid, force=True)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            containers = {c.name: c for c in chi.container.list_containers()}
            if container.name not in containers:
                debug("Container deleted", name=container.name)
                return
            time.sleep(0.5)
        raise RuntimeError(f"Timed out waiting for '{container.name}' to be deleted.")

    def register_host(self, container):
        debug("Waiting for container IP", name=container.name, uuid=container.uuid)
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            container = chi.container.get_container(container.uuid)
            if container is not None and container.addresses:
                break
            time.sleep(0.5)
        else:
            raise RuntimeError(f"Container '{container.name}' has no assigned IP address after 30 seconds.")

        network_id = next(iter(container.addresses))
        ip = container.addresses[network_id][0]["addr"]
        self.add_host(container.name, ip)

    def upload(self, container, src, dst):
        src = Path(src)
        dst = Path(dst)

        with tempfile.TemporaryDirectory() as local_dir:
            temp_file = Path(local_dir) / dst.name
            shutil.copy2(src, temp_file)

            debug(
                "Starting upload",
                container=container.name,
                source=str(src),
                destination=str(dst),
            )

            response = chi.container.upload(
                container.uuid,
                local_dir,
                str(dst.parent),
            )

            debug("Upload response", response=str(response))

            result = chi.container.execute(
                container.uuid,
                f"test -f {shlex.quote(str(dst))}"
            )

            if result["exit_code"] != 0:
                raise RuntimeError(
                    f"Upload failed: {dst} was not created in {container.name}"
                )

    def insert_hosts_ip_in_env(self, env):
        """Insert each registered host's IP as an environment variable NAME_IP."""
        env = dict(env or {})

        for name, ip in self.hosts.items():
            env[f"{name.upper()}_IP"] = str(ip)

        return env

    def wait_for_docker(self, wrapper):
        debug(
            "Waiting for Docker daemon",
            wrapper=wrapper.name,
            uuid=wrapper.uuid,
        )

        for attempt in range(1, 31):
            debug(
                "Checking Docker daemon",
                wrapper=wrapper.name,
                attempt=attempt,
            )

            try:
                result = chi.container.execute(
                    wrapper.uuid,
                    "docker info",
                )
            except Exception as e:
                debug(
                    "Execution failed",
                    wrapper=wrapper.name,
                    uuid=wrapper.uuid,
                    attempt=attempt,
                    error_type=type(e).__name__,
                    error=str(e),
                )

                try:
                    container = chi.container.get_container(wrapper.uuid)
                    debug(
                        "Wrapper status after execution failure",
                        wrapper=wrapper.name,
                        status=container.status,
                        status_reason=getattr(container, "status_reason", None),
                    )
                except Exception as status_error:
                    debug(
                        "Failed to retrieve wrapper status",
                        wrapper=wrapper.name,
                        error=str(status_error),
                    )

                time.sleep(1)
                continue

            debug(
                "Docker info returned",
                wrapper=wrapper.name,
                attempt=attempt,
                exit_code=result.get("exit_code"),
            )

            if result.get("exit_code") == 0:
                debug(
                    "Docker daemon ready",
                    wrapper=wrapper.name,
                    attempts=attempt,
                )
                return

            debug(
                "Docker daemon not ready",
                wrapper=wrapper.name,
                attempt=attempt,
            )

            time.sleep(1)

        debug(
            "Docker daemon readiness timeout",
            wrapper=wrapper.name,
            uuid=wrapper.uuid,
        )

        raise RuntimeError(
            f"Docker daemon failed to become ready in '{wrapper.name}'"
        )

    def launch_compose(self, component, wrapper):
        while True:
            result = chi.container.execute(
                wrapper.uuid,
                f"docker pull {shlex.quote(component.image)}",
            )

            if result["exit_code"] == 0:
                break

            if result["exit_code"] is not None:
                raise RuntimeError(result["output"])

            time.sleep(2)

        result = chi.container.execute(
            wrapper.uuid,
            f"docker compose -f {shlex.quote(COMPOSE_FILE)} -p disco up -d",
        )
        return self.check(result, "Launch nested container")

    def launch_container(self, component, wrapper):
        name = self.format_name(component.name)

        debug(
            "Preparing nested container deployment",
            component=component.name,
            wrapper=wrapper.name,
            image=component.image,
        )

        config = {
            "services": {
                "app": {
                    "image": component.image,
                    "container_name": name,
                    "environment": self.insert_hosts_ip_in_env(component.env),
                    "volumes": [
                        f"{dst}:{dst}"
                        for dst in component.mounting.values()
                    ],
                }
            }
        }

        service = config["services"]["app"]

        if component.entrypoint is not None:
            service["entrypoint"] = component.entrypoint

        if component.command is not None:
            service["command"] = component.command

        hosts = dict(self.hosts)

        if self.hosts:
            service["extra_hosts"] = {
                name: str(ip)
                for name, ip in self.hosts.items()
            }

        if component.ports:
            service["ports"] = [
                f"{host}:{container}"
                for host, container in component.ports.items()
            ]

        debug(
            "Compose configuration generated",
            component=component.name,
            image=component.image,
            ports=component.ports,
            mounts=component.mounting,
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "compose.yaml"

            with path.open("w") as f:
                yaml.safe_dump(config, f)

            debug(
                "Uploading Compose configuration",
                wrapper=wrapper.name,
                destination=COMPOSE_FILE,
            )

            self.upload(wrapper, path, COMPOSE_FILE)

        debug("Starting nested container", name=name, wrapper=wrapper.name)

        result = self.launch_compose(component, wrapper)

        debug(
            "Compose deployment completed",
            name=name,
            output=result.get("output"),
        )

        debug("Verifying nested container state", name=name)

        result = chi.container.execute(
            wrapper.uuid,
            f"docker inspect -f '{{{{.State.Running}}}}' {shlex.quote(name)}",
        )
        self.check(result, "Inspect nested container")

        if result["output"].strip() != "true":
            debug(
                "Nested container is not running",
                name=name,
                state=result["output"].strip(),
            )
            raise RuntimeError(f"Container '{name}' is not running")

        debug(
            "Nested container deployment successful",
            name=name,
            wrapper=wrapper.name,
        )

    def setup_wrapper_network(self, wrapper):
        debug("Configuring wrapper network", wrapper=wrapper.name)

        result = chi.container.execute(
            wrapper.uuid,
            "ip route replace default via 169.254.1.1 dev eth0",
        )

        self.check(result, "Configure wrapper default route")

        debug("Wrapper network configured", wrapper=wrapper.name)

    def create_wrapper_with_retry(self, kwargs, attempts=3):
        for attempt in range(attempts):
            try:
                wrapper = chi.container.create_container(**kwargs)
                chi.container.wait_for_active(wrapper.uuid)
                return wrapper

            except Exception as e:
                debug(
                    "Wrapper creation failed",
                    attempt=attempt + 1,
                    error=repr(e),
                )

                if attempt == attempts - 1:
                    raise

                time.sleep(min(2 ** attempt, 10))


    def deploy(self, component, node, register_host=True):
        reservation_id = self.allocated(node.worker_name).reservation_id
        name = self.format_name(component.name)

        debug("Preparing deployment", component=component.name, name=name,
              image=component.image, worker=node.worker_name, reservation_id=reservation_id)

        containers = {c.name: c for c in chi.container.list_containers()}

        existing = containers.get(name)

        if existing is not None and component.redeploy:
            debug("Redeployment requested", name=name)
            self.delete_and_wait(existing)
        elif existing is not None:
            debug("Reusing existing container", name=name, uuid=existing.uuid)
            if not existing.addresses:
                raise RuntimeError(f"Container '{existing.name}' has no assigned IP address.")

            self.add_host(existing.name, next(iter(existing.addresses.values()))[0]["addr"])
            return existing


        kwargs = {
            "name": name,
            "image": WRAPPER_IMAGE,
            "reservation_id": reservation_id,
            "start": True,
            "start_timeout": 300,
            "environment": {
                "DNS_IP": "8.8.8.8",
            },
            "labels": {
                "capabilities.privileged": "true",
            },
        }

        if component.ports:
            kwargs["exposed_ports"] = component.ports

        print(f"Deploying {component.name} on {reservation_id}")

        debug("Creating wrapper", name=name)

        try:
            wrapper = self.create_wrapper_with_retry(kwargs)
            debug("Wrapper creation returned", name=name, uuid=wrapper.uuid)
            
            chi.container.wait_for_active(wrapper.uuid)
            debug("Wrapper became ACTIVE", name=name, uuid=wrapper.uuid)

            self.wait_for_docker(wrapper)
            debug("Wrapper's docker daemon is ready", name=name, uuid=wrapper.uuid)

            self.setup_wrapper_network(wrapper)
            debug("Wrapper's network is setup", name=name, uuid=wrapper.uuid)
            
        except Exception as e:
            debug("Container deployment failed", name=name, error=repr(e))
            raise RuntimeError(f"Failed to deploy '{component.name}' on '{node.worker_name}'.") from e

        if register_host:
            self.register_host(wrapper)

        for src, dst in component.mounting.items():
            self.upload(wrapper, src, dst)

        self.launch_container(component, wrapper)

        return wrapper

    
