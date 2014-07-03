import requests
import json
from base64 import b64encode

from credentials import imgur_access_token
from credentials import imgur_refresh_token
from credentials import imgur_client_ID
from credentials import imgur_client_secret

def get_access_token():
	payload = {'refresh_token': imgur_refresh_token,
						 'client_id': imgur_client_ID,
						 'client_secret': imgur_client_secret,
						 'grant_type':'refresh_token'}
	r = requests.post('https://api.imgur.com/oauth2/token', data=payload)
	content = json.loads(r.content)
	access_token = content['access_token']
	
	return access_token

def upload_image(img):
	url = 'https://api.imgur.com/3/image'
	#encode image for POST request
	img_data = b64encode(img.getvalue())
	payload = {
		'image':img_data,
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