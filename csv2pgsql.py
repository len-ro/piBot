#!/usr/bin/env python3

import psycopg2
import csv


class csv2pgsql:
    def __init__(self):
        self.dbconn = 'dbname=piBot user=piBot password=simple host=10.8.0.1 port=5432'
        self.conn = None
        self.cur = None

    def open(self):
        self.conn = psycopg2.connect(self.dbconn)
        self.cur = self.conn.cursor()

    def insert(self, row):
        self.cur.execute("""insert into sensor_data(capture_time, id, name, value) values (%s, %s, %s, %s)""", row)
        self.conn.commit()
    
    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == '__main__':
    db = csv2pgsql()
    db.open()
    with open('data.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile, dialect='excel')
        for row in csvreader:
            value = row[-1]
            if not value == 'NO-DATA':  
                db.insert(row)
    db.close()