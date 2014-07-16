#!/usr/bin/python
from subprocess import check_output
from email.mime.text import MIMEText

import smtplib

def get_ip():
	return check_output(['curl','icanhazip.com'])

def get_if():
	return check_output(['ifconfig'])

def send_email(message):
	msg = MIMEText(message)

	msg['Subject'] = 'Master, my ip address has changes'
	msg['From'] = 'RPI@home.ro'
	msg['To'] = 'colin.dumitru@gmail.com'

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()
	s.login('rpi.mozi', 'mozi.rpi')
	s.sendmail('RPI@home.ro', ['colin.dumitru@gmail.com'], msg.as_string())
	s.quit()

def has_ip_changed(ip):
	content = ''

	try:
		file = open('/tmp/rpi.ip')
		content = file.read()
		file.close()		
	except IOError:
   		pass

	return not (content == ip)

def save_ip(ip):
	file = open('/tmp/rpi.ip', 'w')
	file.write(ip)
	file.close()


def main():
	ip = get_ip()
	ifc = get_if()

	message = 'Hi, my ip address has changes\n ip: %s \n\n %s' % (ip, ifc)
	if has_ip_changed(ip):
		send_email(message)	
		save_ip(ip)

if __name__== '__main__':
	main()