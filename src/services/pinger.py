from component import Component

class Pinger(Component):

    def __init__(self, target, count=5, name="pinger"):

        command = ["sh", "-c", f"which ping && ping -c 5 {target}"]
        super().__init__(
            image="nicolaka/netshoot:latest",
            name=name,
            stderr=True,
            stdout=True,
            command=command,
        )
