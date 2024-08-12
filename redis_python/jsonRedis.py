import json
import redis

# 将JSON数据转换为字符串
json_data = [
    [
        118.897299,
        32.02599
    ],
    [
        118.893303,
        32.026212
    ]
]

# 连接到Redis服务器
redis_client = redis.StrictRedis(host='*****', port=6379, db=00,password="*****")

for index, coords in enumerate(json_data):
    i=1;
    i = i+1;
    # 生成唯一的键名
    key = f'loc+i:{index}'
    # 将经纬度对转换为JSON字符串
    value = json.dumps(coords)
    # 将键值对存入Redis
    redis_client.set(key, value)
    print("JSON数据已存入Redis的Hash中。")
    