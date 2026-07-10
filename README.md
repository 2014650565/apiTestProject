# 接口自动化测试实战项目

## 启动 Mock 服务器

```bash
cd D:\Python\apiTestProject
python mock_server\app.py
```

服务运行在 `http://127.0.0.1:5000`

## Mock API 接口文档

### 健康检查

```
GET /api/health
-> {"code":0, "message":"ok", "server_time":"..."}
```

### 登录

```
POST /api/login
body: {"username":"...", "password":"..."}

成功 -> 200  {"code":0, "token":"mock_token_...", "user":{"id":1, "username":"tester", "name":"测试同学", "role":"qa"}}
失败 -> 400  {"code":1, "message":"用户名或密码不能为空"}
失败 -> 401  {"code":1, "message":"用户名或密码错误"}

可用账号:
  tester / 123456   (角色: qa)
  admin  / admin123  (角色: admin)
  seller / seller123 (角色: seller)
```

### 商品列表

```
GET /api/products
GET /api/products?category=数码
GET /api/products?page=1&page_size=2

-> {"code":0, "data":{"total":5, "page":1, "page_size":10, "items":[...]}}

商品数据:
  id=1  Python编程：从入门到实践  89元   120库存  图书
  id=2  机械键盘K8              399元  55库存   数码
  id=3  27寸4K显示器            2499元 8库存    数码
  id=4  人体工学椅Pro           1899元 0库存    家具
  id=5  蓝牙降噪耳机            699元  200库存  数码
```

### 商品详情

```
GET /api/products/<id>

存在 -> 200  {"code":0, "data":{"id":1, "name":"...", "price":89.0, "stock":120, "category":"图书"}}
不存在 -> 404  {"code":1, "message":"商品 xxx 不存在"}
```

### 创建订单（需要登录）

```
POST /api/orders
headers: {"Authorization": "Bearer <token>"}
body: {"product_id":1, "quantity":2}

成功   -> 201  {"code":0, "data":{"order_id":1001, "total_price":178.0, "status":"待支付", ...}}
无token -> 401  {"code":2, "message":"未登录或token已失效"}
假token -> 401  {"code":2, "message":"未登录或token已失效"}
不存在商品 -> 404  {"code":1, "message":"商品 xxx 不存在"}
库存不足   -> 400  {"code":1, "message":"库存不足（剩余 x）"}
```

### 查询订单（需要登录）

```
GET /api/orders
headers: {"Authorization": "Bearer <token>"}

成功 -> 200  {"code":0, "data":{"total":N, "items":[...]}}
无token -> 401
```

### 不稳定接口（练习失败重试）

```
GET /api/unstable

约 60% 概率 -> 200  {"code":0, "data":"这次成功了！"}
约 40% 概率 -> 500  {"code":1, "message":"服务器繁忙，请重试"}
```

## 测试数据文件

- `test_suite/data/login_data.csv`  — 登录测试数据（含正确和错误组合）
- `test_suite/data/order_data.yaml`  — 订单测试数据（含正常和不存在的商品）

## 你需要创建的文件（都在 test_suite/ 下）

```
test_suite/
├── conftest.py      # 定义 fixture（base_url、token、api_client...）
├── test_login.py    # 登录接口测试
├── test_product.py  # 商品接口测试
├── test_order.py    # 订单接口测试（接口关联）
└── test_rerun.py    # 失败重试
```

pytest.ini 和 data/ 已准备好，你只需写测试代码。

## 运行测试

```bash
cd test_suite
python -m pytest -v -s --sensitive-url=''
```
