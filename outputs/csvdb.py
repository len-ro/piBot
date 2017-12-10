from csv import writer
import os
import datetime
import logging

class csvdb:
    def __init__(self, config):
        self.config = config
        self.csv_file = None
        self.csv_writer = None
        self.day = None
        self.logger = logging.getLogger('piBot.csvdb')

    def open(self):
        now = datetime.datetime.now()
        self.day = now.day
        file_name = now.strftime(self.config['file']) 
        self.logger.info("writing to %s", file_name)
        self.csv_file = open(file_name, 'abt')
        self.csv_writer = writer(self.csv_file, dialect = self.config['dialect'])

    def write(self, rows):
        now = datetime.datetime.now()
        if self.day != now.day: #create a new file
            self.close()
            self.open()
        self.csv_writer.writerows(rows)
        self.csv_file.flush()
        os.fsync(self.csv_file.fileno())
    
    def close(self):
        self.csv_file.close()
