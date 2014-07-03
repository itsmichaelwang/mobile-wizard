import requests
from base64 import b64encode
from credentials import imgur_access_token

# required for get_access_token
from tokens import *

def upload_image(filename):
	url = 'https://api.imgur.com/3/image'
	#encode image for POST request
	with open(filename, 'rb') as myfile:
		data = b64encode(myfile.read())

	payload = {
		'image':data,
		'type':'base64',
		'title':"Test Image",
		'description':"Test of the ASCII-Bot"
	}
	header = {
		'Authorization': 'Bearer ' + imgur_access_token
	}

	status_code = 0
	while (status_code != 200):
		# invalid access token - generate a new one and print it (storing to file will come later)
		if (status_code == 403):
			new_access_token = get_access_token()
			print new_access_token
			header = {
				'Authorization': 'Bearer ' + new_access_token
			}

		r = requests.post(url, data=payload, headers=header)
		print r
		status_code = r.status_code

upload_image('data.png')
