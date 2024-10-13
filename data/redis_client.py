import redis  # Redis客户端
from config.settings import REDIS_HOST, REDIS_PORT

class RedisClient:
    def __init__(self):
        # 初始化Redis客户端
        self.client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

    def get(self, key):
        """获取Redis中的值"""
        return self.client.get(key)

    def set(self, key, value):
        """设置Redis中的值"""
        self.client.set(key, value)
