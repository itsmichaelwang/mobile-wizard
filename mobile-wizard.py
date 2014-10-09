from __future__ import print_function
from collections import deque
from urllib2 import HTTPError
import praw
import json
import time
import datetime
import configparser

import sys
import os.path

# user-made modules
import strtoimg
import imgur

# login to Reddit using optional credentials file
def reddit_login(credentials_file=None):
	user_agent = ("mobile-wizard: post2image conversion bot for mobile users by /u/Zapurdead")
	r = praw.Reddit(user_agent=user_agent)

	if credentials_file:
		config = configparser.ConfigParser()
		config.read(credentials_file)
		global r_username
		global r_password
		r_username = config['REDDIT']['reddit_username']
		r_password = config['REDDIT']['reddit_password']
		user = r.login(username=reddit_username, password=reddit_password)
	else:
		user = r.login()
	return r

def comments_by_keyword(r, keyword, subreddit='all', limit=1000, print_comments=False):
	"""Fetches comments from a subreddit containing a given keyword or phrase

	Args:
		r: The praw.Reddit class, which is required to access the Reddit API
		keyword: Keep only the comments that contain the keyword or phrase
		subreddit: A string denoting the subreddit(s) to look through, default is 'all' for r/all
		limit: The maximum number of posts to fetch, increase for more thoroughness at the cost of increased redundancy/running time
		print_comments: (Debug option) If True, comments_by_keyword will print every comment it fetches, instead of just returning filtered ones

	Returns:
		An array of comment objects whose body text contains the given keyword or phrase
	"""
	output = []

	try:
		comments = r.get_comments(subreddit, limit=limit)
	except urllib2.HTTPError, e:
		msg = "Reddit error " + e.code + ": Restart required"
		r.send_message('Zapurdead', 'mobile-wizard', msg)

	for comment in comments:
		# ignore the case of the keyword and comments being fetched
		# Example: for keyword='RIP mobile users', comments_by_keyword would keep 'rip Mobile Users', 'rip MOBILE USERS', etc.
		if keyword.lower() in comment.body.lower():
			print(comment.body.encode('utf-8'))
			print("=====\n")
			output.append(comment)
		elif print_comments:
			print(comment.body.encode('utf-8'))
			print("=====\n")
	return output

def get_parent(comment):
	"""Returns submission and its selftext if the given comment is a root comment, otherwise returns the comment's parent and its body

	Args:
		comment: A praw comment object, the given comment

	Returns:
		An array, where array[0] is the parent object, and array[1] is its text (returns blank if contents are an image)
	"""
	if comment.is_root:
		parent = comment.submission
		parent_text = parent.selftext
	else:
		parent = r.get_info(thing_id=comment.parent_id)
		parent_text = parent.body
	output = [parent, parent_text]
	return output

def is_valid(comment, comment_history):
	"""Determines whether or not the parent (see get_parent) of the given comment should be converted/posted

	Args:
		comment: The comment in question
		comment_history: A dictionary with key=submission ID => value=[array of IDs of converted comments for that submission].

	Returns:
		False if the comment given violates any of the above rules, otherwise True
	"""
	submission_id = comment.submission.id
	output = get_parent(comment)
	parent_id = output[0].id
	parent_text = output[1]

	# RULES:
	# Do not convert empty posts/image posts (which are returned as empty anyways)
	# Do not convert posts shorter than 3 lines
	# Do not convert the parents of comments whose parents have already been converted
	# Do not convert comments if the submission in which in the comment exists has already been visited 5 times
	MAX_COMMENTS = 3
	if not parent_text:
		print("ERROR: Empty/invalid input")
		return False
	if len(parent_text.splitlines()) <= 3:
		print("ERROR: Input was too short (three lines or shorter)")
		return False
	if submission_id in comment_history:
		if len(comment_history.get(submission_id, [])) >= MAX_COMMENTS:
			print("ERROR: Submission response cap reached")
			return False
		if parent_id in comment_history[submission_id]:
			print("ERROR: Comment already processed")
			return False
	if output[0].author.name == "mobile-wizard":
		print("ERROR: Attempted to convert own post")
		return False
	# otherwise, return true
	return True

def reply_with_image(r, comment, comment_history):
	"""Reply to the given comment with a picture of the comment's parent. The function does not return anything.

	Args:
		r: The praw.Reddit class, which is required to access the Reddit API
		comment: The comment to reply to
	"""
	# see get_parent for more information
	submission_id = comment.submission.id
	output = get_parent(comment)
	parent_id = output[0].id
	parent_text = output[1]
	# convert/upload the parent post to imgur
	image = strtoimg.str_to_img(parent_text)
	uploaded_image_url = imgur.upload_image(image, comment.permalink)
	# post the reply to Reddit
	reply_text = ">" + uploaded_image_url + "\n>=" + "\n\n^An ^image ^version ^of ^this ^post ^was ^created ^because ^it ^was ^indicated ^that ^it ^was ^hard ^for ^mobile ^users ^to ^see." + "\n\n^[Github](https://github.com/itsmichaelwang/ascii-wizard) ^| ^This ^bot ^features ^multiple ^[anti-spam](https://github.com/itsmichaelwang/mobile-wizard/blob/master/README.md#anti-spam) ^measures."
	comment.reply(reply_text)
	# update the comment history to reflect this, and flush it to a json file for future reference
	with open('completed.json', 'r+') as comment_history_file:
		comment_history[submission_id] = comment_history.get(submission_id, [])
		comment_history[submission_id].append(parent_id)
		comment_history_file.seek(0)
		json.dump(comment_history, comment_history_file)

def delay(start, delay_time):
	"""From a given point in time (that was marked before delay was called), halt execution until a certain amount of time has passed.

	Args:
		start: The point in time to start counting from, in seconds. The easiest way to get this is to create an instance of time.time() somewhere in your code, and pass it in
		delay_time: The time, in seconds after start, that the function should delay execution until
	"""
	elapsed_time = time.time() - start
	while (elapsed_time < delay_time):
		print(delay_time - elapsed_time, end='\r')
		elapsed_time = time.time() - start
	print("")

r = reddit_login('credentials.ini')

while True:
	start = time.time()	# to get posts from Reddit at regular intervals, keep track of the start time
	print("Fetching comments...")
	print("=====\n")

	with open('completed.json', 'r') as comment_history_file:
		comment_history = json.load(comment_history_file)

	for comment in comments_by_keyword(r, 'rip mobile users', subreddit='all', print_comments=True):
		if is_valid(comment, comment_history):
			reply_with_image(r, comment, comment_history)
	# Reddit caches recent comments every 30 seconds, so fetch comments in intervals of a little over 30 seconds
	print("Last Successful Query (UTC): " + str(datetime.datetime.utcnow()) + "\n")
	delay(start, 35)