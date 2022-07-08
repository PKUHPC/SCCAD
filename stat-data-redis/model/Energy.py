import datetime

class Energy:

    def __init__(self, pue_str):
        self.pue = None
        self.power = None
        self.update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if pue_str:
            info = pue_str.strip().split("\n")
            if len(info) >= 3:
                city_in = int(info[0])
                big_ups_out = int(info[1])
                small_ups_in = int(info[2])
                self.pue = round((city_in+big_ups_out)/(big_ups_out+small_ups_in),2)
                self.power = round((city_in+big_ups_out)/100,2)

    def get_cluster_pue(self):
        if self.pue:
            return self.__dict__
        else:
            return None
