#!/usr/bin/python

from queue import Queue
from chatbot import *
# ~ from camera import *

if(__name__ == '__main__'):
	queue_camera_chatbot = Queue() # queue from the camera to the chatbot
	queue_chatbot_camera = Queue() # queue from the chatbot to the camera

	thread_cam = camera(queue_camera_chatbot, queue_chatbot_camera)   # Camera thread
	thread_chat = server(queue_chatbot_camera, queue_camera_chatbot)  # Chatbot thread
	
	thread_cam.start()
	thread_chat.start()
