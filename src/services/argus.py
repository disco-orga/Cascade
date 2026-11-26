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
            "--prom-port", str(prom_port),
        ]

        if broker is not None:
            command.extend(["--broker-host", str(broker)])

        if prom_host is not None:
            command.extend(["--prom-host", str(prom_host)])


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
