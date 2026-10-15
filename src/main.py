import os
import time
from cluster import Cluster
from component import Component
from services.mosquitto import Mosquitto
from backends.expeca import ExpecaBackend, ExpecaNode
from backends.docker_backend import DockerBackend

cluster = Cluster(backend=ExpecaBackend(), max_concurrency=1)
cluster.reserve_node(ExpecaNode("worker-07", days=0, hours=4))

# cluster = Cluster(backend=DockerBackend(), max_concurrency=5, fetch_images=False)
# cluster.reserve_node("node")

# Add the services

cluster.add_streaming()
cluster.add_monitoring(prom_config="./prometheus.yml")


# Add the app nodes

robot_count = 3
image = "explorer"

kairos = Component(
    "kairos",
    name="kairos",
    stdout=True
)
kairos.depends_on("argus")
cluster.add(kairos)

prism = Component(
    "prism",
    name=f"prism"
)
prism.expose_port(3333, 3333)
prism.depends_on("vider")
cluster.add(prism)


for i in range(robot_count):
    component = Component(
        image,
        name=f"node-{i}",
        command=["./explorer", "process", f"{i}", "--video-kind", "gol", "--n", f"{robot_count}", "--framing", "unified"],
        stdout=True
    )

    # Vider is part of the streaming batch
    component.depends_on("prism")
    cluster.add(component)


cloud = Component(
    image,
    name=f"cloud",
    command=["./explorer", "cloud"]
)

# Mosquitto is part of the streaming and prometheus batch
cloud.depends_on("mosquitto")
cluster.add(cloud)

for name in ["argus"]:
    cluster.get_comp(name).set_logs(stdout=True, stderr=False)

# # Execute deployment
cluster.run()

while True:
    pass
