from pyms.flask.app import Microservice

ms = Microservice()
app = ms.create_app()

if __name__ == "__main__":
    app.run()
