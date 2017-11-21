from csv import writer
import os

class csvdb:
    def __init__(self, config):
        self.config = config
        self.csv_file = None
        self.csv_writer = None

    def open(self):
        self.csv_file = open(self.config['file'], 'ab')
        self.csv_writer = writer(self.csv_file, dialect = self.config['dialect'])

    def write(self, rows):
        self.csv_writer.writerows(rows)
        self.csv_file.flush()
        os.fsync(self.csv_file.fileno())
    
    def close(self):
        self.csv_file.close()
