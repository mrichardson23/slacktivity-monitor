import time
from slackclient import SlackClient
from gpiozero import LED

token = "SLACK TOKEN HERE" # found at https://api.slack.com/web#authentication

red = LED(15)
yellow = LED(14)
green = LED(18)

red.off()
yellow.off()
green.off()

sc = SlackClient(token)

message_counts =[]

if sc.rtm_connect():
	while True:
		message_count = 0
		events = sc.rtm_read()
		for event in events:
			if event['type'] == 'message':
				message_count = message_count + 1
		message_counts.insert(0, message_count)
		if len(message_counts) > 600:
			message_counts.pop(600)
		total_message_count = 0
		for i in range(0,len(message_counts)):
			total_message_count = total_message_count + message_counts[i]
		if total_message_count == 0:
			red.on()
			yellow.off()
			green.off()
		if total_message_count > 0 and total_message_count < 15:
			red.off()
			yellow.on()
			green.off()
		if total_message_count >= 15:
			red.off()
			yellow.off()
			green.on()
		time.sleep(.1)
else:
	print "Connection Failed, invalid token?"
