# import praw
# import time
from PIL import Image, ImageDraw, ImageFont

# returns True if 'str' has a segment of consecutive characters of length 'size'
def has_consecutive_chars(str, size):
	char_counts = []
	for char in str:
		if len(char_counts) != 0:
			if char_counts[-1][0] == char:
				char_counts[-1][1] += 1
				# check for consecutive condition
				if (char_counts[-1][1] >= size):
					return True
			else:
				char_counts.append([char, 1])
		else:
			char_counts.append([char, 1])
	return False

# determines whether or not a string is ascii art, using a "very sophisticated" algorithm
def is_ascii_art(str):
	num_lines = len(str.splitlines())
	return num_lines >= 5 and has_consecutive_chars(str, 5)

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

# use 12pt Courier New for ASCII art
font = ImageFont.truetype("cour.ttf", 12)

# pull text from file
with open('data.txt', 'r') as myfile:
	data = myfile.read()

if is_ascii_art(data):
	data_by_line = data.split("\n")
	num_of_lines = len(data_by_line)

	# create a placeholder image to determine correct image
	img = Image.new('RGB', (1,1))
	d = ImageDraw.Draw(img)
	
	line_widths = []
	for i, line in enumerate(data_by_line):
		line_dimensions = d.textsize(data_by_line[i], font=font)
		line_widths.append(line_dimensions[0])
	line_height = d.textsize(data)[1]					# the height of a line of text is unchanging

	img_width = max(line_widths)								# the image width is the largest of the individual line widths
	img_height = num_of_lines * line_height		# the image height is the # of lines * line height

	# creating the output image
	img = Image.new('RGB', (img_width, img_height), 'white')
	d = ImageDraw.Draw(img)

	for i, line in enumerate(data_by_line):
		text = unicode(data_by_line[i],'utf-8')
		d.text((0,i*line_height), text, font=font, fill='black')
	img.save("data.png", 'png')