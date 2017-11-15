import time
class ds18b20:

    def __init__(self, config):
        self.config = config
        self.s_path = '/sys/bus/w1/devices/%s/w1_slave' % (self.config['path'])

    def read(self, data):
        return [data['ts'], self.config['id'], self.config['name'], self.read_temp()]

    def read_raw(self):
        """reads the raw content of sensor "file" """
        s_file = open(self.s_path, 'r')
        lines = s_file.readlines()
        s_file.close()
        return lines

    def read_temp(self):
        """converts raw content of sensor "file" to temp data as float """
        try:
            lines = self.read_raw()

            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = self.read_raw()

            temp_output = lines[1].find('t=')
            if temp_output != -1:
                temp_string = lines[1].strip()[temp_output + 2:]
                temp_c = float(temp_string) / 1000.0
                return temp_c
        except IOError:
            return 'NO-DATA'
