import requests
import json
from base64 import b64encode

def get_access_token():
	payload = {'refresh_token': imgur_refresh_token,
						 'client_id': imgur_client_ID,
						 'client_secret': imgur_client_secret,
						 'grant_type':'refresh_token'}
	r = requests.post('https://api.imgur.com/oauth2/token', data=payload)
	content = json.loads(r.content)
	access_token = content['access_token']
	return access_token

def upload_image(img, title):
	# load oauth credentials from 'credentials.json'
	credentials_json = open('credentials.json', 'r+')
	credentials = json.load(credentials_json)
	global imgur_access_token
	global imgur_refresh_token
	global imgur_client_ID
	global imgur_client_secret
	imgur_access_token = credentials['imgur_access_token']
	imgur_refresh_token = credentials['imgur_refresh_token']
	imgur_client_ID = credentials['imgur_client_ID']
	imgur_client_secret = credentials['imgur_client_secret']

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
		r = requests.post(url, data=payload, headers=header)
		print(r)
		status_code = r.status_code
		# success, return link
		if (status_code == 200):
			credentials_json.close()
			data = json.loads(r.text)['data']
			return data['link']
		# invalid access token - generate a new one and print it (storing to file will come later)
		if (status_code == 403):
			imgur_access_token = get_access_token()
			print "Generating new access token: " + imgur_access_token
			credentials['imgur_access_token'] = imgur_access_token
			credentials_json.seek(0)
			json.dump(credentials, credentials_json)
			header = {
				'Authorization': 'Bearer ' + imgur_access_token
			}