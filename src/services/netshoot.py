from component import Component


class Netshoot(Component):

    def __init__(self, name="netshoot", **kwargs):
        args = {
            "image": "nicolaka/netshoot:latest",
            "name": name,
            "stdout": True,
            "stderr": True,
            "command": ["sleep", "infinity"],
        }
        args.update(kwargs)

        super().__init__(**args)
