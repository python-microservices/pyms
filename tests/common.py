from pyms.flask.app import Microservice

class MyMicroserviceNoSingleton(Microservice):
    _singleton = False


class MyMicroservice(Microservice):
    pass
