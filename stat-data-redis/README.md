

### 系统功能：

1. 在远端集群中运行slurm指令获得节点信息和作业信息，结构化之后存储在redis中
2. 在远端集群中运行指令获得节点PUE信息，结构化之后存储在redis中



### 部署方式：

1. 新建local.py，按照 Config 类中 TODO 的注释说明修改对应信息
2. 安装依赖库 pip3 install -r requirements.txt

### 注意
提供调用本地shell和调用远端shell两种方式查询slurm信息，对应实现为 LocalShell 和 RemoteShell，需要在main.py中手动切换。


### 使用方式：

```shell
python3 main.py -h
```



### Redis数据结构

1. 集群状态页信息：

   存储方式为哈希

| key                          | field              | value                    |
| :--------------------------- | ------------------ | ------------------------ |
| [cluster_name]_cluster_node  | all_cpu_alloc      | 所有节点 CPU 运行中数量  |
|                              | all_cpu_error      | 所有节点 CPU 不可用数量  |
|                              | all_cpu_free       | 所有节点 CPU 可用数量    |
|                              | all_cpu_tot        | 所有节点 CPU 总数        |
|                              | all_node_tot       | 所有节点 节点 总数       |
|                              | all_node_error     | 所有节点 节点 不可用数量 |
|                              | all_node_available | 所有节点 节点 可用数量   |
|                              | all_node_running   | 所有节点 节点 运行中数量 |
|                              | gpu_card_alloc     | GPU节点 GPU 运行中数量   |
|                              | gpu_card_error     | GPU节点 GPU 不可用数量   |
|                              | gpu_card_free      | GPU节点 GPU 可用数量     |
|                              | gpu_card_tot       | GPU节点 GPU 总数         |
|                              | gpu_node_error     | GPU节点 节点 不可用数量  |
|                              | gpu_node_running   | GPU节点 节点 运行中数量  |
|                              | gpu_node_available | GPU节点 节点 可用数量    |
|                              | gpu_node_tot       | GPU节点 节点 总数        |
|                              | cpu_cpu_alloc      | CPU节点 CPU 运行中数量   |
|                              | cpu_cpu_error      | CPU节点 CPU 不可用数量   |
|                              | cpu_cpu_free       | CPU节点 CPU 可用数量     |
|                              | cpu_cpu_tot        | CPU节点 CPU 总数         |
|                              | cpu_node_tot       | CPU节点 节点 总数        |
|                              | cpu_node_error     | CPU节点 节点 不可用数量  |
|                              | cpu_node_available | CPU节点 节点 可用数量    |
|                              | cpu_node_running   | CPU节点 节点 运行中数量  |
|                              | update_time        | 更新时间                 |
| [cluster_name]_cluster_job   | running_jobs       | 运行中的作业数           |
|                              | pending_jobs       | 排队中的作业数           |
|                              | cpu_running_jobs   | 运行中的CPU作业数        |
|                              | cpu_pending_jobs   | 排队中的CPU作业数        |
|                              | gpu_running_jobs   | 运行中的GPU作业数        |
|                              | gpu_pending_jobs   | 排队中的GPU作业数        |
|                              | running_users      | 运行中的用户数           |
|                              | pending_users      | 排队中的用户数           |
|                              | users              | 排队和运行的用户总数     |
|                              | cpu_users          | 排队和运行的CPU用户总数  |
|                              | gpu_users          | 排队和运行的GPU用户总数  |
|                              | cpu_running_users  | 运行中的CPU用户数        |
|                              | cpu_pending_users  | 排队中的CPU用户数        |
|                              | gpu_running_users  | 运行中的GPU用户数        |
|                              | gpu_pending_users  | 排队中的GPU用户数        |
|                              | pengding_top5      | 作业排队时间TOP5         |
|                              | running_top5       | 作业运行时间TOP5         |
|                              | update_time        | 更新时间                 |
| [cluster_name]_cluster_pue   | pue                | 能源效率（PUE）          |
|                              | power              | 电力负荷                 |
|                              | update_time        | 更新时间                 |
| [cluster_name]_cluster_brief | node_running       | 运行的节点比例           |
|                              | node_available     | 可用的节点比例           |
|                              | node_error         | 不可用的节点比例         |
|                              | core_running       | 运行的核心/卡比例        |
|                              | core_available     | 可用的核心/卡比例        |
|                              | core_error         | 不可用的核心/卡比例      |
|                              | job_running        | 运行中的作业数           |
|                              | job_pending        | 排队中的作业数           |

2. 集群作业状态页面信息

   存储方式为列表


| [cluster_name]_jobs  | name              | 作业名               |
| :------------------- | ----------------- | -------------------- |
|                      | account           | 账户                 |
|                      | user              | 用户                 |
|                      | partition         | 分区                 |
|                      | qos               | QOS                  |
|                      | nodes             | 节点数               |
|                      | cpus              | 核心数               |
|                      | state             | 状态                 |
|                      | time_used         | 运行/排队时间        |
|                      | time_used_seconds | 运行/排队时间(秒)    |
|                      | info              | 说明                 |




3. 集群节点状态页面信息

   存储方式为列表

| [cluster_name]_nodes | name              | 节点名               |
| :------------------- | ----------------- | -------------------- |
|                      | type              | 节点类型             |
|                      | state             | 节点状态             |
|                      | res_tot           | CPU核心/GPU卡 总数   |
|                      | res_alloc         | CPU核心/GPU卡 已使用 |
|                      | cpu_avg_load      | CPU负载              |
|                      | mem_tot           | 内存总数             |
|                      | mem_alloc         | 已用内存             |

### Redis 启动和配置：

```shell
docker run -itd --name hpc-redis -p 6379:6379 redis
docker exec -it hpc-redis /bin/bash

redis_cli
CONFIG SET requirepass "PASSWORD"

```
