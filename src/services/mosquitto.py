from component import Component
from steps import WaitFor, Deploy


class Mosquitto(Component):
    def __init__(
        self,
        name="mosquitto",
        host=None,
        port=1883,
        timeout=10,
        **kwargs,
    ):
        args = {
            "image": "eclipse-mosquitto",
            "name": name,
            "stdout": False,
            "stderr": False,
            "redeploy": False,
        }
        args.update(kwargs)

        super().__init__(**args)

        self.host = host or self.name
        self.port = port
        self.timeout = timeout

    def deployment_plan(self, node):
        return [Deploy(self, node), WaitFor(self.port, self.host, self.timeout)]
