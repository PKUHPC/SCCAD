import datetime,atexit,pymysql

def get_readable_seconds_time(time_seconds):
    if time_seconds < 60:
        return "{:.0f} seconds".format(time_seconds)
    elif time_seconds < 3600:
        return "{:.2f} minutes".format(time_seconds/60)
    else:
        return "{:.2f} hours".format(time_seconds/3600)

class MySql:
    def __init__(self,db_config):
        self.charset = 'utf8'
        self.connect = pymysql.connect(
            host    = db_config['host'],
            port    = db_config['port'],
            user    = db_config['user'],
            passwd  = db_config['passwd'],
            db      = db_config['database'],
            charset = self.charset
        )
        self.db_config = db_config
        self.cursor = self.connect.cursor(cursor=pymysql.cursors.DictCursor)
        atexit.register(self.close)

    def close(self):
        self.cursor.close()
        self.connect.close()

    def execute(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def commit(self):
        self.connect.commit()
