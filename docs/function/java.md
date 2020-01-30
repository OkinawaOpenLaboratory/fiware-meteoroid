# Using Java language
[The process of creating Java function depends on OpenWhisk.](https://github.com/apache/openwhisk/blob/master/docs/actions-java.md)
You must use JDK8 in order to compile.

You must write main method that has the exact signature as follows.

```java
public static JsonObject main(JsonObject args)
```

Import the following package called [google-gson](https://github.com/google/gson).

```java
import com.google.gson.JsonObject;
```

Create a java file called Hello.java

```java
import com.google.gson.JsonObject;

public class Hello {
    public static JsonObject main(JsonObject args) {
        String name = "stranger";
        if (args.has("name"))
            name = args.getAsJsonPrimitive("name").getAsString();
        JsonObject response = new JsonObject();
        response.addProperty("greeting", "Hello " + name + "!");
        return response;
    }
}
```

Compile a Hello.java into a JAR file called hello.jar.
[google-gson](https://github.com/google/gson) must exist in your Java CLASSPATH when compiling the Java file.

```bash
javac Hello.java
```

```bash
jar cvf hello.jar Hello.class
```

Create a function called function1.
You need to specify the name of the main class using --main.

```bash
meteoroid function create function1 hello.jar --language java --main Hello
```
