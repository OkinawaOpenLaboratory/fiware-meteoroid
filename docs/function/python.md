# Using Python language
[The process of creating Python function depends on OpenWhisk.](https://github.com/apache/openwhisk/blob/master/docs/actions-python.md)


Python function is top-level function called main, create a file called hello.py.

```python
def main(args):
    name = args.get("name", "stranger")
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"greeting": greeting}
```


Create a function.

```bash
meteoroid fucntion create function1 hello.py
```

if you want to use other entry method, must specify the method name using --main.
