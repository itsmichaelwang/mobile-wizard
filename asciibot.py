from __future__ import print_function
import praw
import json
import time

# custom modules
import strtoimg
import imgur

# login to Reddit
user_agent = ("ascii-wizard"
							"ASCII art to image conversion for mobile users bot"
							"Version 1.0b by /u/Zapurdead")
with open('credentials.json', 'r') as credentials_json:
	credentials = json.load(credentials_json)
	global reddit_user_name
	global reddit_pass_word
	reddit_user_name = credentials['reddit_user_name']
	reddit_pass_word = credentials['reddit_pass_word']

r = praw.Reddit(user_agent=user_agent)
user = r.login(username=reddit_user_name, password=reddit_pass_word)

# keep track of what has been analyzed
already_done = {}

# analyze comments as they are made
while True:
	start = time.time()
	print("Retrieving the 150 most recent comments...")
	comments = r.get_comments('all', limit=150)
	
	for comment in comments:
		print(comment)
		if strtoimg.is_ascii_art(comment.body):
			print("^ASCII ART")
			image = strtoimg.str_to_img(comment.body)
			imgur.upload_image(image)
		else:
			print("^NOT ASCII ART")

	# Reddit comment stream is cached every 30 seconds, so wait 30 (+5 for imperfections) seconds until fetching comments again
	elapsed_time = time.time() - start
	MIN_WAIT_TIME = 35
	while (elapsed_time < MIN_WAIT_TIME):
		print(MIN_WAIT_TIME - elapsed_time, end='\r')
		elapsed_time = time.time() - start