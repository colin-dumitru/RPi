import RPi.GPIO as GPIO

class Light1:
	def __init__(self):
		self.name = 'light1'

	def init(self, app):
		self.app = app

		GPIO.setup(4, GPIO.OUT)

	def process(self, params):
		if params == 'true':
			self.app.send("notify:Light1 : On")
			GPIO.output ( 4, True )
		
		if params == 'false':
			self.app.send("notify:Light1 : Off")
			GPIO.output ( 4, False )
