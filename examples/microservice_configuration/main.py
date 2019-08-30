from examples.microservice_configuration import ms
app = ms.create_app()

if __name__ == '__main__':
    """
    run first:
    export CONFIGMAP_SERVICE=my-configure-microservice
    """
    app.run()
