from batch.batch import Batch

from services.vider import Vider
from services.beacon import Beacon
from services.mosquitto import Mosquitto

class StreamingBatch(Batch):
    """
    Bundle of services providing the default streaming infrastructure.

    Adds the following services to the cluster:

        Mosquitto -> Beacon -> Vider

    where each service is started after its dependency is ready.

    Custom service instances can be provided to override the defaults.
    """

    def __init__(
            self,
            vider=None,
            beacon=None,
            broker=None
    ):

        self.vider = vider or Vider()
        self.beacon = beacon or Beacon()
        self.broker = broker or Mosquitto()

        self.vider.depends_on(self.beacon)
        self.beacon.depends_on(self.broker)


    def setup(self, cluster):
        for service in [self.vider, self.beacon, self.broker]:
            cluster.try_add(service)

