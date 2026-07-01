from component import Component

class Vider(Component):

    def __init__(self,
                 name="vider",
                 stream_server_ip="vider", 
                 stream_server_port=1808, 
                 web_server_ip="vider", 
                 web_server_port=3333, 
                 broker_host="mosquitto",
                 broker_port=1883
                 ):
        
        command = [
                "./vider",
                "--name", str(name),
                "--broker-port", str(broker_port),
                "--broker-host", broker_host,
                "--stream-server-ip", stream_server_ip,
                "--stream-server-port", str(stream_server_port),
                "--web-server-ip", web_server_ip,
                "--web-server-port", str(web_server_port),
            ]

        super().__init__(
            image="vider",
            name = name,
            stderr = False,
            stdout = False,
            ports = { f"{web_server_port}/tcp": web_server_port },
            command = command
        )
    
