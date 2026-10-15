from steps import Deploy, Workflow

class Component:
    """
    Represents a deployable unit in the cluster.

    A Component corresponds to a container image and its deployment
    configuration.
    """

    def __init__(
            self,
            image,
            fetch_image=True,
            name=None,
            local_image=None,
            node=None,
            command=None,
            stdout=False,
            stderr=True,
            ports=None,
            redeploy=True,
            env={},
            upload_hosts=True,
            entrypoint=None
    ):
        """
        Initialize a Component.
        """
        
        self.fetch_image = fetch_image
        self.env = env
        self.entrypoint = entrypoint
        self.node = node
        self.stdout = stdout
        self.stderr = stderr
        self.command = command
        self.name = image if name is None else name
        self.image = image
        self.ports = ports or {}
        self.mounting = {}
        self.dependencies = []
        self.redeploy = redeploy
        self.upload_hosts = upload_hosts
        self.local_image = local_image or image

    def get_image(self):
        return self.image if self.fetch_image else self.local_image

    def depends_on(self, dependency):
        if not isinstance(dependency, str):
            dependency = dependency.get_name()
        self.dependencies.append(dependency)

    def set_fetch_image(self, fetch_image):
        self.fetch_image = fetch_image

    def place_on(self, node):
        self.node = node

    def expose_port(self, from_p, to_p):
        self.ports[from_p] = to_p

    def get_dependencies(self):
        return self.dependencies

    def mount(self, src, target):
        self.mounting[src] = target

    def set_logs(self, stderr=None, stdout=None):
        if not stderr is None:
            self.stderr = stderr
        if not stdout is None:
            self.stdout = stdout

    def deployment_workflow(self, node):
        return Workflow([Deploy(self, node)])

    def get_name(self):
        return self.name

    def set_env(self, env):
        self.env = env

    def dev_env_variable(self, k, v):
        self.env[k] = v
