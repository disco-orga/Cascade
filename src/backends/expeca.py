import time
import shlex
import shutil
import tempfile
from pathlib import Path
from dataclasses import dataclass

from services.netshoot import Netshoot
from backends.backend import Backend
import chi.expeca
import chi.network
import chi.container


DEBUG = True
HOSTS_PATH = "/etc/hosts"


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
    def __init__(self, network_name="disco-net", config_dns=False):
        self.network_name = network_name
        self.nodes = {}
        self.allocated_nodes = []
        self.leases = []
        self.network = None
        self.hosts = {}
        self.orchestrator = None
        self.config_dns = config_dns

    def format_name(self, name):
        return name.replace("_", "")

    def check(self, result, operation):
        if result["exit_code"] != 0:
            debug("Command failed", operation=operation, result=result)
            raise RuntimeError(f"{operation} failed:\n{result['output']}")
        return result

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
        if not self.nodes:
            raise RuntimeError("Cannot start orchestrator if no nodes are available.")
        debug("Starting orchestrator")
        self.orchestrator = self.deploy(
            Netshoot(name="cascade_orchestrator"),
            next(iter(self.nodes.values()))["reserved"],
            register_host=False,
        )
        debug("Orchestrator ready", uuid=self.orchestrator.uuid)

    def wait_for(self, host, port, timeout):
        if self.orchestrator is None:
            self.start_orchestrator()

        self.upload_hosts(self.orchestrator)
        resolved_host = self.hosts.get(self.format_name(host), host)
        debug("Waiting for service", host=host, resolved_host=resolved_host, port=port, timeout=timeout)
        deadline = time.monotonic() + timeout
        attempt = 0

        while time.monotonic() < deadline:
            attempt += 1
            result = chi.container.execute(
                self.orchestrator.uuid,
                f"nc -zw1 {shlex.quote(str(resolved_host))} {int(port)}",
            )
            if result["exit_code"] == 0:
                debug("Service reachable", host=host, resolved_host=resolved_host, port=port, attempts=attempt)
                return
            debug("Connection attempt failed", attempt=attempt, host=resolved_host, port=port,
                  exit_code=result["exit_code"], output=result.get("output"))
            time.sleep(0.2)

        raise RuntimeError(f"Timeout waiting for {host} ({resolved_host}):{port}")

    def get_ready_path(self):
        return "/disco_ready"

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

    def upload_hosts(self, container):
        debug("Preparing hosts file", container=container.name, destination=HOSTS_PATH)
        current = chi.container.execute(container.uuid, f"cat {shlex.quote(HOSTS_PATH)}")
        if current["exit_code"] == 0:
            hosts = current["output"].rstrip("\n") + "\n"
        else:
            debug("Hosts destination absent or unreadable; starting fresh", output=current.get("output"))
            hosts = ""
        hosts += self.build_hosts_file()
        debug("Hosts content prepared", content=hosts)

        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as f:
            f.write(hosts)
            f.flush()
            self.upload(container, f.name, HOSTS_PATH)

    def upload_ready_file(self, container):
        path = self.get_ready_path()
        debug("Uploading readiness marker", container=container.name, destination=path)
        with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8") as f:
            f.write("ready")
            f.flush()
            self.upload(container, f.name, path)

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
        print("WARN: Uploading a file on EXPECA is not stable yet.")

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

        ready_path = self.get_ready_path()
        command = None
        if component.command is None and component.mounting:
            raise RuntimeError("If you want to mount a file, you need to declare the command explicitly.")
        elif component.command is not None:
            command = [
                "sh", "-c",
                f"""while [ ! -f {shlex.quote(ready_path)} ]; do
    sleep 0.2
done
{" ".join(shlex.quote(arg) for arg in component.command)}
sleep infinity
""",
            ]

        kwargs = {
            "name": name,
            "image": component.image,
            "reservation_id": reservation_id,
            "command": command,
        }
        print(f"Deploying {component.name} on {reservation_id}")
        debug("Creating container", name=name, command=command)
        try:
            container = chi.container.create_container(**kwargs)
            debug("Container creation returned", name=name, uuid=container.uuid)
            chi.container.wait_for_active(container.uuid)
            debug("Container became ACTIVE", name=name, uuid=container.uuid)
        except Exception as e:
            debug("Container deployment failed", name=name, error=repr(e))
            raise RuntimeError(f"Failed to deploy '{component.name}' on '{node.worker_name}'.") from e

        if register_host:
            self.register_host(container)

        self.upload_hosts(container)
        for src, dst in component.mounting.items():
            self.upload(container, src, dst)
        self.upload_ready_file(container)
        debug("Deployment finished", name=name, uuid=container.uuid)
        return container
