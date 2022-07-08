import redis
from local import setting

class RedisOpt:
    def __init__(self):
        self.redis = redis.StrictRedis(
            host=setting.REDIS['hosts'],
            port=setting.REDIS['port'],
            decode_responses=True,
            password=setting.REDIS['password']
        )
