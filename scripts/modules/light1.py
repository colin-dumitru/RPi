import RPi.GPIO as GPIO
import threading
import time

# Commands
#    true
#    false
#    toggle:<times>
class Light1(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.daemon = True
		self.name = 'light1'
		self.state = False
		self.toggle_count = 0
		self.lock = threading.Lock()

	def init(self, app):
		self.app = app

		GPIO.setup(4, GPIO.OUT)
		self.start()

	def update_toggle(self):
		self.lock.acquire()

		if self.toggle_count > 0:
			self.state = not self.state
			self.output_light();

			self.toggle_count = self.toggle_count - 1

		self.lock.release()

	def run(self):
		while True:
			self.update_toggle()	

			time.sleep(1)

	def toggle(self, times):
		self.toggle_count = min(times, 30)
		self.app.send("notify:Light1 : Toggle(%d)" % times)

		if self.toggle_count == 1:
			self.update_toggle()

	def turn_on(self):
		self.app.send("notify2:7:on:12,0,0")
		self.state = True
		self.output_light();

	def turn_off(self):
		self.app.send("notify2:7:off:")
		self.state = False
		self.output_light();		

	def output_light(self):
		GPIO.output ( 4, self.state )

	def process(self, params):
		if params == 'true':
			self.turn_on()			
		
		if params == 'false':
			self.turn_off()

		if params.startswith('toggle'):
			self.toggle(int(params[7:]))
			
