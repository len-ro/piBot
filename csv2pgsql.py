#!/usr/bin/env python3

import csv
import sys
from outputs.pgsql import pgsql

"""one time import of csv data into pgsql"""

if __name__ == '__main__':
    db = pgsql({"dbname": "piBot", "user": "piBot", "password": "simple", "host": "10.8.0.1", "port": "5432",})
    db.open()
    with open(sys.argv[1], 'r') as csvfile:
        csvreader = csv.reader(csvfile, dialect='excel')
        for row in csvreader:  
            print('.', end='', flush=True)
            db.write([row])
    db.close()
