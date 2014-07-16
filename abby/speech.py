import pyaudio
import audioop
import sys
import math
import time
import wave
import os
import httplib2
import json

from lcd import LCD

# TODO
#	 pre-pend previous audio to prevent chopyness

class SpeechRec:
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	FRAMES_PER_BUFFER = 4096
	# How many seconds of silence does it take to en a message
	PHRASE_SILENCE_THRESHOLD = 1
	# NUmber of seconds to record noise for calibration
	CALIBRATION_LENGTH = 2

	RECORDING_FILE = '/tmp/recording'

	RECOGNIZE_URL = 'https://www.google.com/speech-api/v2/recognize?client=chromium&lang=en-US&key=AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw&output=json'


	def __init__(self, debug = False):
		self._debug = debug

	def start(self):
		self.recording = False
		self._audio = pyaudio.PyAudio()

		self._stream = self._audio.open(
			format = SpeechRec.FORMAT,
			channels = SpeechRec.CHANNELS,
			rate = SpeechRec.RATE,
			frames_per_buffer = SpeechRec.FRAMES_PER_BUFFER, 
			input = True
		)

		self._calibrate()

		print ('Audio initialized')

	def listen(self, callback, progress = None):
		self._progress = progress

		finished = False

		while not finished:
			init_buffer = self._wait_for_speech()
			self._record(init_buffer)
			self._convert_to_flac()
			message = self._send_request()

			finished = callback(message)

	def _calibrate(self):
		print ('Recoding %d seconds of noise to calibrate' % SpeechRec.CALIBRATION_LENGTH)

		buffer = []

		for i in range(0, int(SpeechRec.RATE / SpeechRec.FRAMES_PER_BUFFER * SpeechRec.CALIBRATION_LENGTH)):
			chunk = self._stream.read(SpeechRec.FRAMES_PER_BUFFER)

			# Skip the first few frames as that is skewing the avg
			if i > 10:
				buffer.append(chunk)

		avg = sum([self._intensity(chunk) for chunk in buffer]) / len(buffer) / 2

		print ('Setting threshold intensity at: %d' % avg)

		# used to activelly monitor the silence level so it can be adjusted real time
		self._silence_threshold = avg


	def _wait_for_speech(self):
		print ('Waiting for speech')

		buffer = []
		is_silence = True
		self.recording = False

		while is_silence:
			chunk = self._read_chunk()

			if not chunk: continue

			self._chunk_update(chunk)

			buffer.append(chunk)
			# only keep 10 cunks
			if len(buffer) > 10: buffer.pop(0)

			is_silence = self._is_silence(chunk, update_continous = True)			

		return buffer

	def _record(self, buffer):
		print ('Recording')

		seconds_of_silence = 0
		self.recording = True

		while seconds_of_silence < SpeechRec.PHRASE_SILENCE_THRESHOLD:
			chunk = self._read_chunk()

			if not chunk: continue

			self._chunk_update(chunk)
			buffer.append(chunk)

			if self._is_silence(chunk, update_continous = False):
				seconds_of_silence = seconds_of_silence + SpeechRec.FRAMES_PER_BUFFER / SpeechRec.RATE
			else:
				seconds_of_silence = 0

		self._save(buffer, SpeechRec.RECORDING_FILE + '.wav')

	def _read_chunk(self):
		try:
			return self._stream.read(SpeechRec.FRAMES_PER_BUFFER)
		except IOError:
			print ('Skipping chunk...')
			return None


	def _save(self, buffer, filename):
		file = wave.open(filename, 'wb')

		file.setnchannels(SpeechRec.CHANNELS)
		file.setsampwidth(self._audio.get_sample_size(SpeechRec.FORMAT))
		file.setframerate(SpeechRec.RATE)
		file.writeframes(b''.join(buffer))

		file.close()

	def _is_silence(self, chunk, update_continous = False):
		avg = self._intensity(chunk)
		is_silence = avg < (self._silence_threshold * 2)

		if update_continous:
			self._silence_threshold = (self._silence_threshold * 99 + avg) / 100
	
		return is_silence


	def _intensity(self, chunk):
		return int(math.sqrt(abs(audioop.avg(chunk, 4))))

	def _chunk_update(self, chunk):
		if self._progress:
			self._progress(self, chunk)

	def _convert_to_flac(self):
		os.system("avconv -i "+ SpeechRec.RECORDING_FILE + ".wav  -y -ar 44100 " + SpeechRec.RECORDING_FILE + ".flac")

	def _send_request(self):
		print ( "Sending request..." )

		with open(SpeechRec.RECORDING_FILE + '.flac', 'rb') as file:
			flac = file.read()

			headers = {
				"User-Agent": "Mozilla/5.0", 
           		'Content-type': 'audio/x-flac; rate=%d' % SpeechRec.RATE
       		}  

			request = httplib2.Http()
			response, content = request.request(
				SpeechRec.RECOGNIZE_URL, 
				"POST",
			    body = flac, 
			    headers = headers
		    )

			content_str = content.decode("utf-8")

			print (content_str)

			for line in content_str.strip().split('\n'):
				decoded = self._extract_message(json.loads(line))

				if decoded: return decoded

			return None

	def _extract_message(self, json):
		results = json['result']

		if len(results) == 0: return None

		return results[0]['alternative'][0]['transcript']
		

class Test:
	def __init__(self):
		self._last_update = None

	def callback(self, text):
		print("[Message] %s" % text)

		return False	

	def progress(self, rec, chunk):
		now = time.time()

		if not self._last_update or (now - self._last_update) > 0.5:
			self._lcd.line2("%s %d/%d" % (('R' if rec.recording else ' '), rec._intensity(chunk), rec._silence_threshold))

			self._last_update = now

	def do_test(self):
		self._lcd = LCD()
		self._lcd.init()

		rec = SpeechRec(debug = True)
		rec.start()
		rec.listen(self.callback, progress = self.progress)

class Speaker:
	def __init__(self):
		pass

	def speak(self, message):
		os.system('/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=%s"' % message)


def main():
	test = Test()
	test.do_test()


if __name__ == '__main__':
	main()