#!/usr/bin/env python3
import json
import csv
import signal
import os
import time
import datetime
import logging, logging.config
import sys

config = {}
sensors = {}
outputs = {}

class signal_catcher:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

class piBot:

    def __init__(self):
        self.config = json.load(open('config.json', 'r'))
        self.sensors = {}
        self.outputs = {}
        self.setup_logging()

    def setup_logging(self):
        logging.config.dictConfig(self.config['logging'])
        self.logger = logging.getLogger('piBot')

    def import_modules(self, type):
        """ Imports needed modules based on config """
        sys.path.append(type) #https://stackoverflow.com/questions/25997185/python-importerror-import-by-filename-is-not-supported
        for module in self.config[type]:
            m_config = self.config[type][module]
            m_config['id'] = module
            m_type = m_config['type']
            self.logger.info('Configuring module %s %s %s' % (type, module, m_type))
            loaded_modules = self.__dict__[type]
            if not loaded_modules.has_key(m_type):
                module = __import__(m_type)
                m_class = getattr(module, m_type)
                loaded_modules[m_type] = m_class
                m_config['class'] = m_class(m_config)
            else:
                m_config['class'] = loaded_modules[m_type](m_config)

    def output_method(self, method, args):
        for output in self.config['outputs']:
            output_config = self.config['outputs'][output]
            if output_config['active'] == 'true':
                try:
                    getattr(output_config['class'], method)(*args)
                except:
                    self.logger.error("Unexpected error:", sys.exc_info()[0])

    def monitor(self):
        self.logger.info('piBot start')
        self.import_modules('sensors')
        self.import_modules('outputs')
        killer = signal_catcher()

        """open active outputs"""
        self.output_method('open', ())

        """main loop"""
        while True:
            if killer.kill_now:
                break

            now = datetime.datetime.now()
            now_s = now.strftime("%Y-%m-%d %H:%M:%S")
            rows = []
            s_param = {'ts': now_s}

            for sensor in self.config['sensors']:
                s_config = self.config['sensors'][sensor]
                s_data = s_config['class'].read(s_param)
                self.logger.info(s_data)
                rows.append(s_data)
            
            self.output_method('write', [rows])

            time.sleep(self.config['timeout'])


        """close active outputs"""
        self.output_method('close', ())

        self.logger.info('piBot end')


if __name__ == '__main__':
    piBot = piBot()    
    piBot.monitor()
