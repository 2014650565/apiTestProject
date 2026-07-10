import pymysql

DB_CONFIG={
    "host":"127.0.0.1",                #可能需要进行数据分离
    "port":3306,
    "user":"root",
    "password":"123456",
    "database":"mall_test",
    "charset": "utf8mb4"
}

def get_connection():
    try:
        conn=pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None
    



if __name__=="__main__":
    print(get_connection())