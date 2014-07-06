from __future__ import print_function
import praw
import json
import time

# custom modules
import strtoimg
import imgur

# use the credentials file to load username/password
with open('credentials.json', 'r') as credentials_json:
	credentials = json.load(credentials_json)
	global reddit_user_name
	global reddit_pass_word
	reddit_user_name = credentials['reddit_user_name']
	reddit_pass_word = credentials['reddit_pass_word']

# login to Reddit
user_agent = ("ascii-wizard"
							"ASCII art to image conversion for mobile users bot"
							"Version 1.0b by /u/Zapurdead")
r = praw.Reddit(user_agent=user_agent)
user = r.login(username=reddit_user_name, password=reddit_pass_word)

# dictionary of track of submissions => comments that have been modified
already_done = {}

while True:
	print("Fetching comments...")
	start = time.time()
	comments = r.get_comments('all', limit=250)
	for comment in comments:
		print(comment)
		if "rip mobile users" in comment.body:
			if comment.is_root:
				parent = comment.submission
				parent_text = parent.selftext
			else:
				parent = r.get_info(thing_id=comment.parent_id)
				parent_text = parent.body
			# checks to make sure the string isn't empty before converting it
			if parent_text:
				if strtoimg.is_valid(parent_text, 5, 15):
					image = strtoimg.str_to_img(parent_text)
					link = imgur.upload_image(image, parent.permalink)
					# make a post
					comment.reply(link)

	# Reddit recent comments page is cached every 30 seconds, so wait 30 (+5 for error) seconds until fetching comments again
	elapsed_time = time.time() - start
	MIN_WAIT_TIME = 35
	while (elapsed_time < MIN_WAIT_TIME):
		print(MIN_WAIT_TIME - elapsed_time, end='\r')
		elapsed_time = time.time() - start