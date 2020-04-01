#Features

The function that Meteoroid executes is called `Function`. The application developer registers Function from the dedicated command line tool. Meteoroid provides two ways to trigger a Function to meet the commonly used needs of IoT systems.

1. Event-driven execution
Event-driven execution is the execution of a specific function in response to an event change.
Meteoroid can generate a RESTful API linked to a Function called `Endpoint` to call the Function. By linking with the IoT platform (FIWARE), functions can be executed in an event-driven manner in response to changes in context information. In order to link with FIWARE, define `Subscription` and link the context information with the endpoint.


2. Periodic execution
Periodic execution refers to executing a Function at a preset time or cycle.
To implement the regular execution process in Meteoroid, define `Schedule` using UNIX crontab syntax.
