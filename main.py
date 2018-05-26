#!/usr/bin/python

from queue import Queue
from chatbot import *
from camera import *
from door_state import *

if(__name__ == '__main__'):
	queue_camera_chatbot = Queue() # queue from the camera to the chatbot

	thread_cam = Camera(queue_camera_chatbot)   # Camera thread
	thread_chat = Chatbot(queue_camera_chatbot)  # Chatbot thread
	thread_door = DoorState()  # Door state thread
	
	thread_cam.start()
	thread_chat.start()
	thread_door.start()
