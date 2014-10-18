import RPi.GPIO as GPIO
import threading
import time

# Commands
#    true
#    false
#    toggle:<times>
class Light1(threading.Thread):
    PIN_OUT = 4
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.daemon = True
        self.name = 'light1'
        self.state = False
        self.toggle_count = 0
        self.lock = threading.Lock()
    
    def init(self, app):
        self.app = app
        
        GPIO.setup(Light1.PIN_OUT, GPIO.OUT)
        self.start()
    
    def update_toggle(self):
        self.lock.acquire()
        
        if self.toggle_count > 0:
            self.state = not self.state
            self.output_light()
            
            self.toggle_count = self.toggle_count - 1
        
        self.lock.release()
    
    def run(self):
        while True:
            self.update_toggle()
            
            time.sleep(1)
    
    def toggle(self, times):
        self.toggle_count = min(times, 30)
        
        if self.toggle_count == 1:
            self.update_toggle()
    
    def send_notification(self):
        if self.state:
            self.app.send('notify2:7:on:12,0,0')
        else:
            self.app.send('notify2:7:off:12,0,0')
    
    def turn_on(self):
        self.state = True
        self.output_light()
    
    def turn_off(self):
        self.state = False
        self.output_light()
    
    def output_light(self):
        GPIO.output ( Light1.PIN_OUT, self.state )
    
    def process(self, params):
        if params == 'true':
            self.turn_on()
        
        if params == 'false':
            self.turn_off()
        
        if params.startswith('toggle'):
            self.toggle(int(params[7:]))
        
        self.send_notification()
