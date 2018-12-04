import os
from flask import jsonify
from pyms.flask.app import Microservice

os.environ["CONFIGMAP_FILE"] = "config.yml"
ms = Microservice(service="my-minimal-microservice", path=__file__)
app = ms.create_app()

@app.route("/")
def example():
    return jsonify({"main": "hello world"})

if __name__ == '__main__':
    app.run()
