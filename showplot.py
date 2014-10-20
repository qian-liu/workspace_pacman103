import numpy, pylab, random, sys
from retinaFunc import *    
filename = 'results/input.spikes'
pylab.figure()
spikes = load_recordedFile(filename)
pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], ".") 
pylab.xlabel('Time/ms')
pylab.ylabel('spikes')
pylab.title('recorded data')

pylab.show()
