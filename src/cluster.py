from component import Component
from backends.debug_backend import DebugBackend
from backends.docker_backend import DockerBackend
from steps import ParallelGroup, Step
from batch.streaming import StreamingBatch
from batch.prometheus import PrometheusBatch

class Cluster:

    """
    Represents the deployment cluster.

    The Cluster is responsible for:
    - Node allocation
    - Collecting components
    - Building a deployment workflow
    - Executing the deployment
    """

    def __init__(
            self,
            backend=DockerBackend(clean_before=True),
            setup_logging=True,
            max_concurrency=None,
            fetch_images=True
    ):
        """Initialize an empty cluster."""
        self.backend = backend
        self.nodes = []
        self.components = {}
        self.max_concurrency = max_concurrency
        self.fetch_images = fetch_images

        if setup_logging:
            self.setup_logging()

    def setup_logging(self):
        import logging
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(
                level=logging.INFO,
                format="[%(name)s] %(message)s"
            )

    def reserve_node(self, node):
        self.nodes.append(node)
        self.backend.reserve_node(node)

    def get_nodes(self, nodes):
        return self.nodes

    def add_batch(self, batch):
        batch.setup(self)

    def component_exists(self, name):
        return self.components.get(name) is not None

    def try_add(self, comp):
        if not self.component_exists(comp.name):
            self.add(comp)

    def add(self, comp):
        """
        Add a Component to the cluster.
        """
        if not self.component_exists(comp.name):
            if not self.fetch_images:
                comp.set_fetch_image(False)
            self.components[comp.name] = comp
        else:
            raise RuntimeError("You cannot add 2 components with the same name.")

    def add_multiple(self, comps):
        """
        Add a each component to the cluster.
        """
        for comp in comps:
            self.add(comp)

    def get_sorted_components(self):
        """
        Return a topological sort of the components based on the dependency graph.
        Fail if detects a cycle.
        """

        result = []
        state = {}

        def visit(comp):
            name = comp.get_name()
            s = state.get(name, 0)

            if s == 1:
                raise RuntimeError(f"Dependency cycle detected involving {name}")

            if s == 2:
                return

            state[name] = 1

            for dep in comp.get_dependencies():
                visit(dep)

            state[name] = 2
            result.append(comp)

        for comp in self.components.values():
            visit(comp)

        return result



    def get_parallel_sorted_components(self):
        result = {}
        state = {}
        comp_map = {}

        def visit(name):
            comp = self.components[name]
            s = state.get(name, 0)
            
            if s == 1:
                raise RuntimeError(f"Dependency cycle detected involving {name}")

            if s == 2:
                return comp_map[name]

            state[name] = 1

            my_index = 0
            for parent in comp.get_dependencies():
                candidate = visit(parent) + 1
                if candidate > my_index:
                    my_index = candidate

            if my_index not in result:
                result[my_index] = []

            comp_map[name] = my_index
            result[my_index].append(comp)
            state[name] = 2
            return my_index

        for comp in self.components.values():
            visit(comp.get_name())

        return [result[k] for k in sorted(result)]

    def _build_plan(self):
        """
        Build a deployment plan.
        The plan assigns each component replica to a node.
        """
        n = len(self.nodes)

        if n == 0:
            raise ValueError("No nodes allocated")

        def build_components_workflow(components, i=0):
            nodes = dict.fromkeys(self.nodes, 0)
            workflows = []
            for comp in components:
                if comp.node is not None and not comp.node in nodes:
                    raise RuntimeError(f"The node {comp.node} of the component {comp.name} is not declared in the cluster.")

                node = min(nodes, key=nodes.get) if comp.node is None else comp.node
                workflows.append(comp.deployment_workflow(node))
                nodes[node] += 1
            return (workflows, i)

        if self.max_concurrency is not None:
            launching_rounds = self.get_parallel_sorted_components()
            i = 0
            plan = []
            for components in launching_rounds:
                (workflows, i) = build_components_workflow(components)
                plan_round = workflows[0] if len(workflows) == 1 else ParallelGroup(workflows, self.max_concurrency)
                plan.append(plan_round)

            return plan
        else:
            components = self.get_sorted_components()
            (plan, _) = build_components_workflow(components)

            return plan

        
    def _execute(self, plan):
        """
        Execute the deployment plan.
        """
        for plan_step in plan:
            plan_step.process(self.backend)

    def run(self):
        """
        Run the deployment process.
        This includes:
        1. Building the deployment workflow
        2. Allocate the nodes
        3. Executing it
        """
        plan = self._build_plan()
        self.backend.setup()
        self._execute(plan)


    def add_streaming(self, **kwargs):
        self.add_batch(StreamingBatch(**kwargs))

    def add_monitoring(self, **kwargs):
        self.add_batch(PrometheusBatch(**kwargs))

    def get_comp(self, name):
        return self.components[name]
