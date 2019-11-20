# Install Meteoroid using Docker Compose

## Download Meteoroid

```bash
git clone https://github.com/OkinawaOpenLaboratory/fiware-meteoroid.git --recursive
```

Set `METEOROID_HOME`

```bash
cd fiware-meteoroid/
METEOROID_HOME=`pwd`
```

## Install OpenWhisk

```bash
cd ${METEOROID_HOME}/docker/openwhisk-devtools/docker-compose
make quick-start
```

## Install Meteodoid, Orion, MongoDB

Please edit DOCKER_HOST_IP for Meteoroid to access OpenWhisk.

```bash
cd ${METEOROID_HOME}/docker
vim docker-compose.yml
```

You should two changes Meteoroid Service and Migration Service.

```yaml
    environment:
      - OPEN_WHISK_HOST=<DOCKER_HOST_IP>
```

Run containers.

```
docker-compose up -d
```
