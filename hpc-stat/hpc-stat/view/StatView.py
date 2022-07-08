from flask import render_template,jsonify,url_for
from flask_babel import _
from abc import abstractmethod
from local import setting
import time,requests,ast

from model.Node import *
from model.Job import SubmittedJobs
from model.History import *
from model.HistoryDB import HistoryDB
from view.BasicView import BasicView

class StatView(BasicView):
    HistoryCls = None
    HistoryTable = setting.MYSQL["table"]["history"]

    def index(self):

        return render_template(
            "{}/stat.html".format(self.cluster), page=self.page()
        )

    def nodes(self):

        try:
            nodes=self.r.redis.hgetall(self.cluster+"_cluster_node")
            cpu_ret = {
                "cpu_alloc" : nodes["cpu_cpu_alloc"] ,
                "cpu_error" : nodes["cpu_cpu_error"] ,
                "cpu_free" : nodes["cpu_cpu_free"] ,
                "cpu_tot" : nodes["cpu_cpu_tot"] ,
                "node_error" : nodes["cpu_node_error"] ,
                "node_running" : nodes["cpu_node_running"] ,
                "node_available" : nodes["cpu_node_available"] ,
                "node_busy" : "" ,
                "node_tot" : nodes["cpu_node_tot"] ,
                "lan_error" : _("Error"),
                "lan_available" : _("Available"),
                "lan_running" : _("Running")
            }
            gpu_ret = {
                "gpu_alloc" : nodes["gpu_card_alloc"] ,
                "gpu_error" : nodes["gpu_card_error"] ,
                "gpu_free" : nodes["gpu_card_free"] ,
                "gpu_tot" : nodes["gpu_card_tot"] ,
                "node_error" : nodes["gpu_node_error"] ,
                "node_running" : nodes["gpu_node_running"] ,
                "node_available" : nodes["gpu_node_available"] ,
                "node_busy" : "" ,
                "node_tot" : nodes["gpu_node_tot"] ,
                "lan_error" : _("Error"),
                "lan_available" : _("Available"),
                "lan_running" : _("Running")
            }
            all_ret = {
                "cpu_alloc" : nodes["all_cpu_alloc"] ,
                "cpu_error" : nodes["all_cpu_error"] ,
                "cpu_free" : nodes["all_cpu_free"] ,
                "cpu_tot" : nodes["all_cpu_tot"] ,
                "node_error" : nodes["all_node_error"] ,
                "node_running" : nodes["all_node_running"] ,
                "node_available" : nodes["all_node_available"] ,
                "node_busy" : "" ,
                "node_tot" : nodes["all_node_tot"] ,
                "lan_error" : _("Error"),
                "lan_available" : _("Available"),
                "lan_running" : _("Running")
            }
            ret = {
                "cpu_nodes" : cpu_ret,
                "gpu_nodes" : gpu_ret,
                "all_nodes" : all_ret
            }

        except:
            error_ret = {
                "cpu_alloc" :0 ,
                "cpu_error" : 0 ,
                "cpu_free" : 0 ,
                "cpu_tot" : 0 ,
                "gpu_alloc" : 0 ,
                "gpu_error" : 0 ,
                "gpu_free" : 0 ,
                "gpu_tot" : 0 ,
                "node_error" : 0 ,
                "node_running" : 0 ,
                "node_available" : 0 ,
                "node_busy" : 0 ,
                "node_tot" : 0 ,
                "lan_error" : _("Error"),
                "lan_available" : _("Available"),
                "lan_running" : _("Running")
            }
            ret = {
                "cpu_nodes" : error_ret,
                "gpu_nodes" : error_ret,
                "all_nodes" : error_ret
            }

        return ret

    def jobs(self):

        try:
            jobs=self.r.redis.hgetall(self.cluster+"_cluster_job")
            ret = {
                "job_info" : [
                    {_("Running Job") : jobs["running_jobs"]},
                    {_("Pending Job") : jobs["pending_jobs"]},
                    {_("Running User") : jobs["running_users"]},
                    {_("Pending User") : jobs["pending_users"]}
                ],
                "pending_list" : ast.literal_eval(jobs["pengding_top5"]),
                "running_list" : ast.literal_eval(jobs["running_top5"])
            }
        except:
            ret = {
                "job_info" : [
                    {_("Running Job") : "NULL"},
                    {_("Pending Job") : "NULL"},
                    {_("Running User") : "NULL"},
                    {_("Pending User") : "NULL"}
                ],
                "pending_list" : [],
                "running_list" : []
            }
        return ret

    def page(self):

        ret = {
            "cluster" : self.cluster,
            "cluster_show" : self.cluster,
            "today" : time.strftime('%Y-%m-%d',time.localtime(time.time())),
            "nodes" : []
        }
        page_info = []
        page_info.append( {
            "name":_(self.cluster_name),
            "id":"all-info",
            "size" : 12,
            "colors":{
                "node" : ['#ae0001','#daa013','#b8860b'],
                "core" : ['#ae0001','#021496','#000033'],
            }
        })
        page_info.append( {
            # "name":"计算节点",
            "name":_("CPU Nodes"),
            "id":"cpu-info",
            "size" : 6,
            "colors":{
                "node" : ['#ae0001','#daa013','#b8860b'],
                "core" : ['#ae0001','#021496','#000033'],
            }
        })
        page_info.append( {
            # "name":"GPU节点",
            "name":_("GPU Nodes"),
            "id":"gpu-info",
            "size" : 6,
            "colors":{
                "node" : ['#ae0001','#daa013','#b8860b'],
                "core" : ['#ae0001','#021496','#000033'],
            }
        })
        ret["nodes"] = page_info
        return ret
        return ret

    def pue(self):
        return {"power": 0,"pue": 0}

    def overall(self):
        for subclass in Stat.__subclasses__():
            stat = subclass()

    def async_data(self):
        ret = {
            "job" : self.jobs(),
            "node" : self.nodes(),
            "pue" : self.pue()
        }
        return jsonify(ret)

    def history(self,type="nodeuserpue",period="2-DAY"):
        v = period.split("-")
        if len(v) == 2:
            number = v[0] if v[0].isdigit() else "2"
            span = v[1] if v[1] in ['DAY','MONTH'] else "DAY"
        else:
            return jsonify({"job":"","user":"","node":"","core":"","pue":"","power":""})

        hist_db = HistoryDB(number,span,setting.MYSQL,self.HistoryTable)
        hist_db.retrive_period()

        hist_list = {
            "node" : hist_db.node_list,
            "user" : hist_db.user_list,
            "pue" : hist_db.pue_list
        }
        hist = self.HistoryCls(hist_list)

        ret = {
            "job" : hist.job,
            "user" : hist.user,
            "running_job" : hist.running_job,
            "waiting_job" : hist.waiting_job,
            "node" : hist.node,
            "core" : hist.core,
            "gpu_gpu" : hist.gpu_gpu,
            "pue" : hist.pue,
            "power" : hist.power,
            "lan":{
                "node_usage":_("Node Usage"),
                "core_usage":_("Core Usage"),
                "gpu_usage":_("GPU Usage"),
                "user_count":_("User"),
                "job_count":_("Job"),
                "running_job_count":_("Running Job"),
                "waiting_job_count":_("Waiting Job"),
                "job_count":_("Job"),
                "pue":_("PUE"),
                "power":_("POWER")
            }
        }
        return jsonify(ret)

    def history_check(self,type,start_date="2018-01-01",end_date="2018-01-02"):
        start_dates = start_date.split("-")
        end_dates = end_date.split("-")
        if len(start_dates) !=3 or len(end_dates) !=3:
            for item in start_dates+end_dates:
                if not item.isdigit():
                    return self.history()

        hist_req = requests.get(self.api_server + setting.api['history_check'].format(
            type=type,start_date=start_date,end_date=end_date))

        if hist_req.status_code == 200:
            hist = self.HistoryCls(hist_req.json())
        else:
            hist = self.HistoryCls([])

        ret = {
            "job" : hist.job,
            "user" : hist.user,
            # "cpu_job" : hist.cpu_job,
            # "cpu_user" : hist.cpu_user,
            # "gpu_user" : hist.gpu_user,
            # "gpu_job" : hist.gpu_job,
            "running_job" : hist.running_job,
            "waiting_job" : hist.waiting_job,
            # "cpu_waiting_job" : hist.cpu_waiting_job,
            # "gpu_waiting_job" : hist.gpu_waiting_job,
            # "cpu_running_job" : hist.cpu_running_job,
            # "gpu_running_job" : hist.gpu_running_job,
            "node" : hist.node,
            "core" : hist.core,
            # "cpu_node" : hist.cpu_node,
            # "cpu_core" : hist.cpu_core,
            # "gpu_node" : hist.gpu_node,
            # "gpu_core" : hist.gpu_core,
            "gpu_gpu" : hist.gpu_gpu,
            "pue" : hist.pue,
            "power" : hist.power,
            "lan":{
                "node_usage":_("Node Usage"),
                "core_usage":_("Core Usage"),
                "gpu_usage":_("GPU Usage"),
                "user_count":_("User"),
                "job_count":_("Job"),
                "running_job_count":_("Running Job"),
                "waiting_job_count":_("Waiting Job"),
                "pue":_("PUE"),
                "power":_("POWER")
            }
        }
        return jsonify(ret)

class HPC01StatView(StatView):

    cluster = "hpc01"
    cluster_name = "HPC 01"
    HistoryCls = HPC01History
