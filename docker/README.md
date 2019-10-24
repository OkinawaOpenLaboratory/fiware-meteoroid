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

```bash
cd ${METEOROID_HOME}/docker
docker-compose up -d
```
