import RPi.GPIO as GPIO
import threading

from subprocess import Popen, PIPE

class IR(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.daemon = True
		self.name = 'ir'

	def init(self, app):
		self.app = app

		self.start()

	def toggle_light(self, times):
		self.app.send( 'light1:toggle:%d' % times)

	def run_command(self, key):
		if key == 'KEY_A':
			self.toggle_light(1)

		if key == 'KEY_B':
			self.toggle_light(4)

		if key == 'KEY_POWER':
			self.toggle_light(0)

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
