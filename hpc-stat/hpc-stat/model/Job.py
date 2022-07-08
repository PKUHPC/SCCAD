#coding=utf-8
import time, requests
from lib import util

class SubmittedJob:
    def __init__(self,info_dict={}):
        self.partition = info_dict['partition']  if 'partition' in info_dict else '-'
        self.job_name = info_dict['job_name']  if 'job_name' in info_dict else '-'
        self.user = self.privacy(info_dict['user'])  if 'user' in info_dict else '-'
        self.state = info_dict['state']  if 'state' in info_dict else '-'
        self.time_used = info_dict['time_used']  if 'time_used' in info_dict else '00:00:00'
        self.nodes = info_dict['nodes']  if 'nodes' in info_dict else '00:00:00'
        self.info = info_dict['info'].strip("()")  if 'info' in info_dict else '-'
        self.account = self.privacy(info_dict['account'])  if 'account' in info_dict else '-'
        self.cpus = info_dict['cpus']  if 'cpus' in info_dict else '-'
        self.qos = info_dict['qos']  if 'qos' in info_dict else '-'
        self.time_submit = info_dict['time_submit']  if 'time_submit' in info_dict else '-'
        self.scheduled_nodes = info_dict['scheduled_nodes']  if 'scheduled_nodes' in info_dict else '-'
        self.timestamp_submit = int(info_dict['timestamp_submit'])  if 'timestamp_submit' in info_dict else 0
        self.time_used_seconds = int(info_dict['time_used_seconds'])  if 'time_used_seconds' in info_dict else 0
        self.time_wait = int(time.time()) - self.timestamp_submit if self.timestamp_submit > 0 and self.time_used_seconds == 0 else 0

    @property
    def index_name(self):
        if self.job_name == "bash":
            return self.job_name +" - "+ self.user
        else:
            return self.job_name

    def privacy(self,str):
        if len(str) > 6:
            return str[:-6]+"****"+str[-2:]
        else:
            return str

class SubmittedJobs:
    def __init__(self,job_list=[]):
        self.job_list = job_list
        self.running_job_num = len(self.running_list)
        self.running_user_num = len(set([x.user for x in self.running_list]))
        self.pending_job_num = len(self.pending_list)
        self.pending_user_num = len(set([x.user for x in self.pending_list]))

    def init_from_squeue_ret(self,ret):
        self.job_list = [SubmittedJob(x) for x in ret]
        self.running_job_num = len(self.running_list)
        self.running_user_num = len(set([x.user for x in self.running_list]))
        self.pending_job_num = len(self.pending_list)
        self.pending_user_num = len(set([x.user for x in self.pending_list]))

    @property
    def jobs(self):
        return [x.__dict__ for x in self.job_list]

    @property
    def pending_list(self):
        return sorted([x for x in self.job_list if x.time_used_seconds==0], key = lambda x : x.time_wait, reverse=True)

    @property
    def running_list(self):
        return sorted([x for x in self.job_list if x.time_used_seconds>0], key = lambda x : x.time_used_seconds, reverse=True)

    def top_list(self,num=5):
        return {
            "pending_list" :[{x.index_name : util.get_readable_seconds_time(x.time_wait)} for x in self.pending_list[:5]],
            "running_list" :[{x.index_name : util.get_readable_seconds_time(x.time_used_seconds)} for x in self.running_list[:5]]
        }
