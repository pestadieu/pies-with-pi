import os
import time
from threading import Thread
from queue import Queue
import door_state as ds
import handle_lcd as hl

class Timer(Thread):

	def __init__(self, q_write):
		Thread.__init__(self)
		self.name = "timer_thread"
		self.q_timer = q_timer
        self.t_timeout = 0

	def run(self):
		while True:
            if self.t_timeout == 0:
                remaining_time = 0
    		else:
    				remaining_time = self.t_timeout - (time.time() - self.t_start)
    		if remaining_time < 0:
    			remaining_time = 0
    		hl.printTime(remaining_time)
    		print("timer get time" + str(remaining_time))

            time.sleep(1)


    def timer_start(timeout):
		print("timer start" + str(timeout))
		hl.printTime(timeout)
		while(ds.DOOR_CLOSED == False): # We wait until the door close
			pass
		self.t_start = time.time()
		self.t_timeout = timeout

	"""def timer_get_time(self):
		if self.t_timeout == 0: remaining_time = 0
		else:
					remaining_time = self.t_timeout - (time.time() - self.t_start)
		if remaining_time < 0:
			remaining_time = 0
		hl.printTime(remaining_time)
		print("timer get time" + str(remaining_time))
		return remaining_time"""

	def timer_stop(self):
		print('timer stop')
		ds.DOOR_CLOSED == False
		self.t_start = 0
