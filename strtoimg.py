from PIL import Image, ImageDraw, ImageFont
from cStringIO import StringIO
import HTMLParser

def str_to_img(str):
	"""Converts a given string to a PNG image, and saves it to the return variable"""
	# use 12pt Courier New for ASCII art
	font = ImageFont.truetype("cour.ttf", 12)

	# do some string preprocessing
	str = str.replace("\n\n", "\n")	# Reddit requires double newline for new line, don't let the bot do this
	h = HTMLParser.HTMLParser()
	str = h.unescape(str).encode('utf-8') # convert HTML entities to plain text

	# create a placeholder image to determine correct image
	img = Image.new('RGB', (1,1))
	d = ImageDraw.Draw(img)
	
	str_by_line = str.split("\n")
	num_of_lines = len(str_by_line)
	
	line_widths = []
	for i, line in enumerate(str_by_line):
		line_widths.append(d.textsize(str_by_line[i], font=font)[0])
	line_height = d.textsize(str, font=font)[1]		# the height of a line of text should be unchanging

	img_width = max(line_widths)									# the image width is the largest of the individual line widths
	img_height = num_of_lines * line_height				# the image height is the # of lines * line height

	# creating the output image
	# add 5 pixels to account for lowercase letters that might otherwise get truncated
	img = Image.new('RGB', (img_width, img_height + 5), 'white')
	d = ImageDraw.Draw(img)

	for i, line in enumerate(str_by_line):
		d.text((0,i*line_height), line, font=font, fill='black')
	output = StringIO()
	img.save(output, format='PNG')

	return output