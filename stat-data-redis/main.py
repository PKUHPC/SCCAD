from model.Node import SlurmNodeInfo
from model.Job import SlurmJobInfo
from model.Energy import Energy
from local import config
# from RemoteShell import RemoteShell
from LocalShell import LocalShell
from RedisOpt import RedisOpt

import datetime,argparse

def update_node_job(ssh_client,redis_client):
    slurm_node_ret = ssh_client.execute(config.COMMANDS["nodes_command"])
    if not slurm_node_ret:
        print("ERROR")
        exit()
    slurm_node = SlurmNodeInfo(str(slurm_node_ret))

    slurm_job_ret = ssh_client.execute(config.COMMANDS["jobs_command"])
    slurm_job = SlurmJobInfo(str(slurm_job_ret))

    ### 集群节点统计信息
    r_cluster_node_info_name = config.CLUSTER+"_cluster_node"
    cluster_node_info = slurm_node.get_cluster_node_info()
    ret = redis_client.redis.hset(r_cluster_node_info_name, mapping=cluster_node_info)

    ### 集群节点摘要信息
    r_cluster_node_brief_name = config.CLUSTER+"_cluster_brief"
    cluster_node_brief = slurm_node.get_cluster_node_brief()
    ret = redis_client.redis.hset(r_cluster_node_brief_name, mapping=cluster_node_brief)

    ### 集群所有节点列表
    r_cluster_nodes = config.CLUSTER+"_nodes"
    cluster_nodes = slurm_node.get_node_array()
    ret = redis_client.redis.hset(r_cluster_nodes, mapping=cluster_nodes)

    ### 集群作业统计信息
    r_cluster_job_info_name = config.CLUSTER+"_cluster_job"
    cluster_job_info = slurm_job.get_cluster_job_info()
    ret = redis_client.redis.hset(r_cluster_job_info_name, mapping=cluster_job_info)

    ### 集群作业摘要信息
    r_cluster_job_brief_name = config.CLUSTER+"_cluster_brief"
    cluster_job_brief = slurm_job.get_cluster_job_brief()
    ret = redis_client.redis.hset(r_cluster_job_brief_name, mapping=cluster_job_brief)

    ### 集群所有作业列表
    r_cluster_jobs = config.CLUSTER+"_jobs"
    cluster_jobs = slurm_job.get_job_array()
    ret = redis_client.redis.hset(r_cluster_jobs, mapping=cluster_jobs)

def update_pue(ssh_client,redis_client):
    pue_str = ssh_client.execute(config.COMMANDS["pue_command"])
    pue = Energy(str(pue_str))

    r_cluster_job_info_name = config.CLUSTER+"_cluster_pue"
    cluster_pue = pue.get_cluster_pue()
    if cluster_pue:
        ret = redis_client.redis.hset(r_cluster_job_info_name, mapping=cluster_pue)

if __name__ == "__main__":

    # ssh_client = RemoteShell(config.REMOTE_CONNECT)
    ssh_client = LocalShell()
    r = RedisOpt()

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--node', action='store_true', help="Get node(and job) info from remote slurm client")
    parser.add_argument('-j', '--job', action='store_true', help="Get job(and node) info from remote slurm client")
    parser.add_argument('-p', '--pue', action='store_true', help="Get pue info from remote server")

    args = parser.parse_args()

    if args.node or args.job:
        update_node_job(ssh_client,r)
    if args.pue :
        update_pue(ssh_client,r)
