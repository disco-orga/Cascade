from abc import ABC, abstractmethod

class Backend(ABC):

    @abstractmethod
    def reserve_node(self, node):
        """Remembers to reserve a specific node"""
        pass

    @abstractmethod
    def setup(self):
        """Called before the deployment to allocate nodes and manage network"""
        pass

    @abstractmethod
    def deploy(self, node, component):
        """Deploy an image to a given node."""
        pass
