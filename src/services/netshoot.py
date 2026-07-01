from component import Component

class Netshoot(Component):

    def __init__(self, name="netshoot"):
        super().__init__(
            image="nicolaka/netshoot:latest",
            name=name,
            stdout=True,
            stderr=True,
            command=["sleep", "infinity"],
        )
