import os

import pytest
import requests
from requests.exceptions import ConnectionError

os.environ['ASYNC_TEST_TIMEOUT'] = os.environ.get('ASYNC_TEST_TIMEOUT', '15')


def conf_environment():
    if not os.environ.get("PYMS_CONFIGMAP_FILE", False):
        os.environ["PYMS_CONFIGMAP_FILE"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config-tests.yml")


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Get docker compose file"""
    return os.path.join(str(pytestconfig.rootdir), "docker", "docker-compose.yml")


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
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("consul", 80)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url


@pytest.fixture(scope="session")
def config_env(docker_ip, docker_services):
    """Set config for docker"""
    os.environ["CONSUL_HOST"] = docker_ip
    os.environ["CONSUL_PORT"] = "8500"
