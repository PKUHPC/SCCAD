import redis

class RedisOpt:

    def __init__(self,config):
        self.redis = redis.StrictRedis(
            host=config['hosts'],
            port=config['port'],
            decode_responses=True,
            password=config['password']
        )
