# Using Function Parameters

## Receiving parameters in Function

Function can receive parameters and use them.

- [Python](#python)
- [Java](#java)

### Python

You can receive parameters from main function arguments (params).
The type of params is a dictionary.

```python
def main(params):
    name = params.get('name', 'stranger')
    age = params.get('age', 0)
    return params
```

### Java

You can receive parameters from main function arguments (params).
The type of params is *com.google.gson.JsonObject*.

```java
import com.google.gson.JsonObject;

public class Main {
    public static JsonObject main(JsonObject params) {
        String name = "stranger";
        int age = 0;
        if(params.has("name")) {
           name = params.getAsJsonPrimitive("name").getAsString();
        }
        if(params.has("age")) {
           age = params.getAsJsonPrimitive("age").getAsInt();
        }
        return params;
    }
}
```

## Pass parameters to Function

There are two ways to pass parameters to Function.

1. Pass when creating Function via Meteoroid CLI
2. Pass when calling Function via RESTful API

### 1. Pass when creating Function via Meteoroid CLI

When creating a Function, you can pass parameters to the Function by using the `-p` option.
This method is suitable for parameters that do not change dynamically with each request.

```bash
meteoroid function create function1 function1.py -p name FIWARE -p age 23
```

### 2. Pass when calling Function via RESTful API

Parameters can be specified even if they are not defined when creating a Function.
Also, the parameters specified when creating the Function can be updated.

When using cURL, you can pass parameters as follows:

```bash
curl -X POST http://192.168.29.56:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/endpoint1/function1 \
    -d timeout=60 \
    -d age=21
```
