from pyms.flask.app import Microservice

ms = Microservice(service="my-ms", path=__file__)
app = ms.create_app()

if __name__ == '__main__':
    app.run()
