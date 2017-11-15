#!/usr/bin/env python

import time, csv, datetime, os, signal

ds18b20s=['28-0315937bc3ff']#'28-000005e0a865', '28-0115926cbfff']
read_interval=10 #in seconds

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self,signum, frame):
        self.kill_now = True

def read_raw(sensor):
    f = open(sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor):
    lines = read_raw(sensor)

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_raw(sensor)

    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def monitor():
    killer = GracefulKiller()
    with open('monitor.csv', 'ab') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        while True:
            if killer.kill_now:
                break
            now = datetime.datetime.utcnow()
            now_s = now.strftime("%Y-%m-%d %H:%M:%S")
            row = [now_s]
            for s in ds18b20s:
                sensor = '/sys/bus/w1/devices/%s/w1_slave' % (s)
                data = read_temp(sensor)
                row.append(s)
                row.append(data)

            csvwriter.writerow(row)
            csvfile.flush()
            os.fsync(csvfile.fileno())
            print row
            time.sleep(read_interval)
        csvfile.close()
        print "End."
            
if __name__=='__main__':
    monitor()
