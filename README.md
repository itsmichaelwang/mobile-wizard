##Mobile-Wizard
`mobile-wizard` is a Reddit bot that is trigged when someone types the phrase "rip mobile users", translating the comment above that comment into an image, hosting it on imgur, and posting it as a response.

`data.txt` and `data.png` are provided as example inputs and outputs, respectively.

###Installation Instructions
First, go ahead and clone the `mobile-wizard` repo into whatever directory you prefer. Then, make sure you have [installed pip](http://pip.readthedocs.org/en/latest/installing.html). Then, install the prerequisite packages using the included `requirements.txt` by typing:

`pip install -r requirements.txt`

Make sure to do this as root if you are on linux, otherwise it may not work. Also, Pillow can sometimes be a pain to install. If you can't get it to install on Windows 7, try the [precompiled packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/). For Linux (more specifically Debian), try the solution described in this [StackExchange post](http://unix.stackexchange.com/questions/105265/install-pil-pillow-via-pip-in-debian-testing-jessie).

Next, make a credentials file called `credentials.ini`. It should have this exact format, except with the fields filled in:
```
[REDDIT]
reddit_username = ******
reddit_password = ******

[IMGUR]
imgur_client_id = ******
imgur_client_secret = ******
imgur_access_token = ******
imgur_refresh_token = ******
```
Fill it in with the details of the reddit/imgur accounts that you want to do the posting/image hosting. For more information on how to get imgur credentials, refer to the [Imgur API Documentation](https://api.imgur.com/).

Finally, make a file called `completed.json`. This file basically stores all the posts your bot has ever _converted_ to prevent duplicates. If this is the first time making the file, simply fill it with an empty json array:

`{}`

These record files are swappable between instances of the bot, so you can transfer them. If you want to move your bot from one location to another, make sure to store `credentials.ini` and `completed.json` with you in a flash drive so you can put them back in when you start again.
