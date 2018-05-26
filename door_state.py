import RPi.GPIO as GPIO
import time

DOOR_CLOSED = False
PIN_NBR = 18

class DoorState(Thread):
	
	def __init__(self):
		Thread.__init__(self)
		self.name = "door_state_thread"
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_NBR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
	def run():
		while True:
			input_state = GPIO.input(PIN_NBR)
			if input_state == False:
				DOOR_CLOSED = True
				print('Button Pressed')
				time.sleep(0.2)
