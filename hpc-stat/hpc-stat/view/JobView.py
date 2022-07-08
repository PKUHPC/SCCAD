from flask import render_template,jsonify

from abc import abstractmethod
from local import setting
import requests,ast

from model.Job import SubmittedJobs
from view.BasicView import BasicView
from lib import util

class JobView(BasicView):

    def page(self):

        return {
            "cluster" : self.cluster,
            "cluster_show" : self.cluster,
        }

    def index(self):

        return render_template("{}/job.html".format(self.cluster),page=self.page())

    def jobs(self):

        jobs_ret = self.r.redis.hgetall(self.cluster+"_jobs")
        table_jobs = []
        jobs = jobs_ret["jobs"].split("||||")
        for job_str in jobs:
            job = ast.literal_eval(job_str)
            item = {
                'name' : job["job_name"],
                'account' : job["account"][:-6]+"****"+job["account"][-2:] if len(job["account"]) > 6 else job["account"],
                'user' : job["user"][:-6]+"****"+job["user"][-2:] if len(job["user"]) > 6 else job["user"],
                'partition' : job["partition"],
                'qos' : job["qos"],
                'node' : job["nodes"],
                'cpu' : job["cpus"],
                'state' : job["state"],
                'time_used' : util.get_readable_seconds_time(job['time_used_seconds']),
                'time_used_sort' : job["time_used_seconds"] if job["state"] == "RUNNING" else job["time_wait"],
                'info' : ", ".join(job["info"].split(","))
            }
            item['time_used'] = util.get_readable_seconds_time(max(0,item['time_used_sort']))
            table_jobs.append(item)


        ret_dict = {
            "data" : table_jobs,
            "running_job_num" : jobs_ret["running_jobs"],
            "pending_job_num" : jobs_ret["pending_jobs"],
            "running_user_num" : jobs_ret["running_users"],
            "pending_user_num" : jobs_ret["pending_users"]
        }

        return jsonify(ret_dict)


class HPC01JobView(JobView):
    cluster = "hpc01"
