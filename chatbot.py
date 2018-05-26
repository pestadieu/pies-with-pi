import os
import time
import re
from slackclient import SlackClient
from threading import Thread

slack_token = 'xoxb-312006303360-371464832150-kuFiBgI93LbnMT5PwbPjki9R'

sc = SlackClient(slack_token)

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
	# ~ ch += "snap                       sends a photo of the food."
	return ch

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

def parse_direct_mention(message_text):
	"""
		Finds a direct mention (a mention that is at the beginning) in message text
		and returns the user ID which was mentioned. If there is no direct mention, returns None
	"""
	matches = re.search(MENTION_REGEX, message_text)
	# the first group contains the username, the second group contains the remaining message
	return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
	"""
		Executes bot command if the command is known
	"""
	# Default response is help text for the user
	default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

	# Finds and executes the given command, filling in response
	response = None
	# This is where you start to implement more commands!
	if command.startswith(EXAMPLE_COMMAND):
		response = display_help()
	elif command.startswith("time"):
		response = "The remaining time is"
	elif command.startswith("stop"):
		response = "Stop this microwave"
	elif command.startswith("start"):
		response = "Manual start"
	# ~ elif command.startswith("snap"):
		# ~ response = "Manual start"
	# ~ elif command.startswith("keepwarm"):
		# ~ response = "Manual start"
	else:
		response = default_response

	# Sends the response back to the channel
	slack_client.api_call(
		"chat.postMessage",
		channel=channel,
		text=response
	)

class Chatbot(Thread):
	
	def __init__(self, q_write, q_read):
		Thread.__init__(self)
		self.name = "chatbot.py"
		self.q_read = q_read
		self.q_write = q_write
		if slack_client.rtm_connect(with_team_state=False):
			print("Starter Bot connected and running!")
			# Read bot's user ID by calling Web API method `auth.test`
			starterbot_id = slack_client.api_call("auth.test")["user_id"]
			while True:
				command, channel = parse_bot_commands(slack_client.rtm_read())
				if command:
					print command, channel
					self.command = command
					self.channel = channel
					self.handle_command()
				time.sleep(RTM_READ_DELAY)
		else:
			print("Connection failed. Exception traceback printed above.")
		
	def handle_command(self):
		"""
			Executes bot command if the command is known
		"""
		# Default response is help text for the user
		default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

		# Finds and executes the given command, filling in response
		response = None
		# This is where you start to implement more commands!
		if self.command.startswith(EXAMPLE_COMMAND):
			response = display_help()
		elif self.command.startswith("time"):
			response = "The remaining time is" + q_read.get()
		elif self.command.startswith("stop"):
			q_write.put("STOP")
			# ~ response = "Stop this microwave"
		elif self.command.startswith("start"):
			# ~ response = "Manual start"
			q_write.put("START")
			try:
				q_write.put(self.command.split()[1])
			except:
				q_write.put("0")
		# ~ elif self.command.startswith("snap"):
			# ~ response = "Manual start"
		# ~ elif self.command.startswith("keepwarm"):
			# ~ response = "Manual start"
		else:
			response = default_response

		# Sends the response back to the channel
		slack_client.api_call(
			"chat.postMessage",
			channel=channel,
			text=response
		)

# ~ if __name__ == "__main__":
	# ~ if slack_client.rtm_connect(with_team_state=False):
		# ~ print("Starter Bot connected and running!")
		# ~ # Read bot's user ID by calling Web API method `auth.test`
		# ~ starterbot_id = slack_client.api_call("auth.test")["user_id"]
		# ~ while True:
			# ~ command, channel = parse_bot_commands(slack_client.rtm_read())
			# ~ if command:
				# ~ print command, channel
				# ~ handle_command(command, channel)
			# ~ time.sleep(RTM_READ_DELAY)
	# ~ else:
		# ~ print("Connection failed. Exception traceback printed above.")