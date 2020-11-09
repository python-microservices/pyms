from flask import jsonify, request

from pyms.flask.app import Microservice

ms = Microservice()
app = ms.create_app()


@app.route("/")
def index():
    app.logger.info("There are my headers: \n{}".format(request.headers))
    response = app.ms.requests.get("http://localhost:5000/")
    return jsonify({"response": response.json()})


if __name__ == "__main__":
    app.run(port=5001)
