import numpy, pylab, random, sys
from retinaFunc import *    

pylab.figure()
for j in range (13):
    filename = 'results/32/integrate_%d.spikes' %(j+1)
    spikes = load_recordedFile(filename)
    pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], "b.") 
pylab.xlabel('Time/ms')
pylab.ylabel('Neuron ID')
pylab.title('Recorded Retina Spikes')

title = []
title.append('Gesture: Fist')
title.append('Gesture: Index Finger')
title.append('Gesture: Victory Sign')
title.append('Gesture: Hand')
title.append('Gesture: Thumb Up')
for j in range(5):
    pylab.figure()
    filename = 'results/321/recog_%d.spikes' %(j)
    spikes = load_recordedFile(filename)
    pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], "b.") 
    filename = 'results/322/recog_%d.spikes' %(j)
    spikes = load_recordedFile(filename)
    pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], "b.") 
    pylab.xlabel('Time/ms')
    pylab.ylabel('Neuron ID')
    #pylab.title('recognition_%d' %(j))
    pylab.title(title[j])

pylab.show()

