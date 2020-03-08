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
pip install pyms[all]
```
* Installing minimun dependencies
```
pip install pyms
```
* Installing request dependencies
```
pip install pyms[request]
```
* Installing swagger dependencies
```
pip install pyms[swagger]
```
* Installing metrics dependencies
```
pip install pyms[metrics]
```
* Installing trace dependencies
```
pip install pyms[trace]
```

See [Quickstart](quickstart.md) to continue with this tutorial