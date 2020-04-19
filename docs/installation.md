# Installation

## Python Version
We recommend using the latest version of Python 3. PyMS supports Python 3.6 and newer and PyPy.

```
virtualenv --python=python[3.6|3.7|3.8] venv
source venv/bin/activate
```

## Install PyMS

**Installing pyms with all dependencies**
```
pip install py-ms[all]
```
* Installing minimun dependencies
```
pip install py-ms
```
* Installing request dependencies
```
pip install py-ms[request]
```
* Installing swagger dependencies
```
pip install py-ms[swagger]
```
* Installing metrics dependencies
```
pip install py-ms[metrics]
```
* Installing trace dependencies
```
pip install py-ms[trace]
```

See [Quickstart](quickstart.md) to continue with this tutorial