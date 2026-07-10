import pytest
import requests
import allure
import logging

logger = logging.getLogger(__name__)


@allure.epic("电商系统")
@allure.feature("公共")
@allure.story("健康检查")
@allure.title("服务健康检查")
@pytest.mark.health
def test_health(base_url):
    logger.info("健康检查")
    resp = requests.get(f"{base_url}health")
    assert resp.json()["code"] == 0, f"健康检查失败, resp={resp.json()}"
