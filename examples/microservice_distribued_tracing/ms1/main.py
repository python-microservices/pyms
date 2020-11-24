from flask import current_app, jsonify, request

from pyms.flask.app import Microservice

ms = Microservice()
app = ms.create_app()


@app.route("/")
def index():
    app.logger.info("There are my headers: \n{}".format(request.headers))
    return jsonify({"main": "hello world {}".format(current_app.config["APP_NAME"])})


if __name__ == "__main__":
    app.run()
