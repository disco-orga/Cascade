import time
from cluster import Cluster
from services.prometheus import Prometheus
from services.prometheus_exporter import PrometheusExporter
from services.mosquitto import Mosquitto
from services.argus import Argus
from services.kairos import Kairos
from backends.docker_backend import DockerBackend
from backends.expeca import ExpecaBackend, ExpecaNode

# cluster = Cluster(backend=ExpecaBackend())
# cluster.reserve_node(ExpecaNode("worker-07", 0, 4))

cluster = Cluster(backend=DockerBackend())
cluster.reserve_node("worker")

mosquitto = Mosquitto(redeploy=False)

exp = PrometheusExporter(redeploy=False)
prom = Prometheus(redeploy=True, targets=[exp.target()])

argus = Argus(image="argus", redeploy=True, stdout=True, stderr=True)
kairos = Kairos(image="kairos", stdout=True, stderr=True)

argus.depends_on(prom)
argus.depends_on(mosquitto)
prom.depends_on(exp)
kairos.depends_on(argus)

cluster.add_multiple([mosquitto, prom, exp, argus, kairos])

cluster.run()

while True:
    time.sleep(1)
