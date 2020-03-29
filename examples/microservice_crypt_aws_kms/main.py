from base64 import b64decode

from flask import jsonify

from pyms.flask.app import Microservice

ms = Microservice()
app = ms.create_app()


@app.route("/")
def example():
    return jsonify({"main": app.ms.config.encrypted_key})


if __name__ == '__main__':
    app.run()
