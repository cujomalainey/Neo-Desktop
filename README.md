# Neo-Desktop
A python based windows service script that finds the location of the current background, figures out the most dominant color in it, then sets a Neo Pixel strip connected by a fadecandy to that color.

Acknowledgements:

The base for the dominant color code comes from here https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image

The background file knowledge comes from here
http://superuser.com/questions/966650/path-to-desktop-backgrounds-in-windows-10

The service setup for python comes from here
http://stackoverflow.com/questions/32404/is-it-possible-to-run-a-python-script-as-a-service-in-windows-if-possible-how

The python serial discovery code comes from here
http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

The adafruit neopixel library comes from https://github.com/adafruit/Adafruit_NeoPixel
