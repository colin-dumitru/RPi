import RPi.GPIO as GPIO
import threading
import time

# Commands
#    set_temp:<temperature>
#    get_temp
class Thermostat(threading.Thread):
    PIN_OUT = 17
    TEMP_THRESHOLD = 0.5
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.daemon = True
        self.name = 'thermostat'
        self.state = False
        self.ideal_temp = 21
        self.lock = threading.Lock()
    
    def init(self, app):
        self.app = app
        
        GPIO.setup(Thermostat.PIN_OUT, GPIO.OUT)
        self.start()
    
    def update_temp(self):
        self.lock.acquire()
        
        temp = self.app.send("temp:read")
        
        if temp - Thermostat.TEMP_THRESHOLD > self.ideal_temp:
            self.turn_off()
            
        if temp + Thermostat.TEMP_THRESHOLD < self.ideal_temp:
            self.turn_on()
        
        self.lock.release()
    
    def run(self):
        while True:
            self.update_temp()
            
            time.sleep(5)
    
    def turn_off(self):
        self.state = False
        self.output_light()
        self.app.send('notify2:0:on:0,12,0')
    
    def turn_on(self):
        self.state = True
        self.output_light()
        self.app.send('notify2:0:on:12,0,0')
    
    def output_light(self):
        GPIO.output ( Thermostat.PIN_OUT, self.state )
    
    def set_ideal_temp(self, params):
        action, temp = params.split(':')
        
        self.lock.acquire()
        self.ideal_temp = float(temp)
        self.lock.release()
    
    def process(self, params):
        if params == 'get_state':
            return self.state
            
        if params == 'get_temp':
            return self.ideal_temp
        
        if params.startswith('set_temp'):
            self.set_ideal_temp(params)
        
        if params.startswith('toggle'):
            self.toggle(int(params[7:]))
