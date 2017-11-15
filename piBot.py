#!/usr/bin/env python
import json
import csv
import signal
import os
import time
import datetime

config = {}
modules = {}

class signal_catcher:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True

def import_modules():
    """ Imports needed modules based on config """
    for sensor in config['sensors']:
        s_config = config['sensors'][sensor]
        s_config['id'] = sensor
        s_type = s_config['type']
        print('Configuring', sensor, s_type)
        if not modules.has_key(s_type):
            module = __import__(s_type)
            m_class = getattr(module, s_type)
            modules[s_type] = m_class
            s_config['class'] = m_class(s_config)
        else:
            s_config['class'] = modules[s_type](s_config)


def monitor():
    import_modules()
    killer = signal_catcher()

    with open(config['csv-db'], 'ab') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        while True:
            if killer.kill_now:
                break
            now = datetime.datetime.utcnow()
            now_s = now.strftime("%Y-%m-%d %H:%M:%S")
            rows = []
            s_param = {'ts': now_s}

            for sensor in config['sensors']:
                s_config = config['sensors'][sensor]
                s_data = s_config['class'].read(s_param)
                print(s_data)
                rows.append(s_data)

            csvwriter.writerows(rows)
            csvfile.flush()
            os.fsync(csvfile.fileno())
            time.sleep(config['timeout'])
        csvfile.close()
        print('piBot end')


if __name__ == '__main__':
    print('piBot started')
    config = json.load(open('config.json', 'r'))
    monitor()
