from backends.backend import Backend

class DebugBackend(Backend):

    def reserve_node(self, node):
        print(f"[RESERVE] Reserves node {node}")

    def deploy(self, node, component):
        """Deploy an image to a given node."""
        print(f"[DEPLOY] {image} -> {node}")
