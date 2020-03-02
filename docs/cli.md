# Meteoroid CLI

![PyPI](https://img.shields.io/pypi/v/meteoroid-cli)
![GitHub](https://img.shields.io/github/license/OkinawaOpenLaboratory/fiware-meteoroid-cli?color=blue)

## Overview
Meteoroid CLI is a command-line-interface for Meteoroid that
integrating Function as a Service(FaaS) capabilities in FIWARE.

## Requirements
Python 3.8+
cliff  2.16.0+
pbr    5.4.3+


## Usage

### Install meteoroid cli

```
pip install meteoroid-cli
```

### Export METEOROID_SCHEMA_ENDPOINT (Option)

Defualt endpoint (http://localhost:3000/schema/?format=corejson)

```
export METEOROID_SCHEMA_ENDPOINT=http://host:port/schema/?format=corejson
```

### Example of use

```
$ meteoroid result show 22
+---------------+------------------+
| Field         | Value            |
+---------------+------------------+
| id            | 22               |
| response      | test_response    |
| logs          | test_logs        |
| FiwareService | None             |
| functionId    | test_function_id |
+---------------+------------------+
```

## Commands

### Funciton

| command | description |
----|----
| function show   | Show a function |
| function list   | Show function list |
| function create | Create a function |
| function update | Update a function |
| function delete | Delete a function |

### Endpoint

| command | description |
----|----
| endpoint show | Show a endpoint |
| endpoint list | Show endpoint list |
| endpoint create | Create endpoint |
| endpoint delete | Delete endpoint |

### Description

| command | description |
----|----
| subscription show | Show a subscription |
| subscription list | Show subscription list |
| subscription create | Create subscription |
| subscription delete | Delete subscription |

### Result

| command | description |
----|----
| result list | Show result list |
| result show | Show a result |

### Schedule

| command | description |
----|----
| schedule show | Show a schedule |
| schedule list | Show schedule list |
| schedule create | Create schedule |
| schedule delete | Delete schedule |

## How to use meteoroid

[Meteoroid README](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid/blob/master/README.md)
