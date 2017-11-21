import psycopg2


class pgsql:
    def __init__(self, config):
        self.dbconn = 'dbname=%(dbname)s user=%(user)s password=%(password)s host=%(host)s port=%(port)s' % config
        self.conn = None
        self.cur = None

    def open(self):
        self.conn = psycopg2.connect(self.dbconn)
        self.cur = self.conn.cursor()

    def write(self, rows):
        for row in rows:
            if not row[-1] == 'NO-DATA':
                #do not insert NO-DATA, only valid values
                self.cur.execute("""insert into sensor_data(capture_time, id, name, value) values (%s, %s, %s, %s)""", row)
        self.conn.commit()
    
    def close(self):
        self.cur.close()
        self.conn.close()

