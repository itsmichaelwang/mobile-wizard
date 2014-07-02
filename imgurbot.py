import requests
from base64 import b64encode
from credentials import imgur_access_token

#this part of the bot uploads a specified file to imgur (will be merged in eventually)
url = 'https://api.imgur.com/3/image'
header = {
	'Authorization': 'Bearer ' + imgur_access_token
}
payload = {
	'image':b64encode(open('data.png', 'rb').read()),
	'type':'base64',
	'title':"Test Image",
	'description':"Test of the ASCII-Bot"
}
r = requests.post(url, data=payload, headers=header)
print r