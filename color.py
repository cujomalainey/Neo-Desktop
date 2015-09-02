import subprocess
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import re
import time
import serial
import sys
import glob
import io

current_path = ""
serials = serial_ports()
print "Finding Serial Port"
serial_arduino = None
for ser in serials:
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
	sio.write(ascii("T\n"))
	sio.flush()
	time.sleep(0.5)
	test = sio.readline()
	if test == "GREEN!\n":
		serial_arduino = sio

if serial_arduino == None:
	exit()


while True:
	time.sleep(0.1)
	p = subprocess.Popen(["REG", "QUERY", "HKCU\Software\Microsoft\Internet Explorer\Desktop\General", "/v", "WallpaperSource"], stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()
	output = re.search("""([A-Z]:\\\\)([\\w\\d\\.\\s-]+\\\\)+([\\w\\d\\.\\s-]+\\.\\w+)""", output)
	path = output.group(0)

	if current_path != path:
		current_path = path
		NUM_CLUSTERS = 5

		print 'reading image', path
		im = Image.open(path)
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
		
		sio.write(ascii(tuple(peak).__str__() + "\n"))

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