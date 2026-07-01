from component import Component

class Resolver(Component):

    def __init__(self, name="resolver", broker="mosquitto", broker_port=1883, channel_cap=10):
        command = [
            "./resolver",
            "--name", str(name),
            "--broker-port", str(broker_port),
            "--channel-cap", str(channel_cap),
            "--broker", "192.168.68.221"
        ]

        super().__init__(
            image="ghcr.io/zivomartin/resolver:latest",
            name = name,
            stderr = False,
            stdout = False,
            command = command
        )
