import pymysql
import random
import string

# 数据库连接设置，请根据实际情况调整
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '9Ozw,)h9nq-7',
    'database': 'supplies'
}

# 生成随机字符串
def random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# 连接数据库
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

try:
    # 插入数据的SQL语句
    insert_sql = """
    INSERT INTO act_supplies_auxiliary_accounting
    (affiliated_file, affiliated_organization, code, name, referred_as, superior_code, superior, status, notes, primary_key)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    # 生成并插入100条随机数据
    for _ in range(100000):
        data = (
            random_string(), random_string(), random_string(20), random_string(),
            random_string(), random_string(20), random_string(), random_string(),
            random_string(), random_string(20)
        )
        cursor.execute(insert_sql, data)

    # 提交事务
    conn.commit()
    print("数据插入成功")
except Exception as e:
    # 如果出错则回滚
    conn.rollback()
    print(f"数据插入失败: {e}")
finally:
    # 关闭连接
    cursor.close()
    conn.close()