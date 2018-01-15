from time import sleep
import sys
import RPi.GPIO as GPIO
import logging
class pump:
    """
    starts relay based on start and stop temp by enabling GPIO pin
    see https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
    """

    def __init__(self, config):
        self.logger = logging.getLogger('triggers.pump')
        self.config = config
        self.pin = self.config['pin']
        self.start_temp = self.config['startTemp']
        self.stop_temp = self.config['stopTemp']
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        self.set_pin(False) #default to 0ff

    def trigger(self, data):
        """ data = [['2018-01-15 17:36:48', '28-0115926cbfff', 'one', 'NO-DATA']] """
        for d in data:
            if d[3] != 'NO-DATA':
                temp = d[3]
                if temp >= self.start_temp:
                    if not self.get_pin():
                        self.logger.info("Temp %s is above %s, starting pump", temp, self.start_temp)
                        self.set_pin(True)
                if temp <= self.stop_temp:
                    if self.get_pin():
                        self.logger.info("Temp %s is bellow %s, stoping pump", temp, self.start_temp)
                        self.set_pin(False)

    def get_pin(self):
        return GPIO.input(self.pin)

    def set_pin(self, value):
        """ sets pin value, True = closes relay NO - on, NC - off, False = open relay NO - off, NC - on """
        GPIO.output(self.pin, value) 
        sleep(1) #why?

    def close(self):
        GPIO.cleanup(self.pin)