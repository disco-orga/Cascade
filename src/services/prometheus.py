from dataclasses import dataclass
from pathlib import Path
import tempfile
from component import Component
import yaml
from steps import Deploy, Do, Workflow
import os


@dataclass
class PrometheusTarget:
    """A target to be scraped by Prometheus.

    Args:
        name: Logical name of the target, used as its Prometheus node label
            and for backend name resolution when no host is provided.
        host: Hostname or IP address of the target. If None, the host is
            resolved through the deployment backend using `name`.
        port: Port exposing the Prometheus metrics endpoint.
            Defaults to 9100 (Node Exporter).
    """

    name: str
    host: str | None = None    
    port: int = 9100


class Prometheus(Component):

    def config(self, backend):
        targets = []

        for target in self.targets:
            host = target.host
            if host is None:
                host = backend.resolve_name(target.name)

            targets.append({
                "targets": [f"{host}:{target.port}"],
                "labels": {"node": target.name},
            })

        config = {
            "global": {
                "scrape_interval": f"{self.scrape_interval}s",
            },
            "scrape_configs": [
                {
                    "job_name": "node",
                    "static_configs": targets,
                }
            ],
        }

        return yaml.safe_dump(config, sort_keys=False)

    def __init__(
        self,
        scrape_interval=5,
        targets=None,
        config_path = None,
        container_conf_path="/etc/prometheus/prometheus.yml",
        name="prometheus",
        redeploy=False,
        **kwargs,
    ):
        if targets is None and config_path is None:
            raise ValueError(
                "You should either specify a config path or a target list "
                "to generate the configuration."
            )
        if targets is not None and config_path is not None:
            raise ValueError(
                "Cannot specify both 'targets' and 'config_path'. "
                "Either provide 'targets' and let us generate the configuration, "
                "or provide 'container_conf_path' to use an existing configuration file."
            )            
        

        args = {
            "image": "prom/prometheus:v3.13.0",
            "name": name,
            "stdout": False,
            "stderr": False,
            "redeploy": redeploy,
            "command": [
                f"--config.file={container_conf_path}",
            ],
        }
 
        self.targets = targets or []
        self.scrape_interval = scrape_interval
        self.name = name

        args.update(kwargs)

        super().__init__(**args)

        self.gen_config = config_path is None
        self.container_conf_path = container_conf_path

        if not self.gen_config:
            path = Path(config_path).resolve()
            self.mount(str(path), container_conf_path)


    def generate_config(self, backend):
        if self.gen_config:
            with tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8", delete=False) as f:
                f.write(self.config(backend))
                f.flush()
                os.chmod(f.name, 0o644)

                self.mount(f.name, self.container_conf_path)


    def deployment_workflow(self, node):
        return Workflow([
            Do(lambda backend: self.generate_config(backend)),
            Deploy(self, node),
        ])

