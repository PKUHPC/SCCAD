import redis
from local import config

class RedisOpt:
    def __init__(self):
        self.redis = redis.StrictRedis(
            host=config.REDIS['hosts'],
            port=config.REDIS['port'],
            decode_responses=True,
            password=config.REDIS['password']
        )
