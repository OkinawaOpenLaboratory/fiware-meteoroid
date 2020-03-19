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
