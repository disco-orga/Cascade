from component import Component

class Kairos(Component):
    def __init__(self, name="kairos", broker="mosquitto", broker_port=1883, queue_capacity=100):
        command = [
            "./kairos",
            "--name", str(name),
            "--broker-port", str(broker_port),
            "--queue-capacity", str(queue_capacity),
            "--broker", broker,
        ]

        super().__init__(
            image = "kairos",
            name = name,
            stderr = False,
            stdout = False,
            command = command
        )
