from __future__ import print_function
from time import strftime
from time import sleep
import praw
import json
import configparser
import requests

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
		user = r.login(username=r_username, password=r_password)
	else:
		user = r.login()
	return r

def comments_by_keyword(r, keyword, subreddit='all', print_comments=False):
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
	comments = r.get_comments(subreddit, limit=750)

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
		False if the comment given violates an anti-spam rule, otherwise True
	"""
	submission_id = comment.submission.id
	output = get_parent(comment)
	parent_id = output[0].id
	parent_text = output[1]

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

r = reddit_login('credentials.ini')

while True:
	try:
		print("Fetching comments...")
		print("=====\n")

		with open('completed.json', 'r') as comment_history_file:
			comment_history = json.load(comment_history_file)

		for comment in comments_by_keyword(r, 'rip mobile users', subreddit='all', print_comments=True):
			if is_valid(comment, comment_history):
				reply_with_image(r, comment, comment_history)
		# Reddit caches recent comments every 30 seconds, so fetch comments in intervals of a little over 30 seconds
		print("Last Successful Query (System Time): " + strftime("%Y-%m-%d %I:%M:%S\n"))
	except requests.exceptions.HTTPError as e:
		msg = "Error " + str(e.code) + ": " + str(e)
		r.send_message('Zapurdead', "[MOBILE-WIZARD]", msg)
		pass

	sleep(30)