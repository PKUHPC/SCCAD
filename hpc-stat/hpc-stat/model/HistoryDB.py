from lib.util import MySql

from math import ceil

class HistoryDB:
    MAX_ITEM = 4000
    def __init__(self,start_time,end_time,db_config,table):
        # 时间格式： 2018-07-04 08:05:02
        self.start_time = start_time
        self.end_time = end_time
        self.db_config = db_config
        self.table = table
        self._db = None
        self.pue_list = []
        self.node_list = []
        self.user_list = []

    @property
    def db(self):
        if self._db == None:
            self._db = MySql(self.db_config)
        return self._db

    def retrive(self):
        sql = "select * from {table} where \
            record_time > '{start_date}' and record_time <= '{end_date}' \
            order by record_time desc".format(
                start_date = self.start_time,
                end_date = self.end_time,
                table = self.table
            )
        self._execute(sql)
        self._db.close()

    def retrive_period(self):
        sql = "select * from {table} where \
            record_time >= DATE_SUB(now(), INTERVAL {period} {span}) \
            order by record_time desc".format(
                period = self.start_time,
                span = self.end_time,
                table = self.table
            )
        self._execute(sql)
        self._db.close()

    def _execute(self,sql):
        history_list = self.db.execute(sql)
        ret_list = history_list[::ceil(len(history_list)/self.MAX_ITEM+0.00001)]
        for item in ret_list:
            pue = {}
            if "pue" in item and item["pue"] != None:
                pue["pue"] = float(item["pue"])
            if "power" in item and item["power"] != None:
                pue["power"] = float(item["power"])
            if len(pue.keys()) > 0:
                pue["record_time"] = item['record_time'].timestamp()
                self.pue_list.append(pue)

            user = {}
            if "user" in item and item["user"] != None:
                user["user"] = int(item["user"])
            if "job" in item and item["job"] != None:
                user["job"] = int(item["job"])
            if "cpu_job" in item and item["cpu_job"] != None:
                user["cpu_job"] = int(item["cpu_job"])
            if "cpu_user" in item and item["cpu_user"] != None:
                user["cpu_user"] = int(item["cpu_user"])
            if "gpu_user" in item and item["gpu_user"] != None:
                user["gpu_user"] = int(item["gpu_user"])
            if "gpu_job" in item and item["gpu_job"] != None:
                user["gpu_job"] = int(item["gpu_job"])
            if "running_job" in item and item["running_job"] != None:
                user["running_job"] = int(item["running_job"])
            if "waiting_job" in item and item["waiting_job"] != None:
                user["waiting_job"] = int(item["waiting_job"])
            if "cpu_waiting_job" in item and item["cpu_waiting_job"] != None:
                user["cpu_waiting_job"] = int(item["cpu_waiting_job"])
            if "gpu_waiting_job" in item and item["gpu_waiting_job"] != None:
                user["gpu_waiting_job"] = int(item["gpu_waiting_job"])
            if "cpu_running_job" in item and item["cpu_running_job"] != None:
                user["cpu_running_job"] = int(item["cpu_running_job"])
            if "gpu_running_job" in item and item["gpu_running_job"] != None:
                user["gpu_running_job"] = int(item["gpu_running_job"])
            if len(user.keys()) > 0:
                user["record_time"] = item['record_time'].timestamp()
                self.user_list.append(user)

            node = {}
            if "node" in item and item["node"] != None:
                node["node"] = int(item["node"])
            if "core" in item and item["core"] != None:
                node["core"] = int(item["core"])
            if "cpu_node" in item and item["cpu_node"] != None:
                node["cpu_node"] = int(item["cpu_node"])
            if "cpu_core" in item and item["cpu_core"] != None:
                node["cpu_core"] = int(item["cpu_core"])
            if "gpu_node" in item and item["gpu_node"] != None:
                node["gpu_node"] = int(item["gpu_node"])
            if "gpu_core" in item and item["gpu_core"] != None:
                node["gpu_core"] = int(item["gpu_core"])
            if "gpu_gpu" in item and item["gpu_gpu"] != None:
                node["gpu_gpu"] = int(item["gpu_gpu"])
            if "all_gpu" in item and item["all_gpu"] != None:
                node["all_gpu"] = int(item["all_gpu"])
            if "all_node" in item and item["all_node"] != None:
                node["all_node"] = int(item["all_node"])
            if "all_core" in item and item["all_core"] != None:
                node["all_core"] = int(item["all_core"])

            if len(node.keys()) > 0:
                node["record_time"] = item['record_time'].timestamp()
                self.node_list.append(node)
