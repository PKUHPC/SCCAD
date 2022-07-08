# -*- coding: UTF-8 -*-
class Config:
    ## TODO 集群名称
    CLUSTER="hpc01"

    COMMANDS = {
        "nodes_command" : "scontrol show nodes;",
        "jobs_command" : "squeue -o '%P__x__x__%j__x__x__%u__x__x__%T__x__x__%M__x__x__%D__x__x__%R__x__x__%a__x__x__%C__x__x__%q__x__x__%V__x__x__%Y' --noheader",
        ## TODO 获取电力数据的命令
        "pue_command" : ""
    }

    ##  TODO Redis服务器信息
    REDIS = {
        "hosts":"localhost",
        "port":9999,
        "password":"passwd"
    }

    ## TODO 远端数据源的SSH连接信息
    ## 确保该 user 能免密登录 host
    ## 确保该 user 和 host 已经在know_hosts中
    REMOTE_CONNECT = [{"host":"192.168.1.1", "user":"root"}]

    ## TODO 不参与状态统计的集群节点名
    EXCEPT_NODES = ["login01","login02"]

    ## TODO 集群分区分类表，集群stat页面会把该表中的分区集中展示
    ## 格式为 NODE_TYPE = {"分区类型"："分区名"}
    NODE_TYPE = {
        "GPU" : ["GPU"],
        'CPU' : ["C028M256G"]
    }

    ## TODO GPU分区名，这些分区在操作的时候会解析GPU信息
    ## 格式为 GPU_PARTITION = ["分区类型"]
    ## 注意，格式为分区类型，和 NODE_TYPE 中的键对应
    GPU_PARTITION = ["GPU"]
