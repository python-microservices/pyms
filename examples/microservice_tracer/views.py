from flask import current_app

from examples.microservice_requests import ms


def example():
    current_app.logger.info("start request")
    result = ms.requests.get_for_object("https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe")
    current_app.logger.info("end request")
    return result
