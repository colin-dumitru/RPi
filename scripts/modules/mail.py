import imaplib
import threading
import time
import email 

class Email(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

		self.daemon = True
		self.name = 'email'

		self.login_info = self.get_login_info()

	def get_login_info(self):
		with open('/opt/email_pass') as file:
			return file.readlines()

	def init(self, app):
		self.app = app
		self.start()

	def check_email(self, content):
		mail = email.message_from_string(content)

		print 'From: ' + mail['From']

		if 'abby-pi@outlook.com' in mail['From']:
			self.app.send('light1:toggle:30')
			self.app.send('notify:SEV2')

	def get_header(self, header, lines):
		for i in range(0, len(lines)):
			if lines[i].startswith(header):
				return lines[i][(len(header)):]


	def connect(self):
		imap = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)

		imap.login(self.login_info[0].strip(), self.login_info[1].strip())
		imap.select()

		return imap

	def close(self, imap):
		imap.close()
		imap.logout()


	def run(self):
		while True:
			print 'Checking email...'

			imap = self.connect()

			for index in imap.search(None, '(UNSEEN)')[1][0].split():
				if index is not None:
					status, data = typ, data = imap.fetch(index, '(RFC822)')
					self.check_email(data[0][1])

			self.close(imap)

			time.sleep(60 * 5)

	def process(self, params):
		pass
			
