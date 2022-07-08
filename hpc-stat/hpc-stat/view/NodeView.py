from flask import render_template,jsonify
from flask_babel import _

from abc import abstractmethod
from local import setting
import requests,ast

from model.Node import *
from view.BasicView import BasicView

class NodeView(BasicView):
    NodeCls = None
    def index(self):
        return render_template("{}/node.html".format(self.cluster),page=self.page())

    def page(self):
        return {
            "cluster" : self.cluster,
            "cluster_show" : self.cluster,
        }

    def nodes(self):
        nodes_ret = self.r.redis.hgetall(self.cluster+"_nodes")
        all_list = []
        for node_str in nodes_ret.values():
            node = ast.literal_eval(node_str)
            res_suffix = _("GPU CARD") if node["GPU"]  else  _("CPU CORE")
            node["res_tot"] = "{count} {res_type}".format(count=node["res_tot"],res_type=res_suffix)
            node["res_alloc"] = "{count} {res_type}".format(count=node["res_alloc"],res_type=res_suffix)
            all_list.append(node)
        return jsonify({"data":all_list})

class HPC01NodeView(NodeView):
    NodeCls = HPC01Node
    cluster = "hpc01"
