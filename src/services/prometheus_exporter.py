from component import Component
from steps import WaitFor, Deploy, Workflow
from services.prometheus import PrometheusTarget

DEFAULT_PORT = 9100

class PrometheusExporter(Component):
    def __init__(
        self,
        name="prometheusexporter",
        port=DEFAULT_PORT,
        redeploy=False,
        command=None,
        **kwargs,
    ):

        if port != DEFAULT_PORT and command is None:
            command = f"--web.listen-address=:{port}"

        args = {
            "image": "prom/node-exporter:latest",
            "name": name,
            "stdout": False,
            "stderr": False,
            "redeploy": redeploy,
            "command": command,
            "upload_hosts": False
        }

        self.port = port
        args.update(kwargs)
        super().__init__(**args)
        self.expose_port(self.port, self.port)

    def target(self):
        return PrometheusTarget(self.name, f"{self.name}:{self.port}")

    def deployment_workflow(self, node):
        return Workflow([
            Deploy(self, node),
            WaitFor(self.port, self.name, 60)
        ])
