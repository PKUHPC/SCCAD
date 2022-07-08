import time

class History:
    NODE_NUM = 1.00
    CORE_NUM = 1.00
    GPU_NUM = 1.00

    def __init__(self,hist_info=[]):
        self.job = []
        self.user = []
        self.cpu_job = []
        self.cpu_user = []
        self.gpu_user = []
        self.gpu_job = []
        self.running_job = []
        self.waiting_job = []
        self.cpu_waiting_job = []
        self.gpu_waiting_job = []
        self.cpu_running_job = []
        self.gpu_running_job = []
        self.node = []
        self.core = []
        self.cpu_node = []
        self.cpu_core = []
        self.gpu_node = []
        self.gpu_core = []
        self.gpu_gpu = []
        self.pue = []
        self.power = []
        self.hist_info = hist_info
        self.job_user_init()
        self.node_core_init()
        self.pue_power_init()
        self.sort_history_data()

    def job_user_init(self):
        if len(self.hist_info)==0:
            return
        for job_user in self.hist_info['user']:
            if "job" in job_user:
                self.job.append({
                    "name":self._format_time_for_chart(job_user['record_time']),
                    "value":[self._format_time_for_chart(job_user['record_time']), int(job_user['job'])]
                })
            if "user" in job_user:
                self.user.append({
                    "name":self._format_time_for_chart(job_user['record_time']),
                    "value":[self._format_time_for_chart(job_user['record_time']), int(job_user['user'])]
                })
            if "running_job" in job_user:
                self.running_job.append({
                    "name":self._format_time_for_chart(job_user['record_time']),
                    "value":[self._format_time_for_chart(job_user['record_time']), int(job_user['running_job'])]
                })
            if "waiting_job" in job_user:
                self.waiting_job.append({
                    "name":self._format_time_for_chart(job_user['record_time']),
                    "value":[self._format_time_for_chart(job_user['record_time']), int(job_user['waiting_job'])]
                })

    def node_core_init(self):
        if len(self.hist_info)==0:
            return
        for node_core in self.hist_info['node']:
            max_node = node_core["all_node"] if "all_node" in node_core and node_core["all_node"] > 0 else self.NODE_NUM
            max_core = node_core["all_core"] if "all_core" in node_core and node_core["all_core"] > 0 else self.CORE_NUM
            max_gpu = node_core["all_gpu"] if "all_gpu" in node_core and node_core["all_gpu"] > 0 else self.GPU_NUM

            if "node" in node_core:
                self.node.append({
                    "name":self._format_time_for_chart(node_core['record_time']),
                    "value":[self._format_time_for_chart(node_core['record_time']), round(float(node_core['node'])/max_node*100,2)]
                })
            if "core" in node_core:
                self.core.append({
                    "name":self._format_time_for_chart(node_core['record_time']),
                    "value":[self._format_time_for_chart(node_core['record_time']),round(float(node_core['core'])/max_core*100,2)]
                })
            if "gpu_gpu" in node_core:
                self.gpu_gpu.append({
                    "name":self._format_time_for_chart(node_core['record_time']),
                    "value":[self._format_time_for_chart(node_core['record_time']),round(float(node_core['gpu_gpu'])/max_gpu*100,2)]
                })

    def pue_power_init(self):
        if len(self.hist_info)==0:
            return
        for pue_power in self.hist_info['pue']:
            if "pue" in pue_power:
                self.pue.append({
                    "name":self._format_time_for_chart(pue_power['record_time']),
                    "value":[self._format_time_for_chart(pue_power['record_time']), pue_power['pue']]
                })
            if "power" in pue_power:
                self.power.append({
                    "name":self._format_time_for_chart(pue_power['record_time']),
                    "value":[self._format_time_for_chart(pue_power['record_time']), pue_power['power']]
                })

    def _format_time_for_chart(self,timestamp):
        return time.strftime("%Y/%m/%d %H:%M",time.localtime(int(timestamp)))

    def sort_history_data(self):
        self.job.sort(key=lambda x:x["name"])
        self.user.sort(key=lambda x:x["name"])
        self.running_job.sort(key=lambda x:x["name"])
        self.waiting_job.sort(key=lambda x:x["name"])
        self.node.sort(key=lambda x:x["name"])
        self.core.sort(key=lambda x:x["name"])
        self.gpu_gpu.sort(key=lambda x:x["name"])
        self.pue.sort(key=lambda x:x["name"])
        self.power.sort(key=lambda x:x["name"])

class HPC01History(History):
    NODE_NUM = 101.00
    CORE_NUM = 2848.00
