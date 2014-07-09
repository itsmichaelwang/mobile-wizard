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
	user_agent = ("mobile-wizard: Reddit post2image conversion bot for mobile users"
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
		if keyword.lower() in comment.body.lower():
			output.append(comment)
	return output

def get_parent(comment):
	if comment.is_root:
		parent = comment.submission
		parent_text = parent.selftext
	else:
		parent = r.get_info(thing_id=comment.parent_id)
		parent_text = parent.body
	output = [parent, parent_text]
	return output

def is_valid(comment, comment_history):
	"""Determines whether or not the parent submission/comment of a comment requesting ascii-wizard's services should be converted and posted.
	RULES:
		Do not convert empty posts/image posts
		Do not convert posts shorter than 3 lines
		Do not convert the parents of comments whose parents have already been converted
		Do not convert comments if the submission in which in the comment exists has already been visited 5 times

	Args:
		comment: The comment in question
		comment_history: A dictionary with key=submission ID => value=[array of IDs of converted comments]. To make persistance, I used a json file (see below)
	Returns:
		False if the comment given violates any of the above rules, otherwise True
	"""
	submission_id = comment.submission.id
	output = get_parent(comment)
	parent_id = output[0].id
	parent_text = output[1]
	# don't do more than MAX_COMMENTS responses, don't repeat responses, ignore empty comments
	MAX_COMMENTS = 5
	if not parent_text:
		print("ERROR: Empty/invalid input")
		return False
	if len(parent_text.splitlines()) < 3:
		print("ERROR: Input too short")
		return False
	if submission_id in comment_history:
		if len(comment_history.get(submission_id, [])) >= MAX_COMMENTS:
			print("ERROR: Limit reached")
			return False
		if parent_id in comment_history[submission_id]:
			print("ERROR: Already processed")
			return False
	# otherwise, return true
	return True

def reply_with_image(r, comment, comment_history):
	"""For the given comment, reply to that comment with a picture of the comment's parent. The function does not return anything.

	Args:
		r: The praw.Reddit class, which is required to access the Reddit API and can be gotten from automatic_reddit_login() or praw's login() function
		comment: The comment to reply to.
	"""
	# if 'comment' is a root comment, its parent is the submission itself
	# if 'comment' is not a root comment, its parent is the comment above it
	submission_id = comment.submission.id
	output = get_parent(comment)
	parent_id = output[0].id
	parent_text = output[1]
	# convert/upload the parent post to imgur
	image = strtoimg.str_to_img(parent_text)
	uploaded_image_url = imgur.upload_image(image, comment.permalink)
	# reply to 'comment'
	reply_text = ">" + uploaded_image_url + "\n>=" + "\n\n^An ^image ^version ^of ^this ^post ^was ^created ^because ^it ^was ^indicated ^that ^it ^was ^hard ^for ^mobile ^users ^to ^see." + "\n\n^[Github](https://github.com/itsmichaelwang/ascii-wizard) ^| ^This ^bot ^posts ^a ^maximum ^of ^5 ^times ^in ^a ^submission, ^as ^an ^anti-spam ^measure."
	comment.reply(reply_text)
	# update the comment history to reflect this
	comment_history[submission_id] = comment_history.get(submission_id, [])
	comment_history[submission_id].append(parent_id)
	comment_history_json.seek(0)
	json.dump(comment_history, comment_history_json)

def delay(start, delay_time):
	"""From a given point in time, delay execution until a certain amount of time has passed.

	Args:
		start: The point in time to start counting from, in seconds. The easiest way to get this is to create an instance of time.time() somewhere in your code, and pass it in.
		delay_time: The time, in seconds after start, that the function should delay execution until
	"""
	elapsed_time = time.time() - start
	while (elapsed_time < delay_time):
		print(delay_time - elapsed_time, end='\r')
		elapsed_time = time.time() - start

# start shit
r = automatic_reddit_login('credentials.json')
while True:
	# intentional time delay (see below)
	start = time.time()
	print("Fetching...")
	# dictionary to track and limit the # of conversions in a submission, user to limit posts
	# submission ID => [array of converted comment IDs]
	comment_history_json = open('completed.json', 'r+')
	comment_history = json.load(comment_history_json)
	# fetch relevant comments
	for comment in comments_by_keyword(r, 'rip mobile users', subreddit='all'):
		print(comment.body)
		# check if repeat, or over the limit
		if is_valid(comment, comment_history):
			reply_with_image(r, comment, comment_history)
	# Reddit recent comments page is cached every 30 seconds, so wait 30 (+5 for error) seconds until fetching comments again
	delay(start, 35)