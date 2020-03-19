# Install Meteoroid

## Requirements

The following environment can run Meteoroid with FIWRRE(orion) like [Getting Started](../getting_started.md). So you can easily start using Meteoroid in your machine.

### Hardware

| Hardware | CPU | Memory | HardDisk |
| -- | -- | -- | -- |
| MacBook Pro | Intel Core i5 | 8GB | 500GB |

### Software

| Docker version  | Docker Compose version |
| -- | -- |
| 19.03.4 | 1.16.1 |

## Download

```bash
git clone https://github.com/OkinawaOpenLaboratory/fiware-meteoroid.git --recursive && cd fiware-meteoroid/
```

## Install

OpenWhisk must be running to build Meteoroid.

### Install OpenWhisk

```bash
cd fiware-meteoroid/docker/openwhisk-devtools/docker-compose
make quick-start

```

### Install [Meteoroid CLI](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid-cli)

```bash
pip install meteoroid-cli
```

### Install Meteoroid

You can install Meteoroid in two ways:

- [Automatic installation](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/tree/master#automatic-installation) using Docker (Docker Compose)
- [Manual installation](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/tree/master#manual-installation) using pipenv and Django manage.py

---

## Automatic installation
using Docker (Docker Compose)

```bash
cd fiware-meteoroid/docker/
docker-compose up -d
```

### Export METEOROID_SCHEMA_ENDPOINT for CLI (Option)
Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```

---

## Manual installation
using pipenv and Django manage.py

```
pipenv shell
pipenv install
```

### Migrate database

```
python manage.py migrate
```

### Run meteoroid

```bash
python manage.py runserver
```

### Export METEOROID_SCHEMA_ENDPOINT (Option) for CLI
Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```
