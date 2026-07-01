
from dataclasses import dataclass

from backends.backend import Backend
import chi.expeca
import chi.network
import chi.container
import shlex


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

    def get_or_create_network(self, name):
        for network in chi.network.list_networks():
            if network["name"] == name:
                return network

        return chi.network.create_network(name)

    def get_ready_path(self):
        return "/var/run/disco/ready", "/var/run/disco"

    def setup(self):
        self.leases.clear()

        for node in self.nodes.values():
            node = node["reserved"]
                
            lease_name = f"{node.worker_name}-lease"
            lease = chi.expeca.show_reservation_byname(lease_name)
            if lease is None:
                lease = chi.expeca.reserve({
                    "type": "device",
                    "name": node.worker_name,
                    "duration": {
                        "days": node.days,
                        "hours": node.hours,
                    }
                })

            reservation_id = lease["reservations"][0]["id"]

            self.leases.append(lease)
            self.nodes[node.worker_name]["allocated"] = ExpecaNodeAllocated(reservation_id=reservation_id)
        self.network = self.get_or_create_network("disco-net")

    
    def network_id(self):
        if self.network is None:
            raise RuntimeError("Cannot fetch network id if the network has not been initialized.")
        else:
            return self.network["id"]

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
            
            if c.status == "Creating":
                chi.clients.zun().containers.delete(
                    c.uuid,
                    force=True,
                )
                
                return
            else:
                chi.container.destroy_container(component.name)
        elif c is not None:
            return
        
        print(f"Deploying {component.name} on {reservation_id}")

        ready_path, ready_folder = self.get_ready_path()

        command = [
            "sh",
            "-c",
            f"""
while [ ! -f {ready_path} ]; do
    echo 1
    sleep 0.2
done
echo 2
exec {" ".join(shlex.quote(arg) for arg in component.command)}
""",
        ]

        kwargs = {
            "name": component.name,
            "image": component.image,
            "reservation_id": reservation_id,
            "command": command,
            "nets": [{"network": self.network_id()}],
        }

        # if component.command:
        #     kwargs["command"] = component.command

        # if component.ports:
        #     kwargs["exposed_ports"] = list(component.ports.keys())

        container = chi.container.create_container(**kwargs)
        for src, dst in component.mounting.items():
            chi.container.upload(
                component.name,
                src,
                dst,
            )

        print(chi.clients.zun().containers.execute(
            container.uuid,
            command=f"""sh -c 'mkdir -p {ready_folder} && echo ready > {ready_path}'"""
        ))
