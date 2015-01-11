import subprocess
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster

p = subprocess.Popen(["REG", "QUERY", "HKCU\Software\Microsoft\Internet Explorer\Desktop\General", "/v", "WallpaperSource"], stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()

p_status = p.wait()
path = output.split()[-1]
#print "Command exit status/return code : ", p_status

NUM_CLUSTERS = 5

print 'reading image'
im = Image.open(path)
im = im.resize((400, 400))      # optional, to reduce time
ar = scipy.misc.fromimage(im)
shape = ar.shape
ar = ar.reshape(scipy.product(shape[:2]), shape[2])

print 'finding clusters'
codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
print 'cluster centres:\n', codes

vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

index_max = scipy.argmax(counts)                    # find most frequent
peak = codes[index_max]
colour = ''.join(chr(c) for c in peak).encode('hex')
print 'most frequent is %s (#%s)' % (peak, colour)