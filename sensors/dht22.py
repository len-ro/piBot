import time
import Adafruit_DHT

class dht22:
    """reads dht22 sensor data (temperature & humidity)"""

    def __init__(self, config):
        self.config = config
        self.pin = self.config['pin']
        self.sensor_type = 22 #DHT22 sensor

    def read(self, data):
        """reads the sensor data """
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)

        """ from Adafruit_DHT example:
        Note that sometimes you won't get a reading and the results will be null 
        (because Linux can't guarantee the timing of calls to read the sensor). If this happens try again! """
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
            return [[data['ts'], self.config['id'] + '-t', self.config['name'], temperature], [data['ts'], self.config['id'] + '-h', self.config['name'], humidity]]    
        else:
            return [[data['ts'], self.config['id'], self.config['name'], 'NO-DATA']]
