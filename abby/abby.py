from speech import *
from wolfram import *

import time

rec = SpeechRec(debug = True)
speaker = Speaker()
wolfram = Wolfram()
lcd = LCD()

last_lcd_update = time.time()

def initialize():
	lcd.init()

	rec.start()

def do_loop():
	rec.listen(rec_callback, progress = rec_progress)

def rec_callback(text):
	if not text: return

	print("[Message] %s" % text)
	lcd.multiline(text)

	response = wolfram.get_response(text)
	speaker.speak(response)

	return False	

def rec_progress(rec, chunk):
	global last_lcd_update

	now = time.time()

	if not last_lcd_update or (now - last_lcd_update) > 0.5:
		lcd.line2("%s %d/%d" % (('R' if rec.recording else ' '), rec._intensity(chunk), rec._silence_threshold))

		last_lcd_update = now

if __name__ == '__main__':
	initialize()
	do_loop()