from PIL import Image, ImageDraw, ImageFont
from types import *
import sys
import cStringIO

import strtoimg

def main(arg):
	assert type(arg) is StringType, "input var is not a string: %r" % arg
	img = strtoimg.str_to_img(arg, True)

if __name__ == "__main__":
	main(sys.argv[1])