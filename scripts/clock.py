#!/usr/bin/python
import commands
import datetime
import time

from lcd import *

class Config:
    LED_OUT = 4
 
def get_cpu_temp():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    return float(cpu_temp)/1000
 
def get_gpu_temp():
    gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
    return  float(gpu_temp)

def main():
    
    
    lcd = LCD()
    lcd.init()

    while True:
        now = datetime.datetime.now()
   
        #afisare de text pe LCD
        lcd.line1("CPU: %d  GPU: %d" % (get_cpu_temp(), get_gpu_temp()))
        lcd.line2(now.strftime("%d/%m %H:%M:%S"))

        time.sleep(1) 
 
if __name__ == '__main__':
    main()
