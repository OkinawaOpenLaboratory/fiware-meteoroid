# Logs Overview

In this section, introduce to you how to confirm the Meteoroid logs and the OpenWhisk logs.

## Meteoroid logs

The Meteoroid is outputting logs using Django logs.

[settings.py](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/blob/master/meteoroid/meteoroid/settings.py)

### How to show Meteoroid logs

You can confirm all Meteoroid logs using Docker command if you installed the Meteoroid using docker-compose.

#### Show Docker processes

```bash
docker ps
```

Output:

```
CONTAINER ID        IMAGE                     COMMAND                  CREATED             STATUS              PORTS                    NAMES
d431c95deb9a        meteoroid/core:0.2.0      "python meteoroid/ma…"   6 days ago          Up 27 minutes       0.0.0.0:3000->3000/tcp   docker_meteoroid_1
c44a1c67856c        fiware/orion              "/usr/bin/contextBro…"   6 days ago          Up 27 minutes       0.0.0.0:1026->1026/tcp   docker_orion_1
609467e698f8        mongo:3.6                 "docker-entrypoint.s…"   6 days ago          Up 27 minutes       27017/tcp                docker_mongo_1
775de6847a7a        openwhisk/alarmprovider   "/bin/bash -c 'node …"   3 weeks ago         Up 27 minutes       8080/tcp                 docker_alarmprovider_1
```

#### Show Meteoroid logs

Specify **CONTAINER ID** of Meteoroid container.

```bash
docker logs d431c95deb9a
```


### Log level

#### INFO

You can confirm the log INFO in the following directory of the Meteoroid container.

```
/var/log/meteoroid/meteoroid.log
```

#### ERROR

You can confirm the log ERROR in the following directory of the Meteoroid container.

```
/var/log/meteoroid/error.log
```

## OpenWhisk logs

### Show Docker processes

You can confirm all OpenWhisk logs using Docker command if you installed the OpenWhisk using docker-compose.

```bash
docker ps
```

Output:

```
1e9dc802a4c6        openwhisk/apigateway:nightly               "/usr/bin/dumb-init …"   18 minutes ago       Up 7 minutes                 0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp, 0.0.0.0:9000->9000/tcp, 8423/tcp, 0.0.0.0:9090->8080/tcp   openwhisk_apigateway_1
26777dae7c3b        openwhisk/controller:nightly               "/bin/sh -c 'exec /i…"   18 minutes ago       Up 7 minutes                 0.0.0.0:2551->2551/tcp, 0.0.0.0:8888->8888/tcp, 0.0.0.0:9222->9222/tcp, 8080/tcp                     openwhisk_controller_1
fda1920fb433        openwhisk/invoker:nightly                  "/bin/sh -c 'exec /i…"   18 minutes ago       Up 7 minutes                 8080/tcp, 0.0.0.0:8085->8085/tcp, 0.0.0.0:9333->9222/tcp                                             openwhisk_invoker_1
...
```

### Show the apigateway logs

Specify **CONTAINER ID** of apigateway container.

```
docker logs 1e9dc802a4c6
```

### Show the logs in other containers

Login to the container by specifying **CONTAINER ID** of each container because you can not obtain **openwhisk/controller** and **openwhisk/invoker** logs using **docker logs** command.

```
docker exec -it CONTAINER_ID  /bin/sh
```

Open the following file.

#### openwhisk/controller

```
/logs/controller-local_logs.log
```

#### openwhisk/invoker

```
/logs/invoker-local_logs.log
```

