# Meteoroid CLI Overview

Command-line interface to the Meteoroid APIs (meteoroid CLI Version: 1.0.0)

```plain
meteoroid -h
usage: meteoroid [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

Meteoroid command line tool

optional arguments:
  --version            show program's version number and exit
  -v, --verbose        Increase verbosity of output. Can be repeated.
  -q, --quiet          Suppress output except warnings and errors.
  --log-file LOG_FILE  Specify a file to log output. Disabled by default.
  -h, --help           Show help message and exit.
  --debug              Show tracebacks on errors.

Commands:
  complete       print bash completion command (cliff)
  endpoint create  Create endpoint
  endpoint delete  Delete endpoint
  endpoint list  Show endpoint list
  endpoint show  Show a endpoint
  function create  Create a function
  function delete  Delete a function
  function list  Show function list
  function show  Show a function
  function update  Update a function
  help           print detailed help for another command (cliff)
  result list    Show result list
  result show    Show a result
  schedule create  Create schedule
  schedule delete  Delete schedule
  schedule list  Show schedule list
  schedule show  Show a schedule
  subscription create  Create subscription
  subscription delete  Delete subscription
  subscription list  Show subscription list
  subscription show  Show a subscription
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --version                             | Show program's version number and exit |
| -v, --verbose, --debug                | Increase verbosity of output and show tracebacks on errors. You can repeat this option. |
| -q, -quiet                            | Suppress output except warnings and errors. |
| --log-file LOG_FILE                   | Specify a file to log output. Disabled by default. |
| -h, --help                            | Show help message and exit. |

# Meteoroid CLI Commands

### endpoint create

Create an endpoint.

```plain
meteoroid endpoint create                 
usage: meteoroid endpoint create [-h] [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH]
                                 name path method function_id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| name                                  | Name of endpoint to be created. |
| path                                  | Path for calling Endpoint. Path must begin with '/'. |
| method                                | HTTP Method for calling the endpoint. |
| function_id                           | Function ID associated with Endpoint. |

#### Usage example

```plain
meteoroid endpoint create endpoint1 /function1 post 1
+---------------------+--------------------------------------------------------------------------------------+
| Field               | Value                                                                                |
+---------------------+--------------------------------------------------------------------------------------+
| id                  | 1                                                                                    |
| url                 | http://192.168.0.1:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/endpoint2/function9 |
| fiware_service      |                                                                                      |
| fiware_service_path | /                                                                                    |
| name                | endpoint1                                                                            |
| path                | /function1                                                                           |
| method              | post                                                                                 |
| function            | 1                                                                                    |
+---------------------+--------------------------------------------------------------------------------------+
```

### endpoint delete

Delete an endpoint.

```plain
meteoroid endpoint delete
usage: meteoroid endpoint delete [-h] [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH] id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Endpoint ID. |

#### Usage example

```plain
meteoroid endpoint delete 1
Success delete endpoint
```

### endpoint list

List endpoints.

```plain
meteoroid endpoint list
```

#### Usage example

```plain
meteoroid endpoint list
+----+----------------------------------------------------------------------------------+----------------+---------------------+-----------+--------+--------+----------+
| id | url                                                                              | fiware_service | fiware_service_path | name      | path   | method | function |
+----+----------------------------------------------------------------------------------+----------------+---------------------+-----------+--------+--------+----------+
|  1 | http://192.168.0.1:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/endpoint1/hello |                | /                   | endpoint1 | /hello | post   |        1 |
+----+----------------------------------------------------------------------------------+----------------+---------------------+-----------+--------+--------+----------+
```

### endpoint show

Show an endpoint.

```plain
meteoroid endpoint show
usage: meteoroid endpoint show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [--fiwareservice FIWARESERVICE]
                               [--fiwareservicepath FIWARESERVICEPATH]
                               id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| -l LANG:VERSION                       | The type of programming language and version. |
| -m MAIN_FILE_NAME                     | Main entrypoint of the action code. |
| -p KEY VALUE                          | Parameters that can be referenced inside the function. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Endpoint ID. |

#### Usage example

```plain
meteoroid endpoint show 1
+---------------------+----------------------------------------------------------------------------------+
| Field               | Value                                                                            |
+---------------------+----------------------------------------------------------------------------------+
| id                  | 1                                                                                |
| url                 | http://192.168.0.1:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/endpoint1/hello |
| fiware_service      |                                                                                  |
| fiware_service_path | /                                                                                |
| name                | endpoint1                                                                        |
| path                | /function1                                                                       |
| method              | post                                                                             |
| function            | 1                                                                                |
+---------------------+----------------------------------------------------------------------------------+
```

### function create

Create a function.

```plain
meteoroid function create
usage: meteoroid function create [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [-l LANG:VERSION] [-m MAIN_FILE_NAME] [-p KEY VALUE]
                                 [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH]
                                 name file
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| -l LANG:VERSION                       | The type of programming language and version. |
| -m MAIN_FILE_NAME                     | Main entrypoint of the action code. |
| -p KEY VALUE                          | Parameters that can be referenced inside the function. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| name                                  | Name of endpoint to be created. |
| file                                  | Whether the action has a binary attachment or not. This attribute is ignored when creating or updating an action. |

#### Usage example

```plain
meteoroid function create -l python:3 function1 function1.py -p name Meteoroid
+---------------------+-------------------------------------------+
| Field               | Value                                     |
+---------------------+-------------------------------------------+
| id                  | 1                                         |
| code                | def main(params):                         |
|                     |     name = params.get("name", "stranger") |
|                     |     print(name)                           |
|                     |     return {"Hello": name}                |
|                     |                                           |
| language            | python:3                                  |
| binary              | False                                     |
| main                |                                           |
| version             | 0.0.1                                     |
| parameters          | [{'key': 'name', 'value': 'Meteoroid'}]   |
| fiware_service      |                                           |
| fiware_service_path | /                                         |
| name                | function1                                 |
+---------------------+-------------------------------------------+
```

### function delete

Delete a function.

```plain
meteoroid function delete
usage: meteoroid function delete [-h] [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH] id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Function ID |

#### Usage example

```plain
meteoroid function delete 1
Success delete function
```

### function list

List functions.

```plain
meteoroid function list
```

#### Usage example

```plain
meteoroid function list
+----+------+----------+--------+------+---------+------------+----------------+---------------------+-----------+
| id | code | language | binary | main | version | parameters | fiware_service | fiware_service_path | name      |
+----+------+----------+--------+------+---------+------------+----------------+---------------------+-----------+
|  1 |      | python:3 | False  |      | 0.0.1   |            |                | /                   | function1 |
+----+------+----------+--------+------+---------+------------+----------------+---------------------+-----------+
```

### function show

Show a function.

```plain
meteoroid function show
usage: meteoroid function show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [-co] [--fiwareservice FIWARESERVICE]
                               [--fiwareservicepath FIWARESERVICEPATH]
                               id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| -co                                   | Specify when retrieve the code of function from OpenWhisk. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Function ID. |


#### Usage example

```plain
meteoroid function show 1
+---------------------+-----------------------------------------+
| Field               | Value                                   |
+---------------------+-----------------------------------------+
| id                  | 4                                       |
| code                |                                         |
| language            | python:3                                |
| binary              | False                                   |
| main                |                                         |
| version             | 0.0.1                                   |
| parameters          | [{'key': 'name', 'value': 'Meteoroid'}] |
| fiware_service      |                                         |
| fiware_service_path | /                                       |
| name                | function1                               |
+---------------------+-----------------------------------------+
```

### function update

```plain
meteoroid function update
usage: meteoroid function update [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [-l LANG:VERSION] [-m MAIN_FILE_NAME] [-p KEY VALUE KEY VALUE]
                                 [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH]
                                 id file
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| -l LANG:VERSION                       | The type of programming language and version. |
| -m MAIN_FILE_NAME                     | Main entrypoint of the action code. |
| -p KEY VALUE                          | Parameters that can be referenced inside the function. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Function ID. |
| file                                  | Whether the action has a binary attachment or not. This attribute is ignored when creating or updating an action. |

#### Usage example

```plain
meteoroid function update 4 function1.py -p name FIWARE
+---------------------+-------------------------------------------+
| Field               | Value                                     |
+---------------------+-------------------------------------------+
| id                  | 4                                         |
| code                | def main(params):                         |
|                     |     name = params.get("name", "stranger") |
|                     |     print(name)                           |
|                     |     return {"Hello": name}                |
|                     |                                           |
| language            | python:default                            |
| binary              | False                                     |
| main                |                                           |
| version             | 0.0.2                                     |
| parameters          | [{'key': 'name', 'value': 'FIWARE'}]      |
| fiware_service      |                                           |
| fiware_service_path | /                                         |
| name                | function1                                 |
+---------------------+-------------------------------------------+
```

### result list

List function execution results

```plain
meteoroid result list
```

#### Usage example

```plain
meteoroid result list
+----------------------------------+-----------+-----------+----------+---------------+---------------+---------+-------------+---------+
| activation_id                    | name      | namespace | duration | start         | end           | publish | status_code | version |
+----------------------------------+-----------+-----------+----------+---------------+---------------+---------+-------------+---------+
| cc4d4442b8ae41d18d4442b8ae41d10f | function1 | guest     |      421 | 1582102627912 | 1582102628333 | False   |           0 | 0.0.1   |
| 005bf6c7c6b14aba9bf6c7c6b1aaba3d | hello     | guest     |      226 | 1582069092448 | 1582069092674 | False   |           0 | 0.0.2   |
| aa30e19f3bd543c9b0e19f3bd5d3c9e1 | hello     | guest     |      238 | 1582069086757 | 1582069086995 | False   |           0 | 0.0.1   |
+----------------------------------+-----------+-----------+----------+---------------+---------------+---------+-------------+---------+
```

### result show

Show a function execution result

```plain
meteoroid result show
usage: meteoroid result show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [--annotations] [--fiwareservice FIWARESERVICE]
                             [--fiwareservicepath FIWARESERVICEPATH]
                             id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Activation ID of OpenWhisk. |

#### Usage example

```plain
meteoroid result show cc4d4442b8ae41d18d4442b8ae41d10f
+---------------+--------------------------------------------------------------------------------------------------------------------+
| Field         | Value                                                                                                              |
+---------------+--------------------------------------------------------------------------------------------------------------------+
| activation_id | cc4d4442b8ae41d18d4442b8ae41d10f                                                                                   |
| name          | function1                                                                                                          |
| namespace     | guest                                                                                                              |
| duration      | 421                                                                                                                |
| start         | 1582102627912                                                                                                      |
| end           | 1582102628333                                                                                                      |
| publish       | False                                                                                                              |
| status_code   | 0                                                                                                                  |
| version       | 0.0.1                                                                                                              |
| logs          | []                                                                                                                 |
| response      | OrderedDict([('result', OrderedDict([('test', 'test')])), ('size', 16), ('status', 'success'), ('success', True)]) |
+---------------+--------------------------------------------------------------------------------------------------------------------+
```

### schedule create

Create a schedule.

```plain
meteoroid schedule create
usage: meteoroid schedule create [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [-s STARTDATE] [-e STOPDATE] [-p TRIGGER_PAYLOAD]
                                 [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH]
                                 name schedule function
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| -s STARTDATE                          | The date when the first trigger will be fired. Subsequent fires will occur based on the interval length specified by the minutes parameter. |
| -e STOPDATE                           | The date when the Trigger will stop running. Triggers will no longer be fired once this date has been reached. |
| -p TRIGGER_PAYLOAD                    | The value of this parameter becomes the content of the Trigger every time the Trigger is fired. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| name                                  | Name of schedule to be created. |
| schedule                              | A string, based on the UNIX crontab syntax that indicates when to fire the Trigger in Coordinated Universal Time (UTC). The string is a sequence of five fields that are separated by spaces: X X X X X. For more information, see: http://crontab.org. The following strings are examples that use varying duration's of frequency. This specification depends on `OpenWhisk Alarm Package.` Please see [OpenWhisk Alarm Package](https://github.com/apache/openwhisk-package-alarms#firing-a-trigger-on-a-time-based-schedule-using-cron) for the detail. |
| function                              | Function ID associated with Schedule. |

#### Usage example1

```plain
meteoroid schedule create schedule1 '*/20 * * * *' 4
+-----------------+--------------+
| Field           | Value        |
+-----------------+--------------+
| name            | schedule1    |
| schedule        | */20 * * * * |
| function        | 4            |
| trigger_payload |              |
| startDate       |              |
| stopDate        |              |
| id              | 1            |
+-----------------+--------------+
```

#### Usage example2

```plain
meteoroid schedule create schedule1 '*/20 * * * *' 4 -e '2021-03-31T23:59:00.000Z' -p '{"name":"Meteoroid"}'
+-----------------+--------------------------------------+
| Field           | Value                                |
+-----------------+--------------------------------------+
| name            | schedule1                            |
| schedule        | */20 * * * *                         |
| function        | 1                                    |
| trigger_payload | OrderedDict([('name', 'Meteoroid')]) |
| startDate       |                                      |
| stopDate        | 2021-03-31T23:59:00.000Z             |
| id              | 1                                    |
+-----------------+--------------------------------------+
```

### schedule delete

Delete a schedule.

```plain
meteoroid schedule delete
usage: meteoroid schedule delete [-h] [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH] id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Schedule ID |

#### Usage example

```plain
meteoroid schedule delete 1
Success delete schedule
```

### schedule list

List schedules.

```plain
meteoroid schedule list
```

#### Usage example

```plain
meteoroid schedule list
+----+----------------+---------------------+-------------------+----------------+----------+-----------+
| id | fiware_service | fiware_service_path | trigger_name      | rule_name      | function | name      |
+----+----------------+---------------------+-------------------+----------------+----------+-----------+
|  1 |                | /                   | schedule1-trigger | schedule1-rule |        1 | schedule1 |
+----+----------------+---------------------+-------------------+----------------+----------+-----------+
```

### schedule show

Show a schedule.

```plain
meteoroid schedule show
usage: meteoroid schedule show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [--fiwareservice FIWARESERVICE]
                               [--fiwareservicepath FIWARESERVICEPATH]
                               id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Schedule ID. |

#### Usage example

```plain
$ meteoroid schedule show 3
+-----------------+--------------------------------------+
| Field           | Value                                |
+-----------------+--------------------------------------+
| schedule        | */20 * * * *                         |
| function        | 4                                    |
| id              | 3                                    |
| name            | schedule1                            |
| startDate       |                                      |
| stopDate        | 2021-03-31T23:59:00.000Z             |
| trigger_payload | OrderedDict([('name', 'Meteoroid')]) |
+-----------------+--------------------------------------+
```

### subscription create

Create a subscription.

```plain
meteoroid subscription create
usage: meteoroid subscription create [-h] [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH] endpoint_id orion_subscription
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| endpoint_id                           | Endpoint ID associated with Subscription. |
| orion_subscription                    | FIWARE Orion Subscription. Please refer to [Subscription](https://fiware-orion.readthedocs.io/en/master/user/walkthrough_apiv2/index.html#subscriptions) for how to write Subscription. Notification url is automatically generated by Meteoroid. |

#### Usage example

```plain
meteoroid subscription create 3 '
> {
>     "description": "test subscription",
>     "subject": {
>         "entities": [
>             {
>                 "id": "Room1",
>                 "type": "Room"
>             }
>         ]
>     },
>     "notification": {
>         "attrs": [
>             "temperature"
>         ]
>     },
>     "expires": "2040-01-01T14:00:00.00Z",
>     "throttling": 1
> }'
+-----------------------+--------------------------+
| Field                 | Value                    |
+-----------------------+--------------------------+
| id                    | 2                        |
| fiware_service        |                          |
| fiware_service_path   | /                        |
| endpoint_id           | 3                        |
| orion_subscription_id | 5e5f5d8e9c3996ddd2e1ee8c |
+-----------------------+--------------------------+
```

### subscription delete

Delete a subscription.

```plain
meteoroid subscription delete
usage: meteoroid subscription delete [-h] [--fiwareservice FIWARESERVICE] [--fiwareservicepath FIWARESERVICEPATH] id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Subscription ID. |

#### Usage example

```plain
meteoroid subscription delete 1
Success delete subscription
```

### subscription list

List subscriptions.

```plain
meteoroid subscription list
```

#### Usage example

```plain
meteoroid subscription list
+----+----------------+---------------------+-------------+--------------------------+
| id | fiware_service | fiware_service_path | endpoint_id | orion_subscription_id    |
+----+----------------+---------------------+-------------+--------------------------+
|  1 |                | /                   |           1 | 5e5f5d8e9c3996ddd2e1ee8c |
+----+----------------+---------------------+-------------+--------------------------+
```

### subscription show

Show a subscription.

```plain
meteoroid subscription show
usage: meteoroid subscription show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN] [--noindent] [--prefix PREFIX] [--max-width <integer>] [--fit-width] [--print-empty] [--fiwareservice FIWARESERVICE]
                                   [--fiwareservicepath FIWARESERVICEPATH]
                                   id
```

#### Parameters

| Parameter                             | Description |
| ------------------------------------- | -- |
| -f <FORMATTER>, --format <FORMATTER>  | the output format, defaults to table. |
| -c COLUMN, --column COLUMN            | specify the column(s) to include, can be repeated to show multiple columns. |
| --noindent                            | whether to disable indenting the JSON. |
| --prefix <PREFIX>                     | add a prefix to all variable names. |
| --max-width <integer>                 | Maximum display width, <1 to disable. You can also use the CLIFF_MAX_TERM_WIDTH environment variable, but the parameter takes precedence. |
| --fit-width                           | Fit the table to the display width. Implied if –max-width greater than 0. Set the environment variable CLIFF_FIT_WIDTH=1 to always enable. |
| --print-empty                         | Print empty table if there is no data to show. |
| --fiwareservice FIWARESERVICE         | FIWARE Service. |
| --fiwareservicepath FIWARESERVICEPATH | FIWARE Service Path. |
| id                                    | Subscription ID. |

#### Usage example

```plain
$ meteoroid subscription show 1
+-----------------------+--------------------------+
| Field                 | Value                    |
+-----------------------+--------------------------+
| id                    | 1                        |
| fiware_service        |                          |
| fiware_service_path   | /                        |
| endpoint_id           | 3                        |
| orion_subscription_id | 5e5f5d8e9c3996ddd2e1ee8c |
+-----------------------+--------------------------+
```


