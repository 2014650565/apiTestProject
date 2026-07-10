import requests
import pytest
from common.yaml_util import yaml_read
import allure
import logging

logger = logging.getLogger(__name__)


@allure.epic("电商系统")
@allure.feature("订单模块")
class TestOrder():

    @pytest.fixture(autouse=True)
    def _get_basic_data(self, api_client):
        self.api_client=api_client

    @allure.story("创建订单")
    @allure.title("product_id:{testcase[product_id]}, quantity:{testcase[quantity]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.order
    @pytest.mark.smoke
    @pytest.mark.parametrize("testcase", yaml_read("./test_suite/data/order_data.yaml"))
    def test_create_orders(self, testcase):
        logger.info("创建订单, product_id: %s, quantity: %s", testcase["product_id"], testcase["quantity"])
        resp=self.api_client.post("orders",json={"product_id": testcase["product_id"],"quantity": testcase["quantity"]})
        # resp = requests.request(url=f"{self.base_url}orders",
        #                         method="post",
        #                         json={"product_id": testcase["product_id"],
        #                               "quantity": testcase["quantity"]},
        #                         headers=self.header)

        if testcase["expected_total"] is None:
            if resp.json()["code"] == 0:
                logger.error("预期失败但成功了 | resp=%s", resp.text)
            assert resp.json()["code"] != 0, f"预期失败但code=0, resp={resp.json()}"
            if resp.status_code == 404:
                assert "不存在" in resp.json()["message"], \
                    f"商品不存在断言失败, resp={resp.json()}"
            elif resp.status_code == 400:
                assert "库存不足" in resp.json()["message"], \
                    f"库存不足断言失败, resp={resp.json()}"
        else:
            if resp.json()["code"] != 0:
                logger.error("创建订单失败 | resp=%s", resp.text)
            assert resp.json()["code"] == 0, f"下单失败, resp={resp.json()}"
            assert resp.json()["data"]["total_price"] == testcase["expected_total"], \
                f"金额不匹配, 期望{testcase['expected_total']}, 实际{resp.json()['data']['total_price']}"

    @allure.story("鉴权")
    @allure.title("token为空")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.order
    def test_create_order_without_token(self,base_url):
        logger.info("token为空时创建订单")
        resp = requests.request(url=f"{base_url}orders",
                                method="post",
                                json={"product_id": 1, "quantity": 1})
        if resp.status_code != 401:
            logger.error("状态码断言失败 | 期望401, 实际%s | %s", resp.status_code, resp.text)
        assert resp.status_code == 401, f"期望401, 实际{resp.status_code}, resp={resp.text}"
        assert resp.json()["code"] == 2, f"期望code=2, 实际{resp.json()['code']}, resp={resp.text}"
        assert "未登录" in resp.json()["message"], \
            f"期望消息含'未登录', 实际{resp.json().get('message','N/A')}"

    @allure.story("鉴权")
    @allure.title("虚假token")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.order
    def test_create_order_with_fake_token(self,base_url):
        logger.info("虚假token创建订单")
        resp = requests.request(url=f"{base_url}orders",
                                method="post",
                                json={"product_id": 1, "quantity": 1},
                                headers={"Authorization": "Bearer fake_token"})
        if resp.status_code != 401:
            logger.error("状态码断言失败 | 期望401, 实际%s | %s", resp.status_code, resp.text)
        assert resp.status_code == 401, f"期望401, 实际{resp.status_code}, resp={resp.text}"
        assert resp.json()["code"] == 2, f"期望code=2, 实际{resp.json()['code']}, resp={resp.text}"
        assert "未登录" in resp.json()["message"], \
            f"期望消息含'未登录', 实际{resp.json().get('message','N/A')}"

    @allure.story("查询订单")
    @pytest.mark.order
    def test_get_all_orders(self):
        logger.info("查询订单列表")
        resp=self.api_client.get("orders")
        # resp = requests.request(url=f"{self.base_url}orders",
        #                         method="get",
        #                         headers=self.header)
        assert resp.json()["code"] == 0, f"查询订单失败, resp={resp.json()}"
