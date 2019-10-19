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

### Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t meteoroid .

# starting up a container
docker run -p 8000:8000 meteoroid
``
