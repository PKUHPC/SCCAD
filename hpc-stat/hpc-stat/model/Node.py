from flask_babel import _

class Node:
    def __init__(self,info_dict={}):
        self.name = info_dict['name']  if 'name' in info_dict else '-'
        self.state = info_dict['state']  if 'state' in info_dict else '-'
        self.mem_tot = int(info_dict['mem_tot'])  if 'mem_tot' in info_dict else 0
        self.mem_alloc = int(info_dict['mem_alloc'])  if 'mem_alloc' in info_dict else 0
        self.cpu_tot = int(info_dict['cpu_tot'])  if 'cpu_tot' in info_dict else 0
        self.gpu_tot = int(info_dict['gpu_tot'])  if 'gpu_tot' in info_dict and info_dict['gpu_tot'] else 0
        self.gpu_alloc = int(info_dict['gpu_alloc'])  if 'gpu_alloc' in info_dict else 0

        # print(self.name,self.state,self.state.strip() != "ALLOCATED+DRAIN" and self.state.strip() != "MIXED+DRAIN" and"DRAIN" in self.state)

        # 坏节点判定：
        if   "DOWN" in self.state or ( \
                self.state.strip() != "ALLOCATED+DRAIN" and \
                self.state.strip() != "MIXED+DRAIN" and \
                self.state.strip() != "IDLE+COMPLETING+DRAIN" and\
                "DRAIN" in self.state) :

            self.cpu_load = 0
            self.cpu_err = self.cpu_tot
            self.cpu_alloc = 0
            self.gpu_err = self.gpu_tot
        else:
            if info_dict['cpu_load'] == "N/A":
                self.cpu_load = 0
            else:
                self.cpu_load = float(info_dict['cpu_load'])  if 'cpu_load' in info_dict else 0
            self.cpu_err = int(info_dict['cpu_err'])  if 'cpu_err' in info_dict else 0
            self.cpu_alloc = int(info_dict['cpu_alloc'])  if 'cpu_alloc' in info_dict else 0
            self.gpu_err = int(info_dict['gpu_err'])  if 'gpu_err' in info_dict else 0

    def get_partition(self):
        return "CPU"

    def get_usage_stat(self):
        if self.cpu_err > 0:
            return "Error"
        elif self.cpu_alloc > 0 and self.cpu_alloc < self.cpu_tot:
            return "Running"
        elif self.cpu_alloc == 0:
            return "Available"
        elif self.cpu_alloc == self.cpu_tot:
            return "Busy"

class HPC01Node(Node):
    def get_partition(self):
        if self.name[:3].upper() == "GPU":
            return "GPU"
        else:
            return "CPU"

class Nodes:
    def __init__(self,nodes_list=[]):
        self.cpu_alloc = 0
        self.cpu_error = 0
        self.cpu_free = 0
        self.gpu_alloc = 0
        self.gpu_error = 0
        self.gpu_free = 0
        self.node_error = 0
        self.node_running = 0
        self.node_available = 0
        self.node_busy = 0
        self.mem_tot = 0
        self.mem_alloc = 0
        self.cpu_avg_load = 0.0
        self.nodes_list = nodes_list

        for node in nodes_list:
            self.cpu_alloc += node.cpu_alloc
            self.cpu_error += node.cpu_err
            self.cpu_free += node.cpu_tot-node.cpu_err-node.cpu_alloc
            self.gpu_alloc += node.gpu_alloc
            self.gpu_free += node.gpu_tot-node.gpu_err-node.gpu_alloc
            self.gpu_error += node.gpu_err


            if node.get_usage_stat() == "Error":
                self.node_error += 1
            elif node.get_usage_stat() == "Running":
                self.node_running += 1
            elif node.get_usage_stat() == "Available":
                self.node_available += 1
            elif node.get_usage_stat() == "Busy":
                self.node_busy += 1

    @property
    def cpu_tot(self):
        return self.cpu_free + self.cpu_error + self.cpu_alloc

    @property
    def node_tot(self):
        return self.node_error + self.node_running + self.node_available + self.node_busy

    @property
    def gpu_tot(self):
        return self.gpu_error +  self.gpu_alloc + self.gpu_free

    def get_usage(self):
        return {
            "cpu_alloc" : self.cpu_alloc ,
            "cpu_error" : self.cpu_error ,
            "cpu_free" : self.cpu_free ,
            "cpu_tot" : self.cpu_tot,
            "gpu_alloc" : self.gpu_alloc ,
            "gpu_error" : self.gpu_error ,
            "gpu_free" : self.gpu_free ,
            "gpu_tot" : self.gpu_tot,
            "node_error" : self.node_error ,
            "node_running" : self.node_running ,
            "node_available" : self.node_available ,
            "node_busy" : self.node_busy ,
            "node_tot" : self.node_tot,
            "mem_tot" : self.mem_tot,
            "mem_alloc" : self.mem_alloc,
            "cpu_avg_load" : self.cpu_avg_load,
            "lan_error" : _("Error"),
            "lan_available" : _("Available"),
            "lan_running" : _("Running")
        }
