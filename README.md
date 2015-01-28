##Mobile-Wizard
`mobile-wizard` is a Reddit bot that is trigged when someone types the phrase "rip mobile users", and translates that comment's parent comment into an image, before hosting it on imgur and posting it as a response.

###Installation
Clone the `mobile-wizard` repo into whatever directory you prefer. Then, make sure you have [installed pip](http://pip.readthedocs.org/en/latest/installing.html) and install the prerequisite packages using the included `requirements.txt` by typing:

`pip install -r requirements.txt`

Make sure to do this as root if you are on Linux, otherwise it may not work. Also, Pillow can sometimes be a pain to install. If you can't get it to install on Windows 7, try the [precompiled packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/). For Linux (more specifically Debian), try the solution described in this [StackExchange post](http://unix.stackexchange.com/questions/105265/install-pil-pillow-via-pip-in-debian-testing-jessie).

Next, make a credentials file called `credentials.ini`. It should have this exact format, except with the fields filled in:
```
[REDDIT]
reddit_username =
reddit_password =

[IMGUR]
imgur_client_id =
imgur_client_secret =
imgur_access_token =
imgur_refresh_token =
```

Fill it in with the details of the reddit/imgur accounts that you want to do the posting/image hosting. For more information on how to get imgur credentials, refer to the [Imgur API Documentation](https://api.imgur.com/).

Finally, make a file called `completed.json`. This file basically stores all the posts your bot has ever _converted_ to prevent duplicates. If this is the first time making the file, simply fill it with an empty json array:

`{}`

Hoepfully, future versions of this bot will not require this pre-setup.

The record files are swappable between all instances of the bot, so you can transfer them. If you want to move your bot from one location to another, make sure to take `credentials.ini` and `completed.json` with you.

###Running
To run the bot, simply navigate to the repo location, and type:

`python mobile-wizard.py`

###Anti-Spam
The bot has a couple of anti-spam measures, which will probably be largely ineffective to anyone who really wants to abuse the bot ;):
* The bot keeps track of which comments it has converted into images, and will not duplicate this.
* The bot keeps track of how many times it has posted in a thread, and will not post more than 3 times, no matter what.
* The bot will not convert comments that are 3 lines in length or shorter.
* The bot will not convert its own comments.
* The bot's posts are frequently monitored.

###To-Do List
* ~~Make bot able to decode HTML entities~~ - DONE
* ~~Make bot convert Reddit's double newlines to single newlines.~~ - DONE
* Make bot easier to set up on a computer (ideally should just have to clone repository)
* Add feature to delete comments that have less than 0 karma
* A blacklist
