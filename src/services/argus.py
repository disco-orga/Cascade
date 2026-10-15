from component import Component

class Argus(Component):

    def __init__(
        self,
        name="argus",
        broker="mosquitto",
        broker_port=1883,
        prom_host="prometheus",
        prom_port=9090,
        **kwargs,
    ):
        command = [
            "./argus",
            "--name", str(name),
            "--broker-port", str(broker_port),
            "--broker-host", broker,
            "--prom-host", prom_host,
            "--prom-port", str(prom_port),
        ]

        args = {
            "image": "ghcr.io/zivomartin/argus:latest",
            "local_image": "argus:latest",
            "name": name,
            "stdout": False,
            "stderr": False,
            "command": command,
        }

        args.update(kwargs)

        super().__init__(**args)
