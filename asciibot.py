from __future__ import print_function
import praw
import json
import time

# custom modules
import strtoimg
import imgur

# if you have a json file with the keys 'reddit_user_name' and 'reddit_pass_word'
def automatic_reddit_login(credentials_file=None):
	"""Logs users in automatically if credentials are provided, otherwise prompts user for input.

	Args:
		credentials_file: A string with the name of a json file with the key/value pairs 'reddit_user_name' and 'reddit_pass_word'. If not provided, will default to None, in which case the function will prompt the user for username/password.

	Returns:
		The praw.Reddit class, which allows access to Reddit's API
	"""

	# use the credentials file to load username/password
	with open(credentials_file, 'r') as credentials_json:
		credentials = json.load(credentials_json)
		r_username = credentials['reddit_username']
		r_password = credentials['reddit_password']

	# login to Reddit
	user_agent = ("ascii-wizard: Reddit post2image conversion bot for mobile users"
								"Version 1.0b by /u/Zapurdead")
	r = praw.Reddit(user_agent=user_agent)
	user = r.login(username=r_username, password=r_password)

	return r

# def comments_by_keyword():

r = automatic_reddit_login('credentials.json')

# dictionary to track and limit the # of conversions in a submissiong
# submission => converted comment
completed_json = open('completed.json', 'r+')
completed = json.load(completed_json)

while True:
	print("Fetching comments...")
	start = time.time()
	comments = r.get_comments('test', limit=250)
	for comment in comments:
		print(comment)
		
		# keyword detection
		if "rip mobile users" in comment.body:
			# detect if comments have been made
			submission_id = comment.submission.id
			comment_id = comment.id
			MAX_COMMENTS = 5
			# limit conversions per submission, and don't do repeats either
			if submission_id in completed:
				if len(completed.get(submission_id, [])) >= MAX_COMMENTS:
					continue
				if comment_id in completed[submission_id]:
					continue
			if comment.is_root:
				parent = comment.submission
				parent_text = parent.selftext
			else:
				parent = r.get_info(thing_id=comment.parent_id)
				parent_text = parent.body
			# only convert non-empty strings greater than 5x15
			if strtoimg.is_valid(parent_text, 5, 15):
				image = strtoimg.str_to_img(parent_text)
				uploaded_image_url = imgur.upload_image(image, comment.permalink)
				# make a post
				comment.reply(uploaded_image_url)
				# update completed_json
				completed[submission_id] = completed.get(submission_id, [])
				completed[submission_id].append(comment_id)
				completed_json.seek(0)
				json.dump(completed, completed_json)
	
	# Reddit recent comments page is cached every 30 seconds, so wait 30 (+5 for error) seconds until fetching comments again
	elapsed_time = time.time() - start
	MIN_WAIT_TIME = 35
	while (elapsed_time < MIN_WAIT_TIME):
		print(MIN_WAIT_TIME - elapsed_time, end='\r')
		elapsed_time = time.time() - start