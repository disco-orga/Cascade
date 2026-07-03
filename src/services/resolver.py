from component import Component


class Resolver(Component):

    def __init__(
        self,
        name="resolver",
        broker="mosquitto",
        broker_port=1883,
        channel_cap=10,
        **kwargs,
    ):
        command = [
            "./resolver",
            "--name", str(name),
            "--broker-port", str(broker_port),
            "--channel-cap", str(channel_cap),
            "--broker", broker,
        ]

        args = {
            "image": "ghcr.io/zivomartin/resolver:latest",
            "name": name,
            "stdout": False,
            "stderr": False,
            "command": command,
        }
        args.update(kwargs)

        super().__init__(**args)
