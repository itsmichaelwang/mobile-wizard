from PIL import Image, ImageDraw, ImageFont
from types import *
import sys
from io import StringIO

import strtoimg

def main():
	with open('test.txt', 'r', encoding='utf-8') as file:
		context = file.readlines()
		str = "".join(context)

		img = strtoimg.str_to_img(str, True)

if __name__ == "__main__":
	main()