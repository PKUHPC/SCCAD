from local import config

import time,datetime,json

class JobInfo:
    def __init__(self):
        self.job_name = ""
        self.partition = ""
        self.user = ""
        self.state = ""
        self.time_used = ""
        self.nodes = ""
        self.account = ""
        self.cpus = ""
        self.qos = ""
        self.time_submit = ""
        self.scheduled_nodes = ""

    def init_from_slurm(self,slurm_str):
        slurm_str_list = slurm_str.split("__x__x__")
        self.partition = slurm_str_list[0]
        self.job_name = slurm_str_list[1]
        self.user = slurm_str_list[2]
        self.state = slurm_str_list[3]
        self.time_used = slurm_str_list[4]
        self.nodes = slurm_str_list[5]
        self.info = slurm_str_list[6].strip("()")
        self.account = slurm_str_list[7]
        self.cpus = slurm_str_list[8]
        self.qos = slurm_str_list[9]
        self.time_submit = slurm_str_list[10]
        self.scheduled_nodes = slurm_str_list[11]

        timestamp_submit = time.mktime(time.strptime(self.time_submit, '%Y-%m-%dT%H:%M:%S'))
        self.timestamp_submit = int(timestamp_submit)

        day_list = self.time_used.split("-")
        time_used = 0
        if len(day_list) == 2:
            if len(day_list[0]) <= 2:
                time_used += int(day_list[0])*24*3600
        time_list = day_list[::-1]
        time_list_items = time_list[0].split(":")
        for index,item in enumerate(time_list_items[::-1]):
            time_used += int(item)*(60**index)
        self.time_used_seconds = time_used

        self.time_wait = int(time.time()) - self.timestamp_submit if self.timestamp_submit > 0 and self.time_used_seconds == 0 else 0

    def redis_job_info(self):
        job_info = self.__dict__
        return json.dumps(job_info)

    def get_readable_seconds_time(self,time_seconds):
        if time_seconds < 60:
            return "{:.0f} seconds".format(time_seconds)
        elif time_seconds < 3600:
            return "{:.2f} minutes".format(time_seconds/60)
        else:
            return "{:.2f} hours".format(time_seconds/3600)


class SlurmJobInfo:
    def __init__(self,slurm_ret_str):
        self.job_list = []
        item_list = slurm_ret_str.split('\n')
        for item in item_list:
            if item.strip() == "":
                continue
            job = JobInfo()
            job.init_from_slurm(item)
            self.job_list.append(job)

    @property
    def pending_list(self):
        return sorted([x for x in self.job_list if x.time_used_seconds==0], key = lambda x : x.time_wait, reverse=True)

    @property
    def running_list(self):
        return sorted([x for x in self.job_list if x.time_used_seconds>0], key = lambda x : x.time_used_seconds, reverse=True)

    # 获取所有作业的详细信息，返回的作业信息为字符串，可以直接插入redis中
    # 作业间的分隔符为 ||||
    def get_job_array(self):
        ret = {}
        ret["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ret["running_jobs"] = len([x for x in self.job_list if x.state == "RUNNING"])
        ret["pending_jobs"] = len([x for x in self.job_list if x.state == "PENDING"])
        ret["running_users"] = len(set([x.user for x in self.job_list if x.state == "RUNNING"]))
        ret["pending_users"] = len(set([x.user for x in self.job_list if x.state == "PENDING"]))
        jobs = []
        for job in self.job_list:
            jobs.append(job.redis_job_info())
        ret["jobs"] = "||||".join(jobs)
        return ret

    def get_cluster_job_info(self):
        ret = {}

        ret["running_jobs"] = len([x for x in self.job_list if x.state == "RUNNING"])
        ret["pending_jobs"] = len([x for x in self.job_list if x.state == "PENDING"])
        ret["cpu_running_jobs"] = len([x for x in self.job_list if x.state == "RUNNING" and x.partition not in config.GPU_PARTITION])
        ret["cpu_pending_jobs"] = len([x for x in self.job_list if x.state == "PENDING" and x.partition not in config.GPU_PARTITION])
        ret["gpu_running_jobs"] = len([x for x in self.job_list if x.state == "RUNNING" and x.partition in config.GPU_PARTITION])
        ret["gpu_pending_jobs"] = len([x for x in self.job_list if x.state == "PENDING" and x.partition in config.GPU_PARTITION])

        ret["running_users"] = len(set([x.user for x in self.job_list if x.state == "RUNNING"]))
        ret["pending_users"] = len(set([x.user for x in self.job_list if x.state == "PENDING"]))
        ret["users"] = len(set([x.user for x in self.job_list]))
        ret["cpu_running_users"] = len(set([x.user for x in self.job_list if x.state == "RUNNING" and x.partition not in config.GPU_PARTITION]))
        ret["cpu_pending_users"] = len(set([x.user for x in self.job_list if x.state == "PENDING" and x.partition not in config.GPU_PARTITION]))
        ret["cpu_users"] = len(set([x.user for x in self.job_list if x.partition not in config.GPU_PARTITION]))
        ret["gpu_running_users"] = len(set([x.user for x in self.job_list if x.state == "RUNNING" and x.partition in config.GPU_PARTITION]))
        ret["gpu_pending_users"] = len(set([x.user for x in self.job_list if x.state == "PENDING" and x.partition in config.GPU_PARTITION]))
        ret["gpu_users"] = len(set([x.user for x in self.job_list if x.partition in config.GPU_PARTITION]))

        ret["pengding_top5"] = json.dumps([{x.job_name : x.get_readable_seconds_time(x.time_wait)} for x in self.pending_list[:5]])
        ret["running_top5"] = json.dumps([{x.job_name : x.get_readable_seconds_time(x.time_used_seconds)} for x in self.running_list[:5]])

        ret["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return ret

    def get_cluster_job_brief(self):
        ret = {}

        ret["job_running"] = len([x for x in self.job_list if x.state == "RUNNING"])
        ret["job_pending"] = len([x for x in self.job_list if x.state == "PENDING"])

        return ret
