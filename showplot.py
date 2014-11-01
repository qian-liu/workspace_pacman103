import numpy, pylab, random, sys
from retinaFunc import *    
filename = 'results/integrate.spikes'
pylab.figure()
spikes = load_recordedFile(filename)
pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], ".") 
pylab.xlabel('Time/ms')
pylab.ylabel('spikes')
pylab.title('recorded data')

for j in range(5):
    pylab.figure()
    filename = 'results/recog_%d.spikes' %(j)
    spikes = load_recordedFile(filename)
    pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], ".") 
    pylab.xlabel('Time/ms')
    pylab.ylabel('spikes')
    pylab.title('recognition_%d' %(j))
pylab.show()
