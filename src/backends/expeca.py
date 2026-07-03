import time
import tempfile
import shlex

from dataclasses import dataclass

from backends.backend import Backend
import chi.expeca
import chi.network
import chi.container


@dataclass
class ExpecaNode:
    worker_name: str
    days: int
    hours: int

    def __init__(self, worker_name, days=0, hours=1):
        self.worker_name = worker_name
        self.days = days
        self.hours = hours

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

    def setup_network(self):
        net_name = "disco_net"
        
        for network in chi.network.list_networks():
            if network["name"] == net_name:
                self.network = network

        self.network = chi.network.create_network(net_name)
        chi.network.create_subnet("disco-subnet", self.network["id"])

    def get_ready_path(self):
        return "/disco_ready"

    def build_hosts_file(self):
        return "\n".join(f"{ip} {name}" for name, ip in self.hosts.items()) + "\n"

    def add_host(self, name, ip):
        self.hosts[name] = ip

    def setup(self):
        def reserve(node):
            chi.expeca.reserve({
                "type": "device",
                "name": node.worker_name,
                "duration": {
                    "days": node.days,
                    "hours": node.hours,
                }
            })

        self.leases.clear()

        for node in self.nodes.values():
            node = node["reserved"]
                
            lease_name = f"{node.worker_name}-lease"
            lease = chi.expeca.show_reservation_byname(lease_name)
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
                    raise RuntimeError(
                        f"Cannot continue: lease '{lease_name}' is terminated."
                    )                

            reservation_id = lease["reservations"][0]["id"]

            self.leases.append(lease)
            self.nodes[node.worker_name]["allocated"] = ExpecaNodeAllocated(reservation_id=reservation_id)

        # self.setup_network()
    
    
    def reserve_node(self, node):
        self.nodes[node.worker_name] = {
            "allocated": None,
            "reserved": node
        }

    def allocated(self, node):
        return self.nodes[node]["allocated"]

    def deploy(self, component, node):
        reservation_id = self.allocated(node.worker_name).reservation_id
        containers = {c.name: c for c in chi.container.list_containers()}
        
        c = containers.get(component.name) 

        if c is not None and component.redeploy:            
            chi.clients.zun().containers.delete(c.uuid, force=True)
        elif c is not None:
            self.add_host(c.name, next(iter(c.addresses.values()))[0]["addr"])
            return

        print(f"Deploying {component.name} on {reservation_id}")

        ready_path = self.get_ready_path()
        
        command = None

        if component.command is None and component.mounting != {}:
            raise RuntimeError("If you want to mount a file, you need to declare the command explicitly.")
        elif component.command is not None:
            command = [
                "sh",
                "-c",
                f"""
while [ ! -f {ready_path} ]; do
    sleep 0.2
done
{" ".join(shlex.quote(arg) for arg in component.command)}
sleep infinity
""",
            ]

        kwargs = {
            "name": component.name,
            "image": component.image,
            "reservation_id": reservation_id,
            "command": command
        }

        container = chi.container.create_container(**kwargs)
        network_id = next(iter(container.addresses))
        self.add_host(container.name, container.addresses[network_id][0]["addr"])


        hosts = chi.container.execute(
            container.uuid,
            command="cat /etc/hosts"
        )["output"]

        hosts += "\n"
        hosts += self.build_hosts_file()

        cmd = (
            "sh -c "
            + shlex.quote(f"printf %s {shlex.quote(hosts)} > /etc/hosts")
        )        
        chi.container.execute(component.name, cmd)
        
        for src, dst in component.mounting.items():
            chi.container.upload(
                component.name,
                src,
                dst,
            )

        chi.container.execute(container.uuid, command=f"touch {ready_path}")
