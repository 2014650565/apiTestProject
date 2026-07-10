import requests
import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.epic("电商系统")
@allure.feature("稳定性")
@allure.story("失败重试")
@allure.title("重试次数:10, 延迟:0.5")
@pytest.mark.unstable
@pytest.mark.flaky(reruns=10, reruns_delay=0.5)
def test_reruns(base_url):
    logger.info("调用不稳定接口")
    resp = requests.get(f"{base_url}unstable")
    
    if resp.json()["code"] != 0:
        logger.error("不稳定接口失败 | resp=%s", resp.text)
    assert resp.json()["code"] == 0, f"不稳定接口最终失败, resp={resp.json()}"
