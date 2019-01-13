# Examples

```bash
pip install py-ms
```

config.yml:

```yaml
my-minimal-microservice:
  APP_NAME: "Python Microservice"
```

main.py

```python
from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice(service="my-minimal-microservice", path=__file__)
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({"main": "hello world"})


if __name__ == '__main__':
    app.run()
```

```bash
python main.py
```

Open in your browser http://localhost:5000/

See [this Github page](https://github.com/python-microservices/pyms/tree/master/examples) to see a examples