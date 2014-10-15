import threading
import time
import smbus

ADDR = 0x48

class Temp():
    def __init__(self):
        self.name = 'temp'

    def init(self, app):
        self.app = app
        self.bus = smbus.SMBus(1)


    def get_temp(self):
        word = self.bus.read_word_data(ADDR , 0 )
        lsb = (word & 0xff00) >> 8 
        msb = (word & 0x00ff)
        
        return ((( msb * 256 ) + lsb) >> 4 ) * 0.0625

    def process(self, params):
        action = params
        
        if action == 'read':
            return self.get_temp()
        
