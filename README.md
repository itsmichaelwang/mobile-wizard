##Mobile-Wizard
`mobile-wizard` is a Reddit bot that is trigged when someone types the phrase "rip mobile users", translating the comment above that comment into an image, hosting it on imgur, and posting it as a response.

`data.txt` and `data.png` are provided as example inputs and outputs, respectively.

###Installation Instructions
First, go ahead and clone the `mobile-wizard` repo into whatever directory you prefer. Then, make sure you have [installed pip](http://pip.readthedocs.org/en/latest/installing.html). Then, install the prerequisite packages using the included `requirements.txt` by typing:

`pip install -r requirements.txt`

Make sure to do this as root if you are on linux, otherwise it may not work. Also, Pillow can sometimes be a pain to install. If you can't get it to install on Windows 7, try the [precompiled packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/). For Linux (more specifically Debian), try the solution described in this [StackExchange post](http://unix.stackexchange.com/questions/105265/install-pil-pillow-via-pip-in-debian-testing-jessie).
