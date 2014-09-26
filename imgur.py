import requests
import json
import configparser
from base64 import b64encode

def get_access_token():
	payload = {'refresh_token': imgur_refresh_token,
						 'client_id': imgur_client_ID,
						 'client_secret': imgur_client_secret,
						 'grant_type':'refresh_token'}
	r = requests.post('https://api.imgur.com/oauth2/token', data=payload)
	data = json.loads(r.content)
	access_token = data['access_token']
	return access_token

def upload_image(img, title):
	# load oauth credentials from 'credentials.ini'
	config = configparser.ConfigParser()
	config.read('credentials.ini')
	imgur_credentials = config['IMGUR']

	global imgur_client_ID
	global imgur_client_secret
	global imgur_refresh_token
	global imgur_access_token
	
	imgur_client_ID = imgur_credentials['imgur_client_ID']
	imgur_client_secret = imgur_credentials['imgur_client_secret']
	imgur_refresh_token = imgur_credentials['imgur_refresh_token']
	imgur_access_token = imgur_credentials['imgur_access_token']
	
	url = 'https://api.imgur.com/3/image'
	#encode image for POST request
	img_data = b64encode(img.getvalue())
	payload = {
		'image':img_data,
		'type':'base64',
		'title':title,
	}
	header = {
		'Authorization': 'Bearer ' + imgur_access_token
	}

	status_code = 0
	while (status_code != 200):
		# upload image and parse response
		imgur_response = requests.post(url, data=payload, headers=header)
		print(imgur_response)											# prints the status code out as a string
		status_code = imgur_response.status_code 	# update the numeric value of the status code
		# success, return link to uploaded image
		if (status_code == 200):
			data = json.loads(imgur_response.text)['data']
			return data['link']
		# invalid access token - generate a new one and print it (storing to file will come later)
		if (status_code == 403):
			imgur_access_token = get_access_token()
			print "Generating new access token: " + imgur_access_token
			config['IMGUR']['imgur_access_token'] = imgur_access_token
			with open('credentials.ini', 'r+') as credentials:
				config.set('IMGUR', 'imgur_access_token', imgur_access_token)
				config.write(credentials)
			header = {
				'Authorization': 'Bearer ' + imgur_access_token
			}