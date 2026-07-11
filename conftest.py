import pytest
import requests
from common.api_client import ApiClient

@pytest.fixture(scope="session")
def base_url(env_config):
    return env_config["base_url"]


@pytest.fixture(scope="session")
def get_token(base_url):
    print("用例开始测试")
    resp = requests.request(
        url=f"{base_url}/login",
        method="post",
        json={"username": "tester", "password": "123456"},
    )
    token = resp.json()["token"]
    yield token
    print("用例测试结束")


@pytest.fixture(scope="session")
def api_client(base_url,get_token):
    return ApiClient(base_url,get_token)



#环境配置,  固定名称
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev",
                     choices=["dev", "test", "prod"])
    
@pytest.fixture(scope="session")
def env_config(request):
    env = request.config.getoption("--env")
    from common.config import ENV_CONFIG
    return ENV_CONFIG[env]

#mysql连接
@pytest.fixture(scope="function")
def db_conn():
    
    from common.db_util import get_connection

    conn=get_connection()
    if conn is None:
        pytest.skip("数据库不可用")

    yield conn

    conn.close()
