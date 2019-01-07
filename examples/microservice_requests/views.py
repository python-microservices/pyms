from examples.microservice_requests import ms


def example():
    return ms.requests.get_for_object("https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe")
