from component import Component


class Vider(Component):

    def __init__(
        self,
        name="vider",
        server_ip=None,
        tcp_port=None,
        tls_port=None,
        tls_cert_path=None,
        tls_key_path=None,
        quic_port=None,
        quic_cert_path=None,
        quic_key_path=None,
        broker_host=None,
        broker_port=None,
        **kwargs,
    ):
        env = {}

        if server_ip is not None:
            env["VIDER_SERVER_IP"] = str(server_ip)

        if tcp_port is not None:
            env["VIDER_TCP_PORT"] = str(tcp_port)

        if tls_port is not None:
            env["VIDER_TLS_PORT"] = str(tls_port)

        if tls_cert_path is not None:
            env["VIDER_TLS_CERT_PATH"] = tls_cert_path

        if tls_key_path is not None:
            env["VIDER_TLS_KEY_PATH"] = tls_key_path

        if quic_port is not None:
            env["VIDER_QUIC_PORT"] = str(quic_port)

        if quic_cert_path is not None:
            env["VIDER_QUIC_CERT_PATH"] = quic_cert_path

        if quic_key_path is not None:
            env["VIDER_QUIC_KEY_PATH"] = quic_key_path

        if broker_host is not None:
            env["VIDER_BROKER_HOST"] = broker_host

        if broker_port is not None:
            env["VIDER_BROKER_PORT"] = str(broker_port)

        if name is not None:
            env["VIDER_NAME"] = name

        args = {
            "image": "ghcr.io/zivomartin/vider:latest",
            "local_image": "vider:latest",
            "name": name,
            "stdout": False,
            "stderr": False,
            "env": env,
        }

        args.update(kwargs)

        super().__init__(**args)
