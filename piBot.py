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
        self.triggers = {}
        self.setup_logging()

    def setup_logging(self):
        logging.config.dictConfig(self.config['logging'])
        self.logger = logging.getLogger('piBot')

    def import_modules(self, module_type):
        """ Imports needed modules based on config """
        for module in self.config[module_type]:
            m_config = self.config[module_type][module]
            m_config['id'] = module
            self.import_module(module_type, m_config)

    def import_module(self, module_type, m_config):
        """ Imports a single module of type module_type/m_type and saves the loaded class into the 'class' attribute of m_config """
        m_type = m_config['type']
        loaded_modules = self.__dict__[module_type]
        if not m_type in loaded_modules:
            self.logger.info('creating module %s %s', module_type, m_type)
            sys.path.append(module_type) #https://stackoverflow.com/questions/25997185/python-importerror-import-by-filename-is-not-supported
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
                    self.logger.error("Unexpected error", exc_info =1)

    def close_triggers(self):
        """ triggers cleanup """
        for t in self.triggers:
            t['close']()

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
                #pass data to trigger
                if 'trigger' in s_config:
                    trigger_config = s_config['trigger']
                    if trigger_config['active']:
                        if 'class' not in trigger_config:
                            self.import_module('triggers', trigger_config)
                        else:
                            trigger_config['class'].trigger(s_data)
                rows.extend(s_data)
            
            self.output_method('write', [rows])

            time.sleep(self.config['timeout'])


        """close active outputs"""
        self.output_method('close', ())
        self.close_triggers()

        self.logger.info('piBot end')


if __name__ == '__main__':
    piBot = piBot()    
    piBot.monitor()
