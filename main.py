#!/usr/bin/python

from queue import Queue
from chatbot import *
from camera import *
from door_state import *

if(__name__ == '__main__'):
	queue_camera_timer = Queue() # queue from the camera to the chatbot
	#queue_timer_camera = Queue()

	thread_cam = Camera(queue_camera_timer)   # Camera thread
	thread_chat = Chatbot()  # Chatbot thread
	thread_door = DoorState()  # Door state thread
	thread_timer = Timer(queue_camera_timer) # Timer thread

	thread_cam.start()
	thread_chat.start()
	thread_door.start()
	thread_timer.start()
