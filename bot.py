# import praw
# import time
from functions import *

# user_agent = ("ascii2image for Mobile Users Bot by /u/Zapurdead")
# r = praw.Reddit(user_agent=user_agent)

# from credentials import *
# user = r.login(username=user_name, password=pass_word)

# limit the amount of conversions per submission
# converted_comments is a hash table with the submission ID as the key and an array of coverted comment IDs as the value
# converted_comments = {}
# max_conversions = 5

# def get_stream( subreddit ):
# 	comment_stream = praw.helpers.comment_stream(r, subreddit, limit=1)
# 	for comment in comment_stream:
# 		yield comment

with open ("data.txt", "r") as myfile:
	data = myfile.read()

print is_ascii_art(data)



