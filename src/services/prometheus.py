from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent, indent

from component import Component


@dataclass
class PrometheusTarget:
    name: str
    addr: str


class Prometheus(Component):
    def config(self):
        jobs = "\n".join(
            dedent(
                f"""\
                - job_name: node
                  static_configs:
                    - targets:
                        - {target.addr}
                      labels:
                        node: {target.name}
                """
            )
            for target in self.targets
        )

        return dedent(
            f"""\
            global:
              scrape_interval: {self.scrape_interval}s

            scrape_configs:
            {indent(jobs, "  ")}
            """
        )

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
            raise RuntimeError(
                "You should either specify a config path or a target list "
                "to generate the configuration."
            )
        if targets is not None and config_path is not None:
            raise RuntimeError(
                "Cannot specify both 'targets' and 'container_conf_path'. "
                "Either provide 'targets' and let us generate the configuration, "
                "or provide 'container_conf_path' to use an existing configuration file."
            )            
        

        args = {
            "image": "prom/prometheus:v3.13.0",
            "name": name,
            "stdout": False,
            "stderr": False,
            "redeploy": redeploy,
            "entrypoint": "",
            "command": [
                "prometheus",
                f"--config.file={container_conf_path}",
            ],
        }
 
        self.targets = targets or []
        self.scrape_interval = scrape_interval

        args.update(kwargs)

        super().__init__(**args)

        if config_path is not None:
            path = Path(config_path).resolve()
            self.mount(str(path), container_conf_path)
