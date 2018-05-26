import os
import time
from threading import Thread
from queue import Queue
import qrtools

def take_photo():
	camera.capture('pic.jpg')

class Camera(Thread):

	def __init__(self, q_read):
		Thread.__init__(self)
		self.name = "camera_thread"
		self.q_write = q_write

	def run(self):
		while True:
			sleep(1)
			take_photo()
			# Process your photo, do everything you want here
			qr = qrtools.QR()
			qr.decode('pic.jpg')
			if qr.data is None:
				cooking_time = 0
			else:
				cooking_time = int(qr.data) # in seconds (otherwise decimals)
			#According to the image, put the required cooking time here. If no cooking is required, put 0
			if cooking_time != 0:
				q_write.put(str(cooking_time))
