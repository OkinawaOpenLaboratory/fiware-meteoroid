# Using third party packages

You can use third party packages within each programming language.

- [Python](#python)
- [Java](#java)

## Python

Create the following script with the file name `__main__.py`.

```python
import pytz

def main(params):
    return {'version': pytz.__version__}
```

Create a virtualenv as follows:

```plain
docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash   -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
```

Create a zip file containing the virtualenv directory and `__main__.py`.

```plain
zip -r custom.zip virtualenv __main__.py
```

Upload the zip file and create a function.

```plain
meteoroid function create function1 custom.zip -l python:3 --main main
```

## Java

Add the shadow plugin to build.gradle.

```plain
plugins {
    id 'java'
    id 'com.github.johnrengelman.shadow' version '5.0.0'//Add shadow plugin
}

group 'org.example'
version '1.0'

sourceCompatibility = 1.8

repositories {
    mavenCentral()
}

dependencies {
    implementation group: 'com.google.code.gson', name: 'gson', version: '2.7'
    implementation group: 'com.squareup.okhttp3', name: 'okhttp', version: '4.3.1'
}
```

Create the following script with the file name `Main.java` in your project.

```java
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import okhttp3.*;

import java.io.IOException;

public class Main {
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

Create a **fat jar**(Jar including dependent libraries) using the shadow plugin.

The jar file is created under `build/libs` .

```plain
gradle shadowJar
```

Upload the jar file and create a function.

```plain
meteoroid function create function1 build/libs/project-1.0-all.jar --main Main
```
