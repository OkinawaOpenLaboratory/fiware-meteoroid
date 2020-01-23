# Meteoroid Contribution Guide

This document describes the guidelines to Meteoroid. If you are planning to contribute to the code you should read this document and get familiar with its content.


## General principles

* Meteoroid programming language is Python.
* Using [Django](https://www.djangoproject.com/) and [restframework](https://www.django-rest-framework.org/).
* Using [OpenWhisk](https://openwhisk.apache.org/) as a FaaS platform.
* Code contributed to Meteoroid must follow the [code style guidelines](#code-style-guidelines) in order to set a common programming style for all developers working on the code.


## Pull Request protocol

Coming soon

## Code style guidelines

Meteoroid complaints to [PEP8](https://www.python.org/dev/peps/pep-0008/).
Lint is the [flake8](https://pypi.org/project/flake8/) and plugins that depend on flake8.
Using following plugins that depend on flake8.

* [flake8-import-order](https://github.com/PyCQA/flake8-import-order)
* [flake8-quotes](https://github.com/zheller/flake8-quotes)
* [pep8-naming](https://github.com/PyCQA/pep8-naming)
* [flake8-print](https://github.com/JBKahn/flake8-print)
* [flake8-eradicate](https://github.com/sobolevn/flake8-eradicate)

This project is setting following config of flake8.

```
max-complexity = 10
max-line-length = 100
```
