import pytest
import allure
import logging

logger = logging.getLogger(__name__)


@allure.epic("电商系统")
@allure.feature("商品模块")
class TestProducts():

    @pytest.fixture(autouse=True)
    def _get_basic_data(self,api_client):
        self.api_client=api_client

    @allure.story("查询全部")
    @pytest.mark.product
    def test_get_all_products(self):
        logger.info("查询全部商品")
        resp=self.api_client.get("products")        #封装api_client
        # resp = requests.get(f"{self.base_url}products")
        assert resp.json()["code"] == 0, f"查询全部商品失败, resp={resp.json()}"

    @allure.story("类别查询")
    @allure.title("类别：数码")
    @pytest.mark.product
    def test_get_products_by_category(self):
        logger.info("根据类别查询商品")
        resp=self.api_client.get("products", params={"category": "数码"})
        # resp = requests.get(f"{self.base_url}products", params={"category": "数码"})
        assert resp.json()["code"] == 0, f"类别查询失败, resp={resp.json()}"

    @allure.story("分页查询")
    @allure.title("page:1, page_size:2")
    @pytest.mark.product
    def test_get_product_by_page(self):
        logger.info("分页查询商品")
        resp=self.api_client.get("products",params={"page": 1, "page_size": 2})
        # resp = requests.get(f"{self.base_url}products", params={"page": 1, "page_size": 2})
        assert resp.json()["code"] == 0, f"分页查询失败, resp={resp.json()}"

    @allure.story("根据id查询")
    @allure.title("id={id}, expected_name={expected_name}")
    @pytest.mark.product
    @pytest.mark.parametrize("id,expected_name", [
        (1, "Python"), (2, "键盘"), (3, "显示器"), (4, "工学椅"), (5, "耳机")
    ])
    def test_get_product_by_id(self, id, expected_name):
        logger.info("根据id查询, id: %s, expected_name: %s", id, expected_name)
        resp=self.api_client.get(f"products/{id}")
        # resp = requests.get(f"{self.base_url}products/{id}")
        if resp.json()["code"] != 0:
            logger.error("商品查询失败 | id=%s, resp=%s", id, resp.text)
        assert resp.json()["code"] == 0, f"商品id={id}查询失败, resp={resp.json()}"
        assert expected_name in resp.json()["data"]["name"],f"商品名不匹配, 期望包含'{expected_name}', 实际'{resp.json()['data']['name']}'"
