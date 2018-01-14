import time

class thermal:
    """reads cpu temperature in /sys/class/thermal/*/temp"""

    def __init__(self, config):
        self.config = config
        self.s_path = '/sys/class/thermal/%s/temp' % config['path']

    def read(self, data):
        return ][data['ts'], self.config['id'], self.config['name'], self.read_temp()]]

    def read_temp(self):
        """converts raw content of sensor "file" to temp data as float """
        try:
            s_file = open(self.s_path, 'r')
            temp_string = s_file.readline().strip()
            s_file.close()
            temp_c = float(temp_string) / 1000.0
            return temp_c
        except IOError:
            return 'NO-DATA'
