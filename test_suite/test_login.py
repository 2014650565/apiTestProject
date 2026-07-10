import pytest
from common.csv_util import csv_read
import allure
import logging
logger = logging.getLogger(__name__)


@allure.epic("电商系统")
@allure.feature("登录模块")
class TestLogin():

    @pytest.fixture(autouse=True)
    def _get_base_url(self, api_client):
        self.api_client=api_client

    @allure.story("登陆验证")
    @allure.title("登录：{username}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.login
    @pytest.mark.smoke
    @pytest.mark.parametrize("username,password,expected_code", csv_read("./test_suite/data/login_data.csv"))
    def test_login(self, username, password, expected_code):
        with allure.step("发送登录请求:"):
            logger.info("测试账号密码: %s, %s", username, password)
            resp=self.api_client.post("login",json={"username": username, "password": password})
            # resp = requests.request(url=f"{self.base_url}login",
            #                         method="post",
            #                         json={"username": username, "password": password})

        if resp.json()["code"] != int(expected_code):
            logger.error("登录失败 | 账号: %s, 期望code: %s, 实际code: %s",
                         username, expected_code, resp.json()["code"])
        assert resp.json()["code"] == int(expected_code),  f"登录断言失败, 期望code={expected_code}, 实际={resp.json()}"
