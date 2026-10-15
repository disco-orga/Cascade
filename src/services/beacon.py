from component import Component


class Beacon(Component):

    def __init__(
        self,
        name="beacon",
        broker=None,
        broker_port=None,
        channel_cap=None,
        **kwargs,
    ):
        env = {}

        if name is not None:
            env["BEACON_NAME"] = str(name)

        if broker is not None:
            env["BEACON_BROKER"] = str(broker)

        if broker_port is not None:
            env["BEACON_BROKER_PORT"] = str(broker_port)

        if channel_cap is not None:
            env["BEACON_CHANNEL_CAP"] = str(channel_cap)

        args = {
            "image": "ghcr.io/zivomartin/beacon:latest",
            "local_image": "beacon:latest",
            "name": name,
            "stdout": False,
            "stderr": False,
            "env": env,
        }

        args.update(kwargs)

        super().__init__(**args)
