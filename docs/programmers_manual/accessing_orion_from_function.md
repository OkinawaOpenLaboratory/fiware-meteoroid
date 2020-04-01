# Accessing Orion from Function

You can access context data of Orion Context Broker from within the Meteoroid Function.

- [Python](#python)
- [Java](#java)

## Python

### Create new entity

You can create a new entity to Orion as follows:

```python
import json
import requests

def main(params):
    url = 'http://orion:1026/v2/entities'
    headers = {'content-type': 'application/json'}
    payload = {
        'id': 'Room1',
        'type': 'Room',
        'temperature': {
            'value': 23,
            'type': 'Float'
        }
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    status_code = response.status_code
    return {'status_code': status_code}
```

### Read entity

You can get the temperature attribute of Room1 entity from Orion as follows:

```python
import requests

def main(params):
    url = 'http://orion:1026/v2/entities/Room1'
    response = requests.get(url)
    data = response.json()

    return {'temperature': data['temperature']}
```

### Update Entity

You can update the temperature attribute of Room1 entity as follows:

```python
import requests

def main(params):
    url = 'http://orion:1026/v2/entities/Room1/attrs/temperature/value'
    headers = {'content-type': 'text/plain'}
    update_value = 20
    response = requests.put(url, data=str(update_value), headers=headers)

    return {"status_code": response.status_code}
```

## Java

### Create new entity

You can create new entity to Orion as follows:

```java
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import okhttp3.*;

import java.io.IOException;

public class MainPOST {
    public static final MediaType JSON = MediaType.get("application/json; charset=utf-8");
    public static final String ORION_BASE_URL = "http://orion:1026";
    public static JsonObject main(JsonObject args) {
        OkHttpClient client = new OkHttpClient();
        String entityJsonString = "{" +
                "    \"id\": \"Room1\"," +
                "    \"type\": \"Room\"," +
                "    \"temperature\": {" +
                "        \"value\": 23," +
                "        \"type\": \"Float\"" +
                "    }" +
                "}";
        RequestBody body = RequestBody.create(entityJsonString, JSON);
        Request request = new Request.Builder()
                .url(String.format("%s/v2/entities", ORION_BASE_URL))
                .post(body)
                .build();
        JsonObject responseJsonObject = new JsonObject();
        try {
            Response response = client.newCall(request).execute();
            responseJsonObject.addProperty("status_code", response.code());
        } catch (IOException e) {
            e.printStackTrace();
            responseJsonObject.addProperty("error", e.toString());
        }
        return responseJsonObject;
    }
}
```

### Read entity

You can get the temperature attribute of Room1 entity from Orion as follows:

```java
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import okhttp3.*;

import java.io.IOException;

public class MainGET {
    public static final String ORION_BASE_URL = "http://orion:1026";
    public static JsonObject main(JsonObject args) {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url(String.format("%s/v2/entities/Room1", ORION_BASE_URL))
                .get()
                .build();
        JsonObject responseJsonObject = new JsonObject();
        try {
            Response response = client.newCall(request).execute();
            String json = response.body().string();
            JsonObject jsonObject = new Gson().fromJson(json, JsonObject.class);
            responseJsonObject.add("temperature", jsonObject.get("temperature"));
        } catch (IOException e) {
            responseJsonObject.addProperty("error", e.toString());
            e.printStackTrace();
        }
        return responseJsonObject;
    }
}

```

### Update Entity

You can update the temperature attribute of Room1 entity as follows:

```java
import com.google.gson.JsonObject;
import okhttp3.*;

import java.io.IOException;

public class MainPUT {
    public static final MediaType TEXT = MediaType.get("text/plain; charset=utf-8");
    public static final String ORION_BASE_URL = "http://orion:1026";
    public static JsonObject main(JsonObject args) {
        OkHttpClient client = new OkHttpClient();
        String value = "20";
        RequestBody body = RequestBody.create(value, TEXT);
        Request request = new Request.Builder()
                .url(String.format("%s/v2/entities/Room1/attrs/temperature/value", ORION_BASE_URL))
                .put(body)
                .build();
        JsonObject responseJsonObject = new JsonObject();
        try {
            Response response = client.newCall(request).execute();
            responseJsonObject.addProperty("status_code", response.code());
        } catch (IOException e) {
            e.printStackTrace();
            responseJsonObject.addProperty("error", e.toString());
        }
        return responseJsonObject;
    }
}
```
