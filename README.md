# Neo-Desktop
A python based windows service script that finds the location of the current background, figures out the most dominant color in it, then sets a Neo Pixel strip connected by a fadecandy to that color.

Acknowledgements:

The base for the dominant color code comes from here https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image

The registry query comes from here
http://superuser.com/questions/244924/how-could-i-find-out-the-path-to-the-current-desktop-image

The service setup for python comes from here
http://stackoverflow.com/questions/32404/is-it-possible-to-run-a-python-script-as-a-service-in-windows-if-possible-how
