from batch.batch import Batch

from services.argus import Argus
from services.prometheus import Prometheus
from services.prometheus_exporter import PrometheusExporter
from services.mosquitto import Mosquitto

class PrometheusBatch(Batch):
    """
    Bundle of services providing the default monitoring infrastructure.

    Adds Prometheus, Argus, Mosquitto, and Prometheus exporters to the
    cluster. By default, one exporter is created for each cluster node.

    The dependency graph is:

        Exporters -> Prometheus -> Argus
                     Mosquitto -> Argus

    Custom service instances and exporters can be provided to override
    the defaults.
    """


    def __init__(
            self,
            prom_config=None,
            prom=None,
            exporters={},
            argus=None,
            broker=None
    ):
        self.argus = argus or Argus()

        if prom is None and prom_config is None:
            raise RuntimeError("Please, specify a config path for prometheus.")
        self.prom = prom or Prometheus(config_path=prom_config)

        self.broker = broker or Mosquitto()
        self.exporters = exporters

        self.argus.depends_on(self.prom)
        self.argus.depends_on(self.broker)

    def setup(self, cluster):
                
        self.exporters = self.exporters or [PrometheusExporter(node=node) for node in cluster.nodes]
        
        for exp in self.exporters:
            self.prom.depends_on(exp)
            cluster.try_add(exp)

        for service in [self.argus, self.prom, self.broker]:
            cluster.try_add(service)



    
