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
	# submit user agent
	user_agent = ("ascii-wizard: Reddit post2image conversion bot for mobile users"
								"Version 1.0b by /u/Zapurdead")
	r = praw.Reddit(user_agent=user_agent)

	# if credentials are provided, use them, otherwise prompt
	if credentials_file != None:
		with open(credentials_file, 'r') as credentials_json:
			credentials = json.load(credentials_json)
			r_username = credentials['reddit_username']
			r_password = credentials['reddit_password']
		user = r.login(username=r_username, password=r_password)
	else:
		user = r.login()
	return r

def comments_by_keyword(r, keyword, subreddit='all', limit=250, print_comments=False):
	"""Gets all recent comments from a subreddit containing a keyword or phrase

	Args:
		r: The praw.Reddit class, which is required to access the Reddit API and can be gotten from automatic_reddit_login() or praw's login() function
		keyword: A string with the keyword or phrase to filter comments with
		subreddit: A string with the subreddit to trawl through, default is 'all' for r/all (similar pattern, ex: 'wtf' for r/wtf)
		limit: The maximum number of posts to crawl through at once
		print_comments: If true, comments_by_keyword will print every comment it sees

	Returns:
		An array of comment objects containing all the relevant posts
	"""
	# array of comments that contain the keyword
	output = []
	comments = r.get_comments(subreddit, limit=limit)
	for comment in comments:
		if print_comments:
			print(comment)
		if keyword in comment.body:
			output.append(comment)
	return output

# mind the negative
def is_unnecessary(comment, comment_history_file):
	"""Determines whether or not the parent submission/comment of a comment requesting ascii-wizard's services should be converted and posted.
	RULES:
		Do not convert comments that have already been converted.
		Do not convert comments if the submission in which in the comment exists has already been visited 5 times

	Args:
		comment: The comment in question
		comment_history_file: The name of a json file containing a dictionary with key=submission ID => value=[array of IDs of converted comments]. To initialize, one can simply make a blank json file, and ascii-wizard will do all the work

	Returns:
		False if the comment given violates any of the above rules, otherwise False
	"""


# def post_reply(comment):


# start shit
r = automatic_reddit_login('credentials.json')

# dictionary to track and limit the # of conversions in a submission, user to limit posts
# submission => converted comment
completed_json = open('completed.json', 'r+')
completed = json.load(completed_json)

while True:
	# intentional time delay (see below)
	start = time.time()
	# fetch relevant comments
	for comment in comments_by_keyword(r, 'rip mobile users', subreddit='test'):
		print("Keyworded comment: " + comment.body)
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