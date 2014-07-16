import lcd
import RPi.GPIO as GPIO
import threading
import time
import datetime
import commands

class Notify(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True

		self.name = 'notify'
		self.skip_update = 0

	def init(self, app):
		self.app = app

		self.lcd = lcd.LCD()
		self.lcd.init()

		self.start()


	def get_cpu_temp(self):
	    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
	    cpu_temp = tempFile.read()
	    tempFile.close()
	    return float(cpu_temp)/1000
	 
	def get_gpu_temp(self):
		gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
		return  float(gpu_temp)

	def show_status_message(self):
		now = datetime.datetime.now()
   
		self.lcd.line1("CPU: %d  GPU: %d" % (self.get_cpu_temp(), self.get_gpu_temp()))
		self.lcd.line2(now.strftime("%d/%m %H:%M:%S"))

	def run(self):
		while True:
			if self.skip_update > 0:
				self.skip_update = self.skip_update - 1
			else:
				self.show_status_message();

			time.sleep(1)


	def process(self, params):
		self.skip_update = 5
		self.lcd.message( params )
