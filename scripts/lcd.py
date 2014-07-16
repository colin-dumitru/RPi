import RPi.GPIO as GPIO
import time

class LCD:
	LCD_RS = 25
	LCD_E  = 24
	LCD_D4 = 23 
	LCD_D5 = 17
	LCD_D6 = 18
	LCD_D7 = 22


	LCD_WIDTH = 16 
	LCD_CHR = True
	LCD_CMD = False

	LCD_LINE_1 = 0x80
	LCD_LINE_2 = 0xC0 

	E_PULSE = 0.00005
	E_DELAY = 0.00005


	def init(self):
		GPIO.setmode(GPIO.BCM)       
		GPIO.setup(LCD.LCD_E, GPIO.OUT)  
		GPIO.setup(LCD.LCD_RS, GPIO.OUT) 
		GPIO.setup(LCD.LCD_D4, GPIO.OUT) 
		GPIO.setup(LCD.LCD_D5, GPIO.OUT) 
		GPIO.setup(LCD.LCD_D6, GPIO.OUT) 
		GPIO.setup(LCD.LCD_D7, GPIO.OUT)

		# initialisation
		self._write_byte(0x33, LCD.LCD_CMD)
		# initialisation
		self._write_byte(0x32, LCD.LCD_CMD)
		# 2 line matrix
		self._write_byte(0x28, LCD.LCD_CMD)
		# turn cursor off, 0x0E to enable
		self._write_byte(0x0C, LCD.LCD_CMD) 
		# shift cursor right 
		self._write_byte(0x06, LCD.LCD_CMD)

		self.clear()

	def clear(self):
		# clear
		self._write_byte(0x01, LCD.LCD_CMD)  
		time.sleep(LCD.E_DELAY)

	def write_empty(self):
		self.line1('                ')
		self.line1('                ')

	def line1(self, message):
		self._write_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
		self.write(message.ljust(16))

	def line2(self, message):
		self._write_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
		self.write(message.ljust(16))

	def message(self, message):
		parts = message.split('\n')

		self.line1(parts[0])
		if (len(parts) > 1): self.line2(parts[1])

	def multiline(self, message):
		self.line1(message[0:16].ljust(16))
		self.line2(message[16:].ljust(16))

	def write(self, message):
		for i in range(len(message)):
			self._write_byte(ord(message[i]),LCD.LCD_CHR)

	def set_cursor(self, row, col):
		row_offsets = [ 0x00, 0x40 ]

		self._write_byte(0x80 | (col + row_offsets[row]), LCD.LCD_CMD)

	def _write_byte(self, bits, mode):
		GPIO.output(LCD.LCD_RS, mode) 

		GPIO.output(LCD.LCD_D4, bits & 0x10 == 0x10)
		GPIO.output(LCD.LCD_D5, bits & 0x20 == 0x20)
		GPIO.output(LCD.LCD_D6, bits & 0x40 == 0x40)
		GPIO.output(LCD.LCD_D7, bits & 0x80 == 0x80)

		time.sleep(LCD.E_DELAY) 
		GPIO.output(LCD.LCD_E, True)  
		time.sleep(LCD.E_DELAY)
		GPIO.output(LCD.LCD_E, False)  
		time.sleep(LCD.E_DELAY)    

		GPIO.output(LCD.LCD_D4, bits & 0x01 == 0x01)
		GPIO.output(LCD.LCD_D5, bits & 0x02 == 0x02)
		GPIO.output(LCD.LCD_D6, bits & 0x04 == 0x04)
		GPIO.output(LCD.LCD_D7, bits & 0x08 == 0x08)

		time.sleep(LCD.E_DELAY) 
		GPIO.output(LCD.LCD_E, True)  
		time.sleep(LCD.E_DELAY) 
		GPIO.output(LCD.LCD_E, False)  
		time.sleep(LCD.E_DELAY) 

def main():
	lcd = LCD()

	lcd.lcd_init()

	#afisare de text pe LCD
	lcd.line1("Ce faci?")
	lcd.line2("Bine")

	lcd.set_cursor(0, 5)
	lcd.write("is")


if __name__ == '__main__':
	main()