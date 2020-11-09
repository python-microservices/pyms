from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice(path=__file__)
app = ms.create_app()


@app.route("/")
def example():
    checks = ms.service_discovery.client.agent.checks()
    return jsonify({"main": checks})


if __name__ == '__main__':
    app.run()
