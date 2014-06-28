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

