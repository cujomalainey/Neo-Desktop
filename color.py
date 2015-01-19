import subprocess
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster
import re
import opc
import time

current_path = ""

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
		im = im.resize((400, 400))      # optional, to reduce time
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
		client = opc.Client('localhost:7890')
		client.put_pixels([tuple(peak)]*60)