import os

import pytest

os.environ['ASYNC_TEST_TIMEOUT'] = os.environ.get('ASYNC_TEST_TIMEOUT', '15')


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    """Get docker compose file"""
    return os.path.join(str(pytestconfig.rootdir), "docker", "docker-compose.yml")


@pytest.fixture(scope="session")
def config_env(docker_ip, docker_services):
    """Set config for docker"""
    os.environ["CONSUL_HOST"] = docker_ip
    os.environ["CONSUL_PORT"] = "8500"
