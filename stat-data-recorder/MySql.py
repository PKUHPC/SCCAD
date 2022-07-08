import pymysql,atexit

class Mysql:

    def __init__(self,db_config):
        self.charset = 'utf8'
        self.connect = pymysql.connect(
            host    = db_config['host'],
            port    = db_config['port'],
            user    = db_config['user'],
            passwd  = db_config['passwd'],
            db      = db_config['db'],
            charset = self.charset
        )
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
