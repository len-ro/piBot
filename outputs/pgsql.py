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
                #do nothing on conflict to allow inserting of old data, see https://stackoverflow.com/questions/4069718/postgres-insert-if-does-not-exist-already
                self.cur.execute("""insert into sensor_data(capture_time, id, name, value) values (%s, %s, %s, %s) on conflict do nothing""", row)
        self.conn.commit()
    
    def close(self):
        self.cur.close()
        self.conn.close()

