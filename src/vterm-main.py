(.venv) ➜  Cascade docker rm -f $(docker ps -aq)                      
0ffcdc4e1466
cd913a87c0a1
(.venv) ➜  Cascade python src/main.py            
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Traceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/clien
t.py", line 275, in _raise_for_status
    response.raise_for_status()
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/requests/models.
py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 409 Client Error: Conflict for url: http+docker://localhost/v1.5
5/containers/1ec49aaa874f9c26661a0594cc55b16d0befaaee398088f1839979b7fe395f66/exec

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 70, in <module>
    cluster.run()
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 206, in run
    self._execute(plan)
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 194, in _execute
    plan_step.process(self.backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 71, in process
    future.result()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/_base.py", line 4
45, in result
    return self.__get_result()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/_base.py", line 3
90, in __get_result
    raise self._exception
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/thread.py", line 
52, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 53, in exec_one_workflow
    workflow.process(backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 25, in process
    step.process(backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 81, in process
    backend.wait_for(self.host, self.port, self.timeout)
  File "/home/martin/Projects/disco/Cascade/src/backends/docker_backend.py", line 39, in wait_f
or
    exit_code, _ = container.exec_run(f"nc -z localhost {port}")
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/models/co
ntainers.py", line 209, in exec_run
    resp = self.client.api.exec_create(
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/utils/dec
orators.py", line 19, in wrapped
    return f(self, resource_id, *args, **kwargs)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/exec_
api.py", line 78, in exec_create
    return self._result(res, True)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/clien
t.py", line 281, in _result
    self._raise_for_status(response)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/clien
t.py", line 277, in _raise_for_status
    raise create_api_error_from_http_exception(e) from e
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/errors.py
", line 39, in create_api_error_from_http_exception
    raise cls(e, response=response, explanation=explanation) from e
docker.errors.APIError: 409 Client Error for http+docker://localhost/v1.55/containers/1ec49aaa8
74f9c26661a0594cc55b16d0befaaee398088f1839979b7fe395f66/exec: Conflict ("container 1ec49aaa874f
9c26661a0594cc55b16d0befaaee398088f1839979b7fe395f66 is not running")
(.venv) ➜  Cascade python src/main.py
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Traceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/clien
t.py", line 275, in _raise_for_status
    response.raise_for_status()
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/requests/models.
py", line 1167, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 409 Client Error: Conflict for url: http+docker://localhost/v1.5
5/containers/create?name=mosquitto

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/backends/docker_backend.py", line 101, in deplo
y
    container = self.client.containers.run(
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/models/co
ntainers.py", line 877, in run
    container = self.create(image=image, command=command,
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/models/co
ntainers.py", line 936, in create
    resp = self.client.api.create_container(**create_kwargs)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/conta
iner.py", line 440, in create_container
    return self.create_container_from_config(config, name, platform)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/conta
iner.py", line 457, in create_container_from_config
    return self._result(res, True)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/clien
t.py", line 281, in _result
    self._raise_for_status(response)
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/api/clien
t.py", line 277, in _raise_for_status
    raise create_api_error_from_http_exception(e) from e
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/docker/errors.py
", line 39, in create_api_error_from_http_exception
    raise cls(e, response=response, explanation=explanation) from e
docker.errors.APIError: 409 Client Error for http+docker://localhost/v1.55/containers/create?na
me=mosquitto: Conflict ("Conflict. The container name "/mosquitto" is already in use by contain
er "1ec49aaa874f9c26661a0594cc55b16d0befaaee398088f1839979b7fe395f66". You have to remove (or r
ename) that container to be able to reuse that name.")

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 70, in <module>
    cluster.run()
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 206, in run
    self._execute(plan)
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 194, in _execute
    plan_step.process(self.backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 71, in process
    future.result()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/_base.py", line 4
45, in result
    return self.__get_result()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/_base.py", line 3
90, in __get_result
    raise self._exception
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/thread.py", line 
52, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 53, in exec_one_workflow
    workflow.process(backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 25, in process
    step.process(backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 33, in process
    backend.deploy(self.comp, self.node)
  File "/home/martin/Projects/disco/Cascade/src/backends/docker_backend.py", line 121, in deplo
y
    raise RuntimeError(
RuntimeError: Docker API error while deploying 'mosquitto': Conflict. The container name "/mosq
uitto" is already in use by container "1ec49aaa874f9c26661a0594cc55b16d0befaaee398088f1839979b7
fe395f66". You have to remove (or rename) that container to be able to reuse that name.
(.venv) ➜  Cascade docker rm -f $(docker ps -aq) 
1ec49aaa874f
87f6737f2004
(.venv) ➜  Cascade python src/main.py            
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Deploying prometheus with image prom/prometheus:v3.13.0
Deploying beacon with image beacon:latest
Deploying cloud with image explorer
Deploying vider with image vider:latest
Deploying argus with image argus:latest
[cloud] Cloud: Failed to poll over MQTT: I/O: Connection refused (os error 111)
Deploying kairos with image kairos
Deploying prism with image prism
[argus] 2026-09-23T11:25:16.780178Z  INFO Argus: Starting Argus
Deploying node-0 with image explorer
Deploying node-1 with image explorer
Deploying node-2 with image explorer
[prism] Error: Launching loop terminated unexpectedly
[prism] 
[prism] Caused by:
[prism] 0: Failed to fetch vider address.
[prism] 1: I/O: Connection refused (os error 111)
[prism] 2: Connection refused (os error 111)
[kairos] 2026-09-23T11:25:17.128769Z  INFO kairos: Starting Kairos.
[kairos] 2026-09-23T11:25:17.128835Z  INFO kairos: Listening
[kairos] 2026-09-23T11:25:17.129803Z ERROR kairos: Failed to poll MQTT event error=I/O: Connect
ion refused (os error 111)
[node-0] Node 0: Starting.
[node-0] Trying to fetch the map.
[node-0] Failed to poll.
[node-2] Node 2: Starting.
[node-2] Trying to fetch the map.
[node-2] Failed to poll.
[node-1] Node 1: Starting.
[node-1] Trying to fetch the map.
[node-1] Failed to poll.
^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 72, in <module>
    while True:
KeyboardInterrupt

(.venv) ➜  Cascade docker container list -a      
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS    
                  PORTS                                         NAMES
01d7e2b5535e   explorer                    "./explorer process …"   12 seconds ago   Up 12 seco
nds                                                             node-2
7283486970ba   explorer                    "./explorer process …"   12 seconds ago   Up 12 seco
nds                                                             node-1
8795ceb39509   explorer                    "./explorer process …"   12 seconds ago   Up 12 seco
nds                                                             node-0
3b4f56aca7a1   prism                       "./prism"                13 seconds ago   Exited (1)
 12 seconds ago                                                 prism
fd4ad62a27e6   kairos                      "./kairos"               13 seconds ago   Exited (0)
 12 seconds ago                                                 kairos
bbbfd9ea0138   argus:latest                "./argus --name argu…"   13 seconds ago   Exited (1)
 12 seconds ago                                                 argus
7b20f1ce308d   vider:latest                "./vider"                13 seconds ago   Up 12 seco
nds                                                             vider
25445e010bd4   prom/prometheus:v3.13.0     "/bin/prometheus --c…"   13 seconds ago   Up 13 seco
nds               9090/tcp                                      prometheus
354340bd917c   explorer                    "./explorer cloud"       13 seconds ago   Exited (0)
 12 seconds ago                                                 cloud
21ff772b7687   beacon:latest               "./beacon"               13 seconds ago   Exited (1)
 13 seconds ago                                                 beacon
1709c621b060   eclipse-mosquitto:latest    "/docker-entrypoint.…"   14 seconds ago   Up 13 seco
nds               1883/tcp                                      mosquitto
d4fb6ec596b2   prom/node-exporter:latest   "/bin/node_exporter"     14 seconds ago   Up 13 seco
nds               0.0.0.0:9100->9100/tcp, [::]:9100->9100/tcp   prometheus_exporter
(.venv) ➜  Cascade docker container list -a
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                      PORTS                                         NAMES
01d7e2b5535e   explorer                    "./explorer process …"   13 seconds ago   Up 13 seconds                                                             node-2
7283486970ba   explorer                    "./explorer process …"   13 seconds ago   Up 13 seconds                                                             node-1
8795ceb39509   explorer                    "./explorer process …"   13 seconds ago   Up 13 seconds                                                             node-0
3b4f56aca7a1   prism                       "./prism"                14 seconds ago   Exited (1) 13 seconds ago                                                 prism
fd4ad62a27e6   kairos                      "./kairos"               14 seconds ago   Exited (0) 13 seconds ago                                                 kairos
bbbfd9ea0138   argus:latest                "./argus --name argu…"   14 seconds ago   Exited (1) 13 seconds ago                                                 argus
7b20f1ce308d   vider:latest                "./vider"                14 seconds ago   Up 13 seconds                                                             vider
25445e010bd4   prom/prometheus:v3.13.0     "/bin/prometheus --c…"   14 seconds ago   Up 14 seconds               9090/tcp                                      prometheus
354340bd917c   explorer                    "./explorer cloud"       14 seconds ago   Exited (0) 13 seconds ago                                                 cloud
21ff772b7687   beacon:latest               "./beacon"               14 seconds ago   Exited (1) 14 seconds ago                                                 beacon
1709c621b060   eclipse-mosquitto:latest    "/docker-entrypoint.…"   15 seconds ago   Up 14 seconds               1883/tcp                                      mosquitto
d4fb6ec596b2   prom/node-exporter:latest   "/bin/node_exporter"     15 seconds ago   Up 14 seconds               0.0.0.0:9100->9100/tcp, [::]:9100->9100/tcp   prometheus_exporter
(.venv) ➜  Cascade docker logs 1709c621b060            
1790162716: Info: running mosquitto as user: mosquitto.
1790162716: mosquitto version 2.1.2 starting
1790162716: Using default config.
1790162716: Bridge support available.
1790162716: Persistence support available.
1790162716: TLS support available.
1790162716: TLS-PSK support available.
1790162716: Websockets support available.
1790162716: Starting in local only mode. Connections will only be possible from clients running on this machine.
1790162716: Create a configuration file which defines a listener to allow remote access.
1790162716: For more details see https://mosquitto.org/documentation/authentication-methods/
1790162716: Opening ipv4 listen socket on port 1883.
1790162716: Opening ipv6 listen socket on port 1883.
1790162716: Opening http api listen socket on port 9883.
1790162716: Using http_dir /usr/share/mosquitto/dashboard
1790162716: mosquitto version 2.1.2 running
1790162716: New connection from ::1:40639 on port 1883.
1790162716: Client ::1 [::1:40639] disconnected: connection closed by client.
(.venv) ➜  Cascade docker rm -f $(docker ps -aq) &                    
[1] 13532
(.venv) ➜  Cascade docker rm -f $(docker ps -aq) &01d7e2b5535e
7283486970ba
8795ceb39509
3b4f56aca7a1
fd4ad62a27e6
bbbfd9ea0138
7b20f1ce308d
25445e010bd4
354340bd917c
21ff772b7687
1709c621b060
d4fb6ec596b2

[1]  + 13532 done       docker rm -f $(docker ps -aq)
(.venv) ➜  Cascade docker rm -f $(docker ps -aq) && python src/main.py
docker: 'docker rm' requires at least 1 argument

Usage:  docker rm [OPTIONS] CONTAINER [CONTAINER...]

See 'docker rm --help' for more information
(.venv) ➜  Cascade python src/main.py       
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Deploying prometheus with image prom/prometheus:v3.13.0
Deploying beacon with image beacon:latest
Deploying cloud with image explorer
Deploying vider with image vider:latest
Deploying argus with image argus:latest
[cloud] Cloud: Failed to poll over MQTT: I/O: Connection refused (os error 111)
Deploying kairos with image kairos
Deploying prism with image prism
[argus] 2026-09-23T11:25:55.509691Z  INFO Argus: Starting Argus
Deploying node-0 with image explorer
Deploying node-1 with image explorer
Deploying node-2 with image explorer
[kairos] 2026-09-23T11:25:55.807537Z  INFO kairos: Starting Kairos.
[kairos] 2026-09-23T11:25:55.807603Z  INFO kairos: Listening
[kairos] 2026-09-23T11:25:55.808493Z ERROR kairos: Failed to poll MQTT event error=I/O: Connect
[prism] Error: Launching loop terminated unexpectedly
[prism] 
[prism] Caused by:
[prism] 0: Failed to fetch vider address.
[prism] 1: I/O: Connection refused (os error 111)
[prism] 2: Connection refused (os error 111)
[node-0] Node 0: Starting.
[node-0] Trying to fetch the map.
[node-0] Failed to poll.
[node-1] Node 1: Starting.
[node-1] Trying to fetch the map.
[node-1] Failed to poll.
[node-2] Node 2: Starting.
[node-2] Trying to fetch the map.
[node-2] Failed to poll.
^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 72, in <module>
    while True:
KeyboardInterrupt

(.venv) ➜  Cascade docker rm -f $(docker ps -aq) && python src/main.py
8f5f9db13f49
e1364ed19613
7cdfad218728
ce1f3aa882d7
8c862546d6ec
25cf00bf6bca
3f6491f1259a
0d0594ef71e4
190aefa5a648
17f363496330
79d6f12b4e06
5d7ab98a96d9
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Deploying prometheus with image prom/prometheus:v3.13.0
Deploying beacon with image beacon:latest
Deploying cloud with image explorer
Deploying argus with image argus:latest
Deploying vider with image vider:latest
[argus] 2026-09-23T11:26:09.684099Z  INFO Argus: Starting Argus
Deploying prism with image prism
Deploying kairos with image kairos
[argus] 2026-09-23T11:26:10.016960Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:26:10.016987Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:26:10.018782Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
Deploying node-0 with image explorer
Deploying node-1 with image explorer
[kairos] 2026-09-23T11:26:10.015648Z  INFO kairos: Starting Kairos.
[kairos] 2026-09-23T11:26:10.015687Z  INFO kairos: Listening
Deploying node-2 with image explorer
[node-1] Node 1: Starting.
[node-1] Trying to fetch the map.
[node-2] Node 2: Starting.
[node-2] Trying to fetch the map.
[node-0] Node 0: Starting.
[node-0] Trying to fetch the map.
[argus] 2026-09-23T11:26:12.017862Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:26:12.017894Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:26:12.018776Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
[argus] 2026-09-23T11:26:14.018266Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:26:14.018297Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:26:14.019088Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 72, in <module>
    while True:
KeyboardInterrupt

(.venv) ➜  Cascade mosquitto -p 1883                                               
1790164273: Info: running mosquitto as user: martin.
1790164273: mosquitto version 2.1.2 starting
1790164273: Using default config.
1790164273: Bridge support available.
1790164273: Persistence support available.
1790164273: TLS support available.
1790164273: TLS-PSK support available.
1790164273: Websockets support available.
1790164273: Starting in local only mode. Connections will only be possible from clients running
 on this machine.
1790164273: Create a configuration file which defines a listener to allow remote access.
1790164273: For more details see https://mosquitto.org/documentation/authentication-methods/
1790164273: Opening ipv4 listen socket on port 1883.
1790164273: Opening ipv6 listen socket on port 1883.
1790164273: mosquitto version 2.1.2 running
^C1790164275: mosquitto version 2.1.2 terminating
(.venv) ➜  Cascade docker rm -f $(docker ps -aq) && python src/main.py
05fdfcf9f244
bc25cebc38bf
dd025160c3f9
b8d8444d54f9
738f39faabee
a3de762f826b
61bd00cf7424
89b8e644c54b
6356da1694f1
61d92abb0e30
70b68bbafd9e
86e291f2ecf1
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Deploying prometheus with image prom/prometheus:v3.13.0
Deploying beacon with image beacon:latest
Deploying cloud with image explorer
Deploying vider with image vider:latest
Deploying argus with image argus:latest
[cloud] Cloud: Failed to poll over MQTT: I/O: Connection refused (os error 111)
Deploying kairos with image kairos
Deploying prism with image prism
[argus] 2026-09-23T11:51:20.512304Z  INFO Argus: Starting Argus
[prism] Error: Launching loop terminated unexpectedly
[prism] 
[prism] Caused by:
[prism] 0: Failed to fetch vider address.
[prism] 1: I/O: Connection refused (os error 111)
[prism] 2: Connection refused (os error 111)
Deploying node-1 with image explorer
Deploying node-2 with image explorer
Deploying node-0 with image explorer
[kairos] 2026-09-23T11:51:20.840638Z  INFO kairos: Starting Kairos.
[kairos] 2026-09-23T11:51:20.840683Z  INFO kairos: Listening
[kairos] 2026-09-23T11:51:20.841522Z ERROR kairos: Failed to poll MQTT event error=I/O: Connect
ion refused (os error 111)
[node-1] Node 1: Starting.
[node-1] Trying to fetch the map.
[node-1] Failed to poll.
[node-2] Node 2: Starting.
[node-2] Trying to fetch the map.
[node-2] Failed to poll.
[node-0] Node 0: Starting.
[node-0] Trying to fetch the map.
[node-0] Failed to poll.
^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 72, in <module>
    while True:
KeyboardInterrupt

(.venv) ➜  Cascade docker rm -f $(docker ps -aq) && python src/main.  
b24503e92846
71313d7775f6
fd76f98c36d9
eaf490788231
33ffe03e9068
cc779c6739c5
41727c49dab4
fbbd31ea59cb
415ec37a463a
0c069482379f
8e96b5e3ecc8
346ba0cecc74
python: can't open file '/home/martin/Projects/disco/Cascade/src/main.': [Errno 2] No such file
 or directory
(.venv) ➜  Cascade 
(.venv) ➜  Cascade python src/main.py       
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
^C^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 71, in process
    future.result()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/_base.py", line 4
40, in result
    self._condition.wait(timeout)
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/threading.py", line 320, in wait
    waiter.acquire()
KeyboardInterrupt

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 70, in <module>
    cluster.run()
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 206, in run
    self._execute(plan)
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 194, in _execute
    plan_step.process(self.backend)
  File "/home/martin/Projects/disco/Cascade/src/steps.py", line 57, in process
    with ThreadPoolExecutor() as ex:
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/_base.py", line 6
36, in __exit__
    self.shutdown(wait=True)
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/thread.py", line 
229, in shutdown
    t.join()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/threading.py", line 1089, in join
    self._wait_for_tstate_lock()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/threading.py", line 1105, in _wait_f
or_tstate_lock
    elif lock.acquire(block, timeout):
KeyboardInterrupt
^CException ignored in: <module 'threading' from '/home/martin/.pyenv/versions/3.10.0/lib/pytho
n3.10/threading.py'>
Traceback (most recent call last):
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/threading.py", line 1525, in _shutdo
wn
    atexit_call()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/concurrent/futures/thread.py", line 
31, in _python_exit
    t.join()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/threading.py", line 1089, in join
    self._wait_for_tstate_lock()
  File "/home/martin/.pyenv/versions/3.10.0/lib/python3.10/threading.py", line 1105, in _wait_f
or_tstate_lock
    elif lock.acquire(block, timeout):
KeyboardInterrupt: 

(.venv) ➜  Cascade docker container list -a                         
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS    
      PORTS                                         NAMES
3170295a69ce   eclipse-mosquitto:latest    "/docker-entrypoint.…"   50 seconds ago   Up 50 seco
nds   1883/tcp                                      mosquitto
f9a5e339b32d   prom/node-exporter:latest   "/bin/node_exporter"     50 seconds ago   Up 50 seco
nds   0.0.0.0:9100->9100/tcp, [::]:9100->9100/tcp   prometheus_exporter
(.venv) ➜  Cascade docker logs 3170295a69ce            
1790164400: Info: running mosquitto as user: mosquitto.
1790164400: mosquitto version 2.1.2 starting
1790164400: Config loaded from /mosquitto/config/mosquitto.conf.
1790164400: Bridge support available.
1790164400: Persistence support available.
1790164400: TLS support available.
1790164400: TLS-PSK support available.
1790164400: Websockets support available.
1790164400: Opening ipv4 listen socket on port 1883.
1790164400: mosquitto version 2.1.2 running
(.venv) ➜  Cascade docker exec mosquitto sh -c 'nc -z 127.0.0.1 1883; echo $?'
0
(.venv) ➜  Cascade docker exec mosquitto sh -c 'nc -z ::1 1883; echo $?'
1
(.venv) ➜  Cascade docker rm -f $(docker ps -aq) && python src/main.          
3170295a69ce
f9a5e339b32d
python: can't open file '/home/martin/Projects/disco/Cascade/src/main.': [Errno 2] No such file
 or directory
(.venv) ➜  Cascade 
(.venv) ➜  Cascade python src/main.py       
Deploying mosquitto with image eclipse-mosquitto:latest
Deploying prometheus_exporter with image prom/node-exporter:latest
Deploying prometheus with image prom/prometheus:v3.13.0
Deploying beacon with image beacon:latest
Deploying cloud with image explorer
Deploying vider with image vider:latest
Deploying argus with image argus:latest
Deploying kairos with image kairos
Deploying prism with image prism
[argus] 2026-09-23T11:56:48.652051Z  INFO Argus: Starting Argus
[argus] 2026-09-23T11:56:49.001943Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:56:49.001981Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:56:49.003599Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
Deploying node-0 with image explorer
Deploying node-2 with image explorer
Deploying node-1 with image explorer
[kairos] 2026-09-23T11:56:49.000276Z  INFO kairos: Starting Kairos.
[kairos] 2026-09-23T11:56:49.000318Z  INFO kairos: Listening
[node-0] Node 0: Starting.
[node-0] Trying to fetch the map.
[node-1] Node 1: Starting.
[node-1] Trying to fetch the map.
[node-2] Node 2: Starting.
[node-2] Trying to fetch the map.
[node-2] Successfully got the map.
[node-2] Generating map..
[node-2] Generation completed.
[node-2] Node 2: Connecting..
[node-0] Successfully got the map.
[node-0] Generating map..
[node-0] Generation completed.
[node-0] Node 0: Connecting..
[node-1] Successfully got the map.
[node-1] Generating map..
[node-1] Generation completed.
[node-1] Node 1: Connecting..
[node-1] Response { delegate_to: None, id: "1-1" }
[node-1] Solving locally
[node-1] Node 1: Successfully connected.
[node-0] Response { delegate_to: None, id: "0-1" }
[node-0] Solving locally
[node-0] Node 0: Successfully connected.
[node-2] Response { delegate_to: None, id: "2-1" }
[node-2] Solving locally
[node-2] Node 2: Successfully connected.
[node-1] Response { delegate_to: None, id: "1-2" }
[node-1] Solving locally
[node-1] Response { delegate_to: None, id: "1-3" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-2" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-2" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-4" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-3" }
[node-0] Solving locally
[node-0] Response { delegate_to: None, id: "0-4" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-3" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-5" }
[node-1] Solving locally
[node-1] Response { delegate_to: None, id: "1-6" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-5" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-4" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-6" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-5" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-7" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-7" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-6" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-8" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-8" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-7" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-9" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-9" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-8" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-10" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-10" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-11" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-11" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-9" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-12" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-10" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-12" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-11" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-13" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-13" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-12" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-14" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-13" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-14" }
[node-1] Solving locally
[argus] 2026-09-23T11:56:51.001407Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:56:51.001448Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:56:51.002620Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
[node-0] Response { delegate_to: None, id: "0-15" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-14" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-15" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-16" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-16" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-17" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-15" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-17" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-18" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-16" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-18" }
[node-1] Solving locally
[node-1] Response { delegate_to: None, id: "1-19" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-19" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-17" }
[node-2] Solving locally
[node-2] Response { delegate_to: None, id: "2-18" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-20" }
[node-1] Solving locally
[node-1] Response { delegate_to: None, id: "1-21" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-20" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-22" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-19" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-21" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-23" }
[node-1] Solving locally
[node-1] Response { delegate_to: None, id: "1-24" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-20" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-25" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-22" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-21" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-26" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-23" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-22" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-27" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-24" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-23" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-25" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-28" }
[node-1] Solving locally
[argus] 2026-09-23T11:56:53.002475Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:56:53.002504Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:56:53.003105Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
[node-1] Response { delegate_to: None, id: "1-29" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-26" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-24" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-27" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-25" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-30" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-26" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-28" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-27" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-31" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-29" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-28" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-32" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-30" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-29" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-33" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-30" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-34" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-31" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-31" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-35" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-32" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-32" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-33" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-36" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-34" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-33" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-37" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-35" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-38" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-34" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-39" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-35" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-36" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-40" }
[node-1] Solving locally
[argus] 2026-09-23T11:56:55.004133Z  INFO Argus::prometheus: New request for nodes All, and met
rics [CpuUsage, Up]
[argus] 2026-09-23T11:56:55.004153Z  INFO Argus::prometheus: Waiting for response from promethe
us..
[argus] 2026-09-23T11:56:55.004664Z  INFO Argus::prometheus: Responses collected successfully f
or 0 nodes
[node-2] Response { delegate_to: None, id: "2-36" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-37" }
[node-0] Solving locally
[node-1] Response { delegate_to: None, id: "1-41" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-38" }
[node-0] Solving locally
[node-0] Response { delegate_to: None, id: "0-39" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-37" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-42" }
[node-1] Solving locally
[node-1] Response { delegate_to: None, id: "1-43" }
[node-1] Solving locally
[node-2] Response { delegate_to: None, id: "2-38" }
[node-2] Solving locally
[node-0] Response { delegate_to: None, id: "0-40" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-39" }
[node-2] Solving locally
[node-1] Response { delegate_to: None, id: "1-44" }
[node-1] Solving locally
[node-0] Response { delegate_to: None, id: "0-41" }
[node-0] Solving locally
[node-2] Response { delegate_to: None, id: "2-40" }
[node-2] Solving locally
^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 72, in <module>
    while True:
KeyboardInterrupt

(.venv) ➜  Cascade docker rm -f $(docker ps -aq)                    
6265262a684d
539471834d95
6940649ab996
1c4b46f14e70
7117c96fb030
c6183f2cdb54
4c134d61c926
5749fb66c3d1
13e07d03063e
040ee0f80155
4cb59f912c4c
fa9c89adee64
(.venv) ➜  Cascade python src/main.py            
The lease 'worker-07-lease' has been terminated.
Remove it and reserve a new one? [Y/n] Y
2026-09-23 14:00:18.759 | INFO     | chi.expeca:remove_lease:160 - Removing worker-07-lease res
ervation with id bf2bbae0-4581-41f8-896f-741fe573b5c2.
2026-09-23 14:00:19.098 | INFO     | chi.expeca:wait_until_lease_status:138 - waiting 120 secon
ds for worker-07-lease with id bf2bbae0-4581-41f8-896f-741fe573b5c2 to become "None"
2026-09-23 14:00:24.176 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
ease with id bf2bbae0-4581-41f8-896f-741fe573b5c2 is None.
2026-09-23 14:00:24.176 | SUCCESS  | chi.expeca:try_to_remove:171 - done
2026-09-23 14:00:24.176 | INFO     | chi.expeca:reserve:243 - reserving worker-07
2026-09-23 14:00:26.612 | INFO     | chi.expeca:wait_until_lease_status:138 - waiting 120 secon
ds for worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde to become "ACTIVE"
2026-09-23 14:00:31.660 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:00:36.730 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:00:41.807 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:00:46.882 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:00:52.106 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:00:57.175 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:01:02.273 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:01:07.341 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-lease with id 6e7313f7-a1b9-4747-b47d-14ca8579fbde is PENDING.
2026-09-23 14:01:12.395 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:17.496 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:22.680 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:27.759 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:32.846 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:37.973 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:43.139 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:48.270 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:53.342 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:01:58.491 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:03.576 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:08.658 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:13.741 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:18.821 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:23.876 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:28.948 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:28.948 | WARNING  | chi.expeca:try_to_create_lease:290 - worker-07 reservation
de is stuck in pending.
2026-09-23 14:02:28.948 | INFO     | chi.expeca:remove_lease:160 - Removing worker-07-lease res
2026-09-23 14:02:30.338 | INFO     | chi.expeca:wait_until_lease_status:138 - waiting 120 secon
2026-09-23 14:02:35.499 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:35.499 | SUCCESS  | chi.expeca:try_to_remove:171 - done
2026-09-23 14:02:35.499 | INFO     | chi.expeca:reserve:304 - retrying to reserve worker-07. 2 
2026-09-23 14:02:35.500 | INFO     | chi.expeca:reserve:305 - waiting 5 seconds for worker-07 t
2026-09-23 14:02:42.979 | INFO     | chi.expeca:wait_until_lease_status:138 - waiting 120 secon
2026-09-23 14:02:48.056 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
2026-09-23 14:02:53.122 | INFO     | chi.expeca:wait_until_lease_status:145 - lease worker-07-l
^CTraceback (most recent call last):
  File "/home/martin/Projects/disco/Cascade/src/main.py", line 70, in <module>
    cluster.run()
  File "/home/martin/Projects/disco/Cascade/src/cluster.py", line 205, in run
    self.backend.setup()
  File "/home/martin/Projects/disco/Cascade/src/backends/expeca.py", line 119, in setup
    lease = reserve(node)
  File "/home/martin/Projects/disco/Cascade/src/backends/expeca.py", line 93, in reserve
    return chi.expeca.reserve({
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/chi/expeca.py", 
line 297, in reserve
    answer = try_to_create_lease()
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/chi/expeca.py", 
line 284, in try_to_create_lease
    wait_until_lease_status(leaseid, leasename, "ACTIVE")
  File "/home/martin/Projects/disco/Cascade/.venv/lib/python3.10/site-packages/chi/expeca.py", 
line 143, in wait_until_lease_status
    time.sleep(LEASE_STATUS_CHECK_PERIOD_SEC)
KeyboardInterrupt

(.venv) ➜  Cascade 
