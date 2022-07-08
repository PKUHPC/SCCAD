from local import config
from RedisOpt import RedisOpt
from MySql import Mysql

import datetime,argparse

class HistoryData:
    def __init__(self,conf):
        self.r = RedisOpt(conf.REDIS)

        node_item = self.r.redis.hgetall(conf.CLUSTER+conf.NODE_KEY_SUFFIX)
        job_item = self.r.redis.hgetall(conf.CLUSTER+conf.JOB_KEY_SUFFIX)
        pue_item = self.r.redis.hgetall(conf.CLUSTER+conf.PUE_KEY_SUFFIX)

        self.node = self._get_number_value(node_item,"all_node_running")
        self.core = self._get_number_value(node_item,"all_cpu_alloc")
        self.cpu_node = self._get_number_value(node_item,"cpu_node_running")
        self.cpu_core = self._get_number_value(node_item,"cpu_cpu_alloc")
        self.all_node = self._get_number_value(node_item,"all_node_tot")
        self.all_core = self._get_number_value(node_item,"all_cpu_tot")

        self.gpu_core = self._get_number_value(node_item,"gpu_cpu_alloc")
        self.gpu_gpu = self._get_number_value(node_item,"gpu_card_alloc")
        self.gpu_node = self._get_number_value(node_item,"gpu_node_running")
        self.gpu_error_node = self._get_number_value(node_item,"gpu_node_error")
        self.cpu_error_core = self._get_number_value(node_item,"cpu_cpu_error")
        self.gpu_error_core = self._get_number_value(node_item,"gpu_cpu_error")
        self.gpu_error_gpu = self._get_number_value(node_item,"gpu_card_error")
        self.all_gpu = self._get_number_value(node_item,"gpu_card_tot")
        self.all_gpu_core = self._get_number_value(node_item,"gpu_cpu_tot")
        self.all_gpu_node = self._get_number_value(node_item,"gpu_node_tot")

        self.error_node = self._get_number_value(node_item,"all_node_error")
        self.error_core = self._get_number_value(node_item,"all_cpu_error")
        self.cpu_error_node = self._get_number_value(node_item,"cpu_node_error")
        self.all_cpu_node = self._get_number_value(node_item,"cpu_node_tot")
        self.all_cpu_core = self._get_number_value(node_item,"cpu_cpu_tot")

        self.pue = pue_item["pue"] if "pue" in pue_item else "null"
        self.power = pue_item["power"] if "power" in pue_item else "null"

        self.user = self._get_number_value(job_item,"users")
        self.job = self._get_number_value(job_item,"running_jobs")+self._get_number_value(job_item,"pending_jobs")
        self.cpu_running_job = self._get_number_value(job_item,"cpu_running_jobs")
        self.running_job = self._get_number_value(job_item,"running_jobs")
        self.waiting_job = self._get_number_value(job_item,"pending_jobs")
        self.cpu_waiting_job = self._get_number_value(job_item,"cpu_pending_jobs")
        self.cpu_user = self._get_number_value(job_item,"cpu_users")
        self.cpu_job = self._get_number_value(job_item,"cpu_running_jobs")+self._get_number_value(job_item,"cpu_pending_jobs")

        self.gpu_user = self._get_number_value(job_item,"gpu_user")
        self.gpu_running_job = self._get_number_value(job_item,"gpu_running_jobs")
        self.gpu_waiting_job = self._get_number_value(job_item,"gpu_pending_jobs")
        self.gpu_job = self._get_number_value(job_item,"gpu_running_jobs")+self._get_number_value(job_item,"gpu_pending_jobs")

        self.record_time = job_item["update_time"] if "update_time" in job_item else datetime.now()

        self.table = conf.DB["table"]

    def _get_number_value(self,item,key,type="int"):
        if type=="int":
            return int(item[key]) if key in item else 0;
        else:
            return float(item[key]) if key in item else 0.0;

    def insert_str(self):
        return "insert into {table} (record_time,job,user,cpu_user,cpu_job,cpu_node,\
            cpu_core,gpu_user,gpu_job,gpu_node,gpu_core,node,core,running_job,\
            waiting_job,cpu_running_job,cpu_waiting_job,gpu_running_job, \
            gpu_waiting_job,pue,power,gpu_gpu,error_node,error_core, \
            cpu_error_node,gpu_error_node,cpu_error_core,gpu_error_core, \
            gpu_error_gpu,all_gpu,all_cpu_node,all_gpu_node,all_cpu_core,all_gpu_core,all_core,all_node) \
            value ('{record_time}',{job},{user},{cpu_user},{cpu_job},{cpu_node},\
            {cpu_core},{gpu_user},{gpu_job},{gpu_node},{gpu_core},{node},{core},\
            {running_job},{waiting_job},{cpu_running_job},{cpu_waiting_job}, \
            {gpu_running_job},{gpu_waiting_job},{pue},{power},{gpu_gpu},{error_node},\
            {error_core},{cpu_error_node},{gpu_error_node},{cpu_error_core},\
            {gpu_error_core},{gpu_error_gpu},{all_gpu},{all_cpu_node},{all_gpu_node},\
            {all_cpu_core},{all_gpu_core},{all_core},{all_node})".format(
            error_node = self.error_node,
            error_core = self.error_core,
            cpu_error_node = self.cpu_error_node,
            gpu_error_node = self.gpu_error_node,
            cpu_error_core = self.cpu_error_core,
            gpu_error_core = self.gpu_error_core,
            gpu_error_gpu = self.gpu_error_gpu,
            all_gpu = self.all_gpu,
            all_cpu_node = self.all_cpu_node,
            all_gpu_node = self.all_gpu_node,
            all_cpu_core = self.all_cpu_core,
            all_gpu_core = self.all_gpu_core,
            job = self.job,
            user = self.user,
            cpu_user = self.cpu_user,
            cpu_job = self.cpu_job,
            gpu_user = self.gpu_user,
            gpu_job = self.gpu_job,
            gpu_node = self.gpu_node,
            gpu_core = self.gpu_core,
            cpu_node = self.cpu_node,
            cpu_core = self.cpu_core,
            node = self.node,
            core = self.core,
            running_job = self.running_job,
            waiting_job = self.waiting_job,
            cpu_running_job = self.cpu_running_job,
            cpu_waiting_job = self.cpu_waiting_job,
            gpu_running_job = self.gpu_running_job,
            gpu_waiting_job = self.gpu_waiting_job,
            pue = self.pue,
            power = self.power,
            gpu_gpu = self.gpu_gpu,
            all_node = self.all_node,
            all_core = self.all_core,
            record_time = self.record_time,
            table = self.table
        )




def crond(conf):
    db = Mysql(conf.DB)
    hd = HistoryData(conf)
    db.execute(hd.insert_str())
    db.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cluster', default=config.CLUSTER, help="Cluster name")
    parser.add_argument('-t', '--table', default=config.DB["table"],help="Database table name")

    args = parser.parse_args()
    config.CLUSTER = args.cluster
    config.DB["table"] = args.table

    crond(config)
