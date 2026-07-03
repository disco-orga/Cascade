from component import Component


class Kairos(Component):

    def __init__(
        self,
        name="kairos",
        broker="mosquitto",
        broker_port=1883,
        queue_capacity=100,
        **kwargs,
    ):
        command = [
            "./kairos",
            "--name", str(name),
            "--broker-port", str(broker_port),
            "--queue-capacity", str(queue_capacity),
            "--broker", broker,
        ]

        args = {
            "image": "kairos",
            "name": name,
            "stdout": False,
            "stderr": False,
            "command": command,
        }
        args.update(kwargs)

        super().__init__(**args)
