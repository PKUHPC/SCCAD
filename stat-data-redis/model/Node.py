from local import config

import re,datetime,json

# 单个节点信息
class NodeInfo:
    def __init__(self,name):
        self.name=name
        self.cpu_alloc=0
        self.cpu_error=0
        self.cpu_tot=0
        self.cpu_load=0
        self.state=""
        self.mem_alloc=0
        self.mem_free=0
        self.mem_tot=0
        self.gpu_tot=0
        self.gpu_error=0
        self.gpu_alloc=0
        self.res_usage=0
        self.partitions=""

    # 从slurm 返回字符串中解析节点信息
    def init_from_slurm(self,slurm_str):
        p_nodename = re.compile(r'NodeName=\S*')
        p_cpualloc = re.compile(r'CPUAlloc=\S*')
        p_cpuerr = re.compile(r'CPUErr=\S*')
        p_cputot = re.compile(r'CPUTot=\S*')
        p_cpuload = re.compile(r'CPULoad=\S*')
        p_memtot= re.compile(r'RealMemory=\S*')
        p_memallc = re.compile(r'AllocMem=\S*')
        p_state = re.compile(r'State=\S*')
        p_gputot = re.compile(r'Gres=gpu\S*')
        p_gpualloc = re.compile(r'AllocTRES=\S*gres/gpu=\S*')
        p_partitions = re.compile(r'Partitions=\S*')

        self.name = self.parse_from_re(p_nodename.search(slurm_str),type="str")
        self.cpu_alloc = int(self.parse_from_re(p_cpualloc.search(slurm_str)))
        self.cpu_error = int(self.parse_from_re(p_cpuerr.search(slurm_str)))
        self.cpu_tot = int(self.parse_from_re(p_cputot.search(slurm_str)))
        self.cpu_load = self.parse_from_re(p_cpuload.search(slurm_str))
        self.mem_tot = self.parse_from_re(p_memtot.search(slurm_str))
        self.mem_alloc = self.parse_from_re(p_memallc.search(slurm_str))
        self.state = self.parse_from_re(p_state.search(slurm_str),type="str")
        self.partitions = self.parse_from_re(p_partitions.search(slurm_str),type="str")
        self.gpu_tot = int(self.parse_from_re(p_gputot.search(slurm_str),type="int",split_str=":"))
        self.gpu_alloc = int(self.parse_from_regpu(p_gpualloc.search(slurm_str)))

        if   "DOWN" in self.state or ( \
                self.state.strip() != "ALLOCATED+DRAIN" and \
                self.state.strip() != "MIXED+DRAIN" and \
                self.state.strip() != "IDLE+COMPLETING+DRAIN" and\
                "DRAIN" in self.state) :

            self.cpu_load = 0
            self.cpu_error = self.cpu_tot
            self.cpu_alloc = 0
            self.gpu_error = self.gpu_tot

        else:
            if self.cpu_load == "N/A":
                self.cpu_load = 0
            if self.gpu_tot > 0:
                self.res_usage = round(self.gpu_alloc/self.gpu_tot * 100)
            elif self.cpu_tot > 0:

                self.res_usage = round(self.cpu_alloc/self.cpu_tot * 100)



    ## parse re.search returned key = value
    def parse_from_re(self,str_to_parse,type="int",split_str="="):
        if str_to_parse is None:
            return 0 if type=="int" else ""
        kv = str_to_parse.group(0).split(split_str)
        if len(kv) == 2:
            return kv[1].strip('\\n')
        elif len(kv) == 1:
            return 0 if type=="int" else ""

    ## parse GPU usage info
    def parse_from_regpu(self,str,type="int"):
        if str is None:
            return 0
        else:
            p_str = re.compile(r'gres/gpu=\S*')
            target_str = p_str.search(str.group(0))
            kv = target_str.group(0).split("=")
            if len(kv) == 2:
                return kv[1].strip('\\n')
            elif len(kv) == 1:
                return 0

    # 返回在redis中记录的节点详细信息
    def redis_node_info(self):
        node_info = {}
        node_info['name'] = self.name
        node_info['mem_tot'] = self.mem_tot
        node_info['mem_alloc'] = self.mem_alloc
        node_info['cpu_avg_load'] = self.cpu_load
        node_info['type'] = self.get_type()

        ## 解析节点资源使用情况，GPU记录GPU资源，CPU记录CPU资源
        if node_info['type'] in config.GPU_PARTITION:
            node_info['res_tot'] = self.gpu_tot
            node_info['res_alloc'] = self.gpu_alloc
            node_info['GPU'] = 1
        else:
            node_info['res_tot'] = self.cpu_tot
            node_info['res_alloc'] = self.cpu_alloc
            node_info['GPU'] = 0

        node_info["res_usage_sort"] = round(int(node_info["res_alloc"])/int(node_info["res_tot"]) * 100) if int(node_info["res_tot"]) > 0 else 0
        node_info["res_usage"] = str(node_info["res_usage_sort"])+"%"

        node_info['state'] = self.get_usage_stat()
        return json.dumps(node_info)

    # 返回节点类型，GPU、CPU
    def get_type(self):
        ## 解析节点类型
        ## 节点分区可能有多个，取第一个作为判断节点类型依据
        node_type = ""
        partition_list = self.partitions.split(",")
        for partition in partition_list:
            for type in config.NODE_TYPE:
                if partition in config.NODE_TYPE[type]:
                    node_type = type
        return node_type

    # 返回节点状态 Error、Running、Available、Busy
    def get_usage_stat(self):
        if self.cpu_error > 0:
            return "Error"

        if self.res_usage == 100:
            return "Busy"

        if self.res_usage > 0 and self.res_usage < 100:
            return "Running"

        if self.res_usage == 0:
            return "Available"

        return "Error"


# 集群节点信息
class SlurmNodeInfo:

    def __init__(self,slurm_ret_str):
        self.node_list = []
        if slurm_ret_str:
            item_list = slurm_ret_str.split("NodeName=")
            for item in item_list:
                node = NodeInfo("")
                node.init_from_slurm("NodeName="+item)
                if node.cpu_tot == 0 or node.name in config.EXCEPT_NODES:
                    continue
                self.node_list.append(node)

    # 返回所有节点的详细信息列表，可以直接插入到 redis
    def get_node_array(self):
        ret = {}
        for node in self.node_list:
            ret[node.name] = node.redis_node_info()
        return ret

    # 返回 stat 页面需要使用的节点信息，可以直接插入到 redis
    # 与 config.py 中的 NODE_TYPE 紧耦合
    #
    # 在通常情况下集群在显示了所有节点的统计信息之后只需要分 CPU 分区和 GPU 分区两个部分进行
    # 展示，但未名一号因为历史原因需要展示 CPU、GPU、BIG、GPU36 四部分。为此将 NODE_TYPE
    # 作为定义分区组的配置项，在这里将需要报团展示的分区进行分类。
    # 为了识别这些分区组中哪些属于 GPU 分区（展示卡的使用情况），设置了 GPU_PARTITION 来记
    # 录。
    # 分区组中的对应内容的值，将在前端项目中 StatView::nodes() 中进行解析
    def get_cluster_node_info(self):
        ret={}

        ret["all_cpu_alloc"] = sum([n.cpu_alloc for n in self.node_list])
        ret["all_cpu_error"] = sum([n.cpu_error for n in self.node_list])
        ret["all_cpu_tot"] = sum([n.cpu_tot for n in self.node_list])
        ret["all_cpu_free"] = ret["all_cpu_tot"] - ret["all_cpu_error"] - ret["all_cpu_alloc"]

        ret["all_node_tot"] = len(self.node_list)
        ret["all_node_error"] = len([n for n in self.node_list if n.get_usage_stat() == "Error"])
        ret["all_node_available"] = len([n for n in self.node_list if n.get_usage_stat() == "Available"])
        ret["all_node_running"] = ret["all_node_tot"] - ret["all_node_error"] - ret["all_node_available"]

        for partition_type in config.NODE_TYPE.keys():
            par = partition_type.lower()
            if partition_type in config.GPU_PARTITION:
                ret[par+"_card_tot"] = sum([n.gpu_tot for n in self.node_list if n.get_type() == partition_type])
                ret[par+"_card_alloc"] = sum([n.gpu_alloc for n in self.node_list if n.get_type() == partition_type])
                ret[par+"_card_error"] = sum([n.gpu_error for n in self.node_list if n.get_type() == partition_type])
                ret[par+"_card_free"] = ret[par+"_card_tot"] - ret[par+"_card_error"] - ret[par+"_card_alloc"]
            else:
                ret[par+"_cpu_tot"] = sum([n.cpu_tot for n in self.node_list if n.get_type() == partition_type])
                ret[par+"_cpu_alloc"] = sum([n.cpu_alloc for n in self.node_list if n.get_type() == partition_type])
                ret[par+"_cpu_error"] = sum([n.cpu_error for n in self.node_list if n.get_type() == partition_type])
                ret[par+"_cpu_free"] = ret[par+"_cpu_tot"] - ret[par+"_cpu_error"] - ret[par+"_cpu_alloc"]

            ret[par+"_node_tot"] = len([n for  n in self.node_list if n.get_type() == partition_type])
            ret[par+"_node_error"] = len([n for n in self.node_list if n.get_usage_stat() == "Error" and n.get_type() == partition_type])
            ret[par+"_node_available"] = len([n for n in self.node_list if n.get_usage_stat() == "Available" and n.get_type() == partition_type])
            ret[par+"_node_running"] = ret[par+"_node_tot"] - ret[par+"_node_error"] - ret[par+"_node_available"]

        ret["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return ret

    # 返回 stat 页面 brief 部分需要使用的节点信息，可以直接插入到 redis
    def get_cluster_node_brief(self):
        ret = {}

        all_cpu_tot = sum([n.cpu_tot for n in self.node_list])
        ret["core_running"] = round(100*sum([n.cpu_alloc for n in self.node_list])/all_cpu_tot)
        ret["core_error"] = round(100*sum([n.cpu_error for n in self.node_list])/all_cpu_tot)
        ret["core_available"] = 100 - ret["core_running"] - ret["core_error"]

        all_node_tot = len(self.node_list)
        if all_node_tot > 0:
            ret["node_error"] = round(100*len([n for n in self.node_list if n.get_usage_stat() == "Error"])/all_node_tot)
            ret["node_available"] = round(100*len([n for n in self.node_list if n.get_usage_stat() == "Available"])/all_node_tot)
            ret["node_running"] = 100 - ret["node_error"] - ret["node_available"]

        return ret



## FOR UNIT TEST
if __name__ == "__main__":
    slurm_str_1 = """
    NodeName=gpu01 Arch=x86_64 CoresPerSocket=6
       CPUAlloc=12 CPUErr=0 CPUTot=12 CPULoad=1.63
       AvailableFeatures=(null)
       ActiveFeatures=(null)
       Gres=gpu:2
       NodeAddr=gpu01 NodeHostName=gpu01 Version=17.11
       OS=Linux 3.10.0-514.el7.x86_64 #1 SMP Wed Oct 19 11:24:13 EDT 2016
       RealMemory=254720 AllocMem=254712 FreeMem=222467 Sockets=2 Boards=1
       State=ALLOCATED ThreadsPerCore=1 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
       Partitions=GPU
       BootTime=2021-01-30T17:47:22 SlurmdStartTime=2021-03-22T10:19:22
       CfgTRES=cpu=12,mem=254720M,billing=12,gres/gpu=2
       AllocTRES=cpu=12,mem=254712M,gres/gpu=2
       CapWatts=n/a
       CurrentWatts=0 LowestJoules=0 ConsumedJoules=0
       ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s
    """

    slurm_str_2 = """
    NodeName=gpu11 Arch=x86_64 CoresPerSocket=18
       CPUAlloc=2 CPUErr=0 CPUTot=36 CPULoad=2.83
       AvailableFeatures=(null)
       ActiveFeatures=(null)
       Gres=gpu:4
       NodeAddr=gpu11 NodeHostName=gpu11 Version=17.11
       OS=Linux 3.10.0-957.el7.x86_64 #1 SMP Thu Oct 4 20:48:51 UTC 2018
       RealMemory=384000 AllocMem=21332 FreeMem=355131 Sockets=2 Boards=1
       State=MIXED ThreadsPerCore=1 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
       Partitions=GPU36
       BootTime=2020-10-20T09:24:10 SlurmdStartTime=2021-03-22T10:19:22
       CfgTRES=cpu=36,mem=375G,billing=36,gres/gpu=4
       AllocTRES=cpu=2,mem=21332M,gres/gpu=2
       CapWatts=n/a
       CurrentWatts=0 LowestJoules=0 ConsumedJoules=0
       ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s
    """

    slurm_str_3 = """
    NodeName=gpu13 Arch=x86_64 CoresPerSocket=18
       CPUAlloc=0 CPUErr=0 CPUTot=36 CPULoad=0.01
       AvailableFeatures=(null)
       ActiveFeatures=(null)
       Gres=gpu:4
       NodeAddr=gpu13 NodeHostName=gpu13 Version=17.11
       OS=Linux 3.10.0-957.el7.x86_64 #1 SMP Thu Oct 4 20:48:51 UTC 2018
       RealMemory=384000 AllocMem=0 FreeMem=305684 Sockets=2 Boards=1
       State=IDLE ThreadsPerCore=1 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
       Partitions=GPU36
       BootTime=2021-01-30T17:46:29 SlurmdStartTime=2021-03-22T10:19:22
       CfgTRES=cpu=36,mem=375G,billing=36,gres/gpu=4
       AllocTRES=
       CapWatts=n/a
       CurrentWatts=0 LowestJoules=0 ConsumedJoules=0
       ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s
    """


    ni_1 = NodeInfo("1")
    ni_2 = NodeInfo("2")
    ni_3 = NodeInfo("3")

    ni_1.init_from_slurm(slurm_str_1)
    ni_2.init_from_slurm(slurm_str_2)
    ni_3.init_from_slurm(slurm_str_3)

    print(ni_1.gpu_alloc)
    print(ni_2.gpu_alloc)
    print(ni_3.gpu_alloc)
