import threading
import time

from neopixel import *

# LED strip configuration:
LED_COUNT   = 8      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

class Notify2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.name = 'notify2'

    def init(self, app):
        self.app = app

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        
        for i in range(0, LED_COUNT):
            self.strip.setPixelColor(i, 0)
            
        self.strip.show()

    def run(self):
        while True:
            # TODO implement toggle
            time.sleep(10)
                
    def turn_led_off(self, index):
        self.strip.setPixelColor(int(index), 0)
        self.strip.show()
        
    def set_led_color(self, index, color_str):
        red, green, blue = color_str.split(',')
        
        self.strip.setPixelColor(int(index), Color(int(red), int(green), int(blue)))
        self.strip.show()

    def process(self, params):
        led, action, extra = params.split(':')
        
        if action == 'on':
            self.set_led_color(led, extra)
        else:
            self.turn_led_off(led)
            
        return action
		
