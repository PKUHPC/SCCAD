import string, random

class BaseConfig:
    LANGUAGES = ['en', 'zh']
    secret_key = "".join(random.sample(string.ascii_letters + string.digits,32))

    ##  TODO Redis服务器信息
    REDIS = {
        "hosts":"localhost",
        "port":6357,
        "password":"passwd"
    }

    MYSQL = {
        "host" : "localhost",
        "port" : 3306,
        "user" : "root",
        "passwd" : "passwd",
        "database" : "hpc",
        "table" : {
            "history" : "history",
        }
    }

class DevConfig(BaseConfig):
    DEBUG = True
    ENV = "development"
    HOST = "localhost"
    PORT = 9000
    api_server_port = 8000

class ProConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    HOST = "localhost"
    PORT = 10000
