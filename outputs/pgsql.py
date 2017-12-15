import psycopg2
import logging


class pgsql:
    def __init__(self, config):
        self.dbconn = 'dbname=%(dbname)s user=%(user)s password=%(password)s host=%(host)s port=%(port)s' % config
        self.conn = None
        self.cur = None
        self.logger = logging.getLogger('piBot.pgsql')
        self.connected = False
        self.send_buffer = []

    def open(self):
        try:
            self.conn = psycopg2.connect(self.dbconn)
            self.cur = self.conn.cursor()
            self.connected = True
        except:
            self.logger.error("Cannot open connection", exc_info = 1)

    def write_rows(self, rows):
        for row in rows:
            if not row[-1] == 'NO-DATA':
                #do not insert NO-DATA, only valid values
                #do nothing on conflict to allow inserting of old data, see https://stackoverflow.com/questions/4069718/postgres-insert-if-does-not-exist-already
                self.cur.execute("""insert into sensor_data(capture_time, id, name, value) values (%s, %s, %s, %s) on conflict do nothing""", row)

    def write(self, rows):
        try:
            if not self.connected:
                self.open()
                if self.send_buffer:
                    self.write_rows(self.send_buffer)
                    self.logger.info("Succesfuly wrote send buffer %s", len(self.send_buffer))
                    self.send_buffer = []
            self.write_rows(rows)
            self.conn.commit()
        except:
            self.logger.error("Write error, will retry later", exc_info = 1)
            self.send_buffer.extend(rows)
            self.close()
    
    def close(self):
        try:
            self.connected = False
            self.cur.close()
            self.conn.close()
        except:
            self.logger.error("Cannot close connection", exc_info = 1)

