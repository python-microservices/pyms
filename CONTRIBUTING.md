# Contributing

## Branch workflow

**READ BEFORE CREATE A BRANCH OR OPEN A PR/MR**
- We use [Github Glow](https://guides.github.com/introduction/flow/)
  

## Commit Message Guidelines

- The messages of the commits use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- See [Angular guideline](https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines)


## Installation

After cloning this repo, create a [virtualenv](https://virtualenv.pypa.io/en/stable/) and ensure dependencies are installed by running:

```sh
virtualenv venv
source venv/bin/activate
pip install -e ".[test]"
```

Well-written tests and maintaining good test coverage is important to this project. While developing, run new and existing tests with:

```sh
pytest --cov=pyms --cov=tests tests/
```

Add the `-s` flag if you have introduced breakpoints into the code for debugging.
Add the `-v` ("verbose") flag to get more detailed test output. For even more detailed output, use `-vv`.
Check out the [pytest documentation](https://docs.pytest.org/en/latest/) for more options and test running controls.

PyMS supports several versions of Python3. To make sure that changes do not break compatibility with any of those versions, we use `tox` to create virtualenvs for each Python version and run tests with that version. To run against all Python versions defined in the `tox.ini` config file, just run:

```sh
tox
```

If you wish to run against a specific version defined in the `tox.ini` file:

```sh
tox -e py36
```

Tox can only use whatever versions of Python are installed on your system. When you create a pull request, Travis will also be running the same tests and report the results, so there is no need for potential contributors to try to install every single version of Python on their own system ahead of time.

## Pipenv

### Advantages over plain pip and requirements.txt
[Pipenv](https://pipenv.readthedocs.io/en/latest/) generates two files: a `Pipfile`and a `Pipfile.lock`.
* `Pipfile`: Is a high level declaration of the dependencies of your project. It can contain "dev" dependencies (usually test related stuff) and "standard" dependencies which are the ones you'll need for your project to function
* `Pipfile.lock`: Is the "list" of all the dependencies your Pipfile has installed, along with their version and their hashes. This prevents two things: Conflicts between dependencies and installing a malicious module.

### How to...

Here the most 'common' `pipenv` commands, for a more in-depth explanation please refer to  the [official documentation](https://pipenv.readthedocs.io/en/latest/).

#### Install pipenv
```bash
pip install pipenv
```

#### Install dependencies defined in a Pipfile
```bash
pipenv install
```

#### Install both dev and "standard" dependencies defined in a Pipfile
```bash
pipenv install --dev
```

#### Install a new module
```bash
pipenv install django
```

#### Install a new dev module (usually test related stuff)
```bash
pipenv install nose --dev
```

#### Install dependencies in production
```bash
pipenv install --deploy
```

#### Start a shell
```bash
pipenv shell
```

## Documentation

This project use MkDocs

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

### Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.

## Tutorial: Create your own service

* First, you must create a file with the name of your service inside of `pyms.flask.service`, for example, 
"myawesomesrv":

pyms/flask/services/myawesomesrv.py
```python
from pyms.flask.services.driver import DriverService


class Service(DriverService):
    service = "myawesomesrv"
    default_values = {
        "myvalue": 0,
        "myvalue2": 1
    }
```

* Now, you can configure your service from `config.yml`
```yaml
pyms:
  config:
    myawesomesrv:
      myvalue: 5
```

* Your service will be instanced inside the `ms` object in `flask.current_app` object. For example, with the last config,
you could print the folowing code:

```python
from flask import jsonify, current_app

from pyms.flask.app import Microservice

ms = Microservice(service="my-minimal-microservice", path=__file__)
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({
    	"myvalue": current_app.ms.myawesomesrv.myvalue, 
    	"myvalue2": current_app.ms.myawesomesrv.myvalue2
    })


if __name__ == '__main__':
    app.run()
```

This would be the output in `http://localhost:5000/`:

```json
{"myvalue": 5, "myvalue2": 1}
```