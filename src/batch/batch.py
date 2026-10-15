from abc import ABC, abstractmethod

class Batch(ABC):

    @abstractmethod
    def setup(cluster):
        pass
