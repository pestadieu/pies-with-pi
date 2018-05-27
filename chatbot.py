import os
import time
import re
from slackclient import SlackClient
from threading import Thread
from queue import Queue
import door_state as ds
import handle_lcd as hl

slack_token = 'xoxb-312006303360-371464832150-kuFiBgI93LbnMT5PwbPjki9R'

# instantiate Slack client
slack_client = SlackClient(slack_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "help"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def display_help():
	ch  = "Alvailable Commands: \n"
	ch += "time [time in seconds]     show the remaining cooking time."
	ch += "stop                       stop the microwave."
	ch += "start [time in seconds]    manually start the microwave."
	# ~ ch += "keepwarm                   keep the food warm until you come back."
	ch += "snap                       sends a photo of the food."
	return ch

def send_text_response(response, channel):
	slack_client.api_call(
			"chat.postMessage",
			channel=channel,
			text=response
		)

def parse_bot_commands(slack_events):
	"""
		Parses a list of events coming from the Slack RTM API to find bot commands.
		If a bot command is found, this function returns a tuple of command and channel.
		If its not found, then this function returns None, None.
	"""
	for event in slack_events:
		if event["type"] == "message" and not "subtype" in event:
			user_id, message = parse_direct_mention(event["text"])
			if user_id == starterbot_id:
				return message, event["channel"]
	return None, None

def send_file():
	a = slack_client.api_call(
		'files.upload',
		channels="pies-with-pies-test",
		filename='pic.jpg',
		file=open('test.jpg', 'rb')
	)
	print( "file sent")

def parse_direct_mention(message_text):
	"""
		Finds a direct mention (a mention that is at the beginning) in message text
		and returns the user ID which was mentioned. If there is no direct mention, returns None
	"""
	matches = re.search(MENTION_REGEX, message_text)
	# the first group contains the username, the second group contains the remaining message
	return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

class Chatbot(Thread):

	def __init__(self, q_read):
		Thread.__init__(self)
		self.name = "chatbot_thread"
		self.q_read = q_read
		self.t_timeout = 0

	def run(self):
		if slack_client.rtm_connect(with_team_state=False):
			print("Starter Bot connected and running!")
			# Read bot's user ID by calling Web API method `auth.test`
			starterbot_id = slack_client.api_call("auth.test")["user_id"]
			while True:
				command, channel = parse_bot_commands(slack_client.rtm_read())
				if command:
					print (command, channel)
					self.command = command
					self.channel = channel
					self.handle_command()

				if not self.q_read.empty:
					pass # Handle incoming command

				self.timer_get_time()

				time.sleep(RTM_READ_DELAY)
		else:
			print("Connection failed. Exception traceback printed above.")

	def timer_start(timeout):
		print("timer start" + str(timeout))
		hl.printTime(timeout)
		while(ds.DOOR_CLOSED == False): # We wait until the door close
			pass
		self.t_start = time.time()
		self.t_timeout = timeout

	def timer_get_time(self):
		if self.t_timeout == 0: remaining_time = 0
		else:
					remaining_time = self.t_timeout - (time.time() - self.t_start)
		if remaining_time < 0:
			remaining_time = 0
		hl.printTime(remaining_time)
		print("timer get time" + str(remaining_time))
		return remaining_time

	def timer_stop(self):
		print('timer stop')
		ds.DOOR_CLOSED == False
		self.t_start = 0

	def handle_command(self):
		"""
			Executes bot command if the command is known
		"""
                 print("Handle command" + self.command)
		# Default response is help text for the user
		default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

		# Finds and executes the given command, filling in response
		response = None
		# This is where you start to implement more commands!
		if self.command.startswith(EXAMPLE_COMMAND):
			response = display_help()
		elif self.command.startswith("time"):
			response = "The remaining time is" + self.timer_get_time()
		elif self.command.startswith("stop"):
			self.timer_stop()
			response = "The microwave just stopped"
		elif self.command.startswith("start"):
			try:
				response = "The microwave just started"
				self.timer_start(int(self.command.split()[1]))
			except:
				response = "Error: Please provide a cooking time"
		elif self.command.startswith("snap"):
			send_file()
			response = "Your food seems fine"
		else:
			response = default_response
		# Sends the response back to the channel
		send_text_response(response, self.channel)
