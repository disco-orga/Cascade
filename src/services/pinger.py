from component import Component


class Pinger(Component):

    def __init__(self, target, count=5, name="pinger", **kwargs):
        command = [
            "sh",
            "-c",
            f"which ping && ping -c {count} {target}",
        ]

        args = {
            "image": "nicolaka/netshoot:latest",
            "name": name,
            "stdout": True,
            "stderr": True,
            "command": command,
        }
        args.update(kwargs)

        super().__init__(**args)
