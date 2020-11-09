import os

import pytest
import requests
from requests.exceptions import ConnectionError

os.environ["ASYNC_TEST_TIMEOUT"] = os.environ.get("ASYNC_TEST_TIMEOUT", "15")


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def http_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    url = "http://{}:{}".format(docker_ip, 8500)

    docker_services.wait_until_responsive(timeout=60.0, pause=0.1, check=lambda: is_responsive(url))
    return docker_ip


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Get docker compose file"""
    return os.path.join(str(pytestconfig.rootdir), "docker", "docker-compose.yml")


@pytest.fixture(scope="session")
def config_env(http_service):
    """Set config for docker"""
    os.environ["CONSUL_HOST"] = http_service
    os.environ["CONSUL_PORT"] = "8500"
