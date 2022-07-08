## SCCAD Super Computing stAte Dashboard

超算集群状态监控面板

系统由3个部分组成：  
stat-data-redis：负责定期向redis中写入集群状态信息  
stat-data-recorder：负责定期将redis中数据持久化到数据库中  
hpc-stat：集群状态信息可视化  
