import RPi.GPIO as GPIO
import threading

from subprocess import Popen, PIPE

class IR(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self.name = 'ir'
		self.light = False

	def init(self, app):
		self.app = app

		self.start()

	def toggle_light(self):
		if self.light:
			self.app.send( 'light1:true')
		else:
			self.app.send( 'light1:false')

		self.light = not self.light

	def run_command(self, key):
		if key == 'KEY_A':
			self.toggle_light()

	def process_key(self, key):
		self.run_command(key)

	def run(self):
		p = Popen(["irw"],stdin=PIPE,stdout=PIPE)

		while True:
			line = p.stdout.readline().split(' ')

			if line[1] == '00':
				self.process_key(line[2])

	def process(self, params):
		pass
