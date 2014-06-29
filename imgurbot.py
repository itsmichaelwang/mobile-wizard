import requests
from credentials import imgur_access_token

#this part of the bot uploads a specified file to imgur (will be merged in eventually)
url = 'https://api.imgur.com/3/image'
header = {
	'Authorization': 'Bearer ' + imgur_access_token
}
payload = {
	'image':'data.PNG',
	'type':'file',
	'title':"Test Image",
	'description':"Test of the ASCII-Bot"
}
r = requests.post(url, data=payload, headers=header)
print r