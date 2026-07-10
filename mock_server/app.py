"""
模拟电商系统 API 服务器
提供登录、商品查询、订单管理接口，供 pytest 练习接口自动化测试。

启动方式：
    python mock_server/app.py
    服务运行在 http://127.0.0.1:5000
"""

from flask import Flask, request, jsonify
import time
import random

app = Flask(__name__)

# ============================================================
# 模拟数据库
# ============================================================
USERS = {
    "tester":  {"password": "123456", "name": "测试同学", "role": "qa"},
    "admin":   {"password": "admin123", "name": "管理员", "role": "admin"},
    "seller":  {"password": "seller123", "name": "卖家小王", "role": "seller"},
}

PRODUCTS = [
    {"id": 1,  "name": "Python 编程：从入门到实践", "price": 89.0,  "stock": 120, "category": "图书"},
    {"id": 2,  "name": "机械键盘 K8",              "price": 399.0, "stock": 55,  "category": "数码"},
    {"id": 3,  "name": "27 寸 4K 显示器",           "price": 2499.0,"stock": 8,   "category": "数码"},
    {"id": 4,  "name": "人体工学椅 Pro",            "price": 1899.0,"stock": 0,   "category": "家具"},
    {"id": 5,  "name": "蓝牙降噪耳机",              "price": 699.0, "stock": 200, "category": "数码"},
]

# token -> username 映射（简化版，生产环境用 JWT）
TOKENS = {}
ORDERS = []  # 存储订单
_order_id_counter = 1000


def generate_token(username):
    """简易 token 生成"""
    token = f"mock_token_{username}_{int(time.time())}"
    TOKENS[token] = username
    return token


def get_user_by_token(token):
    """根据 token 获取用户名，token 不存在或无效返回 None"""
    return TOKENS.get(token)


# ============================================================
# 接口实现
# ============================================================

# ---------- 健康检查 ----------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"code": 0, "message": "ok", "server_time": time.strftime("%Y-%m-%d %H:%M:%S")})


# ---------- 登录 ----------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    # 故意慢一点，方便观察 reruns 效果
    time.sleep(0.05)

    if not username or not password:
        return jsonify({"code": 1, "message": "用户名或密码不能为空"}), 400

    user = USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"code": 1, "message": "用户名或密码错误"}), 401

    token = generate_token(username)
    return jsonify({
        "code": 0,
        "message": "success",
        "token": token,
        "user": {
            "id": list(USERS.keys()).index(username) + 1,
            "username": username,
            "name": user["name"],
            "role": user["role"],
        }
    }), 200


# ---------- 商品列表 ----------
@app.route("/api/products", methods=["GET"])
def product_list():
    # 支持 ?category=数码 筛选
    category = request.args.get("category")
    if category:
        result = [p for p in PRODUCTS if p["category"] == category]
    else:
        result = PRODUCTS

    # 支持分页（page, page_size）
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    start = (page - 1) * page_size
    end = start + page_size

    return jsonify({
        "code": 0,
        "data": {
            "total": len(result),
            "page": page,
            "page_size": page_size,
            "items": result[start:end],
        }
    }), 200


# ---------- 商品详情 ----------
@app.route("/api/products/<int:pid>", methods=["GET"])
def product_detail(pid):
    product = next((p for p in PRODUCTS if p["id"] == pid), None)
    if not product:
        return jsonify({"code": 1, "message": f"商品 {pid} 不存在"}), 404
    return jsonify({"code": 0, "data": product}), 200


# ---------- 创建订单（需登录） ----------
@app.route("/api/orders", methods=["POST"])
def create_order():
    # 鉴权
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    username = get_user_by_token(token)
    if not username:
        return jsonify({"code": 2, "message": "未登录或 token 已失效"}), 401

    data = request.get_json(force=True, silent=True) or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    # 参数校验
    if not product_id:
        return jsonify({"code": 1, "message": "商品 ID 不能为空"}), 400

    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return jsonify({"code": 1, "message": f"商品 {product_id} 不存在"}), 404

    if product["stock"] < quantity:
        return jsonify({"code": 1, "message": f"库存不足（剩余 {product['stock']}）"}), 400

    # 扣库存、创建订单
    product["stock"] -= quantity
    global _order_id_counter
    _order_id_counter += 1
    order = {
        "order_id": _order_id_counter,
        "username": username,
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "total_price": round(product["price"] * quantity, 2),
        "status": "待支付",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    ORDERS.append(order)
    return jsonify({"code": 0, "message": "订单创建成功", "data": order}), 201


# ---------- 查询订单（需登录） ----------
@app.route("/api/orders", methods=["GET"])
def list_orders():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    username = get_user_by_token(token)
    if not username:
        return jsonify({"code": 2, "message": "未登录或 token 已失效"}), 401

    my_orders = [o for o in ORDERS if o["username"] == username]
    return jsonify({"code": 0, "data": {"total": len(my_orders), "items": my_orders}}), 200


# ---------- 故意不稳的接口（供 reruns 练习） ----------
@app.route("/api/unstable", methods=["GET"])
def unstable():
    """随机失败，用于练习 --reruns 重试"""
    if random.random() < 0.6:
        return jsonify({"code": 0, "data": "这次成功了！"}), 200
    else:
        return jsonify({"code": 1, "message": "服务器繁忙，请重试"}), 500


if __name__ == "__main__":
    print("Mock 电商 API 已启动 -> http://127.0.0.1:5000")
    print("   可用账号: tester/123456 | admin/admin123 | seller/seller123")
    app.run(host="127.0.0.1", port=5000, debug=False)
