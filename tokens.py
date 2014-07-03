import requests
import json

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