from pathlib import Path
import tempfile

from component import Component
from steps import WaitFor, Deploy, Workflow

class Mosquitto(Component):
    def __init__(
        self,
        name="mosquitto",
        port=1883,
        host=None,
        timeout=10,
        config_path=None,
        redeploy=False,
        **kwargs,
    ):
        args = {
            "image": "eclipse-mosquitto:latest",
            "name": name,
            "stdout": False,
            "stderr": False,
            "redeploy": redeploy,
            "command": [
                "mosquitto",
                "-c",
                "/mosquitto/config/mosquitto.conf",
            ],
        }

        args.update(kwargs)
        super().__init__(**args)

        self.host = host or name
        self.port = port
        self.timeout = timeout

        if config_path is not None:
            self.mount(
                config_path,
                "/mosquitto/config/mosquitto.conf",
            )

    def deployment_workflow(self, node):
        return Workflow([
            Deploy(self, node),
            WaitFor(self.port, self.host, self.timeout),
        ])
