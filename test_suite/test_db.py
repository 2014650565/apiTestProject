import pytest

#数据库验证
@pytest.mark.db
def test_db_query(db_conn):
    with db_conn.cursor() as cursor:
        cursor.execute("select * from users where username = 'tester'")
        row=cursor.fetchone()
        assert row is not None
        print(f"查到用户: {row}")