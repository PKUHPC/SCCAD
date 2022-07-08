### 功能说明：

从redis中取的集群的实时状态数据，存入数据库中；
redis数据结构参考 stat-data-provider 项目；



### 使用说明：

在 *local.py* 中配置数据库信息和redis信息；

执行指令的时候可以指定集群名字和表名字，如果没指定，使用 *local.py* 中的配置。

python3 crond.py -t table_name -c cluster_name
