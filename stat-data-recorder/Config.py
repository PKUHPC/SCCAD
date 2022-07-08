# -*- coding: UTF-8 -*-
class Config:
    ## TODO 集群名称
    CLUSTER="hpc01"

    NODE_KEY_SUFFIX = "_cluster_node"
    JOB_KEY_SUFFIX = "_cluster_job"
    PUE_KEY_SUFFIX = "_cluster_pue"

    ##  TODO Redis服务器信息
    REDIS = {
        "hosts":"localhost",
        "port":9999,
        "password":"RedisPassword"
    }

    DB = {
        'host':'db-ip',
        'port':3306,
        'user':'username',
        'passwd':'password',
        'db':'db-name',
        'table' : 'db_stat'
    }
