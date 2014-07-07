from PIL import Image, ImageDraw, ImageFont
from cStringIO import StringIO

# str is the ASCII art string to be converted
def str_to_img(str):
	# use 12pt Courier New for ASCII art
	font = ImageFont.truetype("cour.ttf", 12)

	str_by_line = str.split("\n")
	num_of_lines = len(str_by_line)

	# create a placeholder image to determine correct image
	img = Image.new('RGB', (1,1))
	d = ImageDraw.Draw(img)
	
	line_widths = []
	for i, line in enumerate(str_by_line):
		line_widths.append(d.textsize(str_by_line[i], font=font)[0])
	line_height = d.textsize(str, font=font)[1]		# the height of a line of text should be unchanging

	img_width = max(line_widths)									# the image width is the largest of the individual line widths
	img_height = num_of_lines * line_height				# the image height is the # of lines * line height

	# creating the output image
	img = Image.new('RGB', (img_width, img_height), 'white')
	d = ImageDraw.Draw(img)

	for i, line in enumerate(str_by_line):
		d.text((0,i*line_height), line, font=font, fill='black')
	output = StringIO()
	img.save(output, format='JPEG')

	return output