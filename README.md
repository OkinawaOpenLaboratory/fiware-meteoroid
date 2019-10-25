# Meteoroid

## Overview
Meteoroid realizes integrating Function as a Service(FaaS) capabilities in FIWARE.
It provides a management interface specialized for FaaS and FIWARE.


## Requirements
Python 3.8+
Django 2.2.6+
Django Rest Framework 3.10.3+


## Usage

### Start pipenv and Install requirements

```
pipenv shell
pipenv install
```


### Migrate database

```
python manage.py migrate
```

### Run meteoroid

```
python manage.py runserver
```

### Running with Docker Compose


```bash
cd docker

sudo docker-compose up
```
