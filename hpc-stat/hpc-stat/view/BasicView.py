from abc import abstractmethod
from local import setting

from lib.RedisOpt import RedisOpt

class BasicView:
    cluster = None
    cluster_name = ""
    def __init__(self):
        self.r = RedisOpt()

    @property
    def all_clusters(self):
        return ["hpc01"]

    @property
    def api_server(self):
        return "{protocal}://{host}:{port}/".format(
            protocal = setting.cluster[self.cluster]['protocal'],
            host = setting.cluster[self.cluster]['host'],
            port = setting.cluster[self.cluster]['port']
        )

    @classmethod
    def factory(cls,cluster_name):
        for subclass in cls.__subclasses__():
            if cluster_name == subclass.cluster:
                return subclass()
            for subsubclass in subclass.__subclasses__():
                if cluster_name == subsubclass.cluster:
                    return subsubclass()
        return cls.__subclasses__()[0]()
