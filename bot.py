import praw

user_agent = ("ascii2image for Mobile Users Bot by /u/Zapurdead")
r = praw.Reddit(user_agent=user_agent)

user_name = "ascii-wizard"
user = r.login(username=user_name)

# limit the amount of conversions per submission
# converted_comments is a hash table with the submission ID as the key and an array of coverted comment IDs as the value
converted_comments = {}
max_conversions = 5

subreddits = [r.get_subreddit("funny")]

for subreddit in subreddits:
	rising_submissions = subreddit.get_rising(limit=10)
	for submission in rising_submissions:
		print "Submission: " + submission.title
		converted_comments[submission.id] = converted_comments.get(submission.id, [])
		# don't convert comments in a submission if you reached the max
		if len(converted_comments[submission.id]) < max_conversions:
			flat_comment_tree = praw.helpers.flatten_tree(submission.comments)
			print "# of Comments: " + str(len(flat_comment_tree))
			for comment in flat_comment_tree:
				print comment
				if len(converted_comments[submission.id]) > max_conversions:
					break

# determines whether or not a string is ascii art, using a very sophisticated algorithm
# def is_ascii_art( str ):
	# num_lines = sum(1 for line in str)
	# if ()



