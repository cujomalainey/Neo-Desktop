from os import listdir
from os.path import isfile, join
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import time
import serial
import sys
import glob
import io
import binascii
import os
import string

system_path = os.getenv('APPDATA') + "/Microsoft/Windows/Themes/"
displayMap = {0:0, 1:1, 2:2}

class background():
    path = ""
    displayNumber = -1
    mtime = 0

    def __init__(self, path):
        self.displayNumber = int(path.split("_")[1])
        self.path = system_path + path

    def changed(self):
        try:
            t = os.stat(self.path)
            if t != self.mtime:
                self.mtime = t
                return True
        except IOError:
            pass
        return False

    def getDominant(self):
        NUM_CLUSTERS = 5

        print 'reading image', self.path
        try:
            im = Image.open(self.path)
        except IOError:
            self.mtime = None
            return
        
        im = im.resize((300, 300))      # optional, to reduce time
        ar = scipy.misc.fromimage(im)
        shape = ar.shape
        ar = ar.reshape(scipy.product(shape[:2]), shape[2])
        print 'finding clusters'
        codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

        index_max = scipy.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        print 'most frequent is %s' % peak
        print 'on display ' + str(self.displayNumber)
        return peak


def serial_ports():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

onlyfiles = [ f for f in listdir(system_path) if isfile(join(system_path,f)) ]
print onlyfiles
backgrounds = []
for f in onlyfiles:
    if string.find(f, "_") != -1:
        backgrounds.append(background(f))

serials = serial_ports()
print "Finding Serial Port"
serial_arduino = None
for ser in serials:
    print "trying: " + ser
    s = serial.Serial(ser)
    s.write("T\n")
    print "sending test command"
    time.sleep(0.5)
    print "reading response"
    test = s.readline()
    if test == "GREEN!\n":
        serial_arduino = s

if serial_arduino == None:
    print "Unable to find serial port"
    exit()

print "entering main loop"
while True:
    time.sleep(0.1)
    for b in backgrounds:
        if b.changed() and b.mtime is not None:
            msg = str(tuple(b.getDominant()))[0:-1] + ", " + str(displayMap[b.displayNumber]) + ")\n"
            print "Sending: " + msg
            serial_arduino.write(msg)
