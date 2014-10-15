#!/usr/bin/python
"""
Author: Qian Liu, SpiNNaker Group, The University of Manchester
This program provides a gesture recognition colvolutional neural network. 

This test requires:
 - an FPGA/robot MC translating the AER sensor events to MC packets (see the application note by Luis Plana at http://solem.cs.man.ac.uk/documentation/spinn-app-8.pdf)
 - the visualiser in tools/visualiser

"""


import pyNN.spiNNaker as p
import numpy, pylab, random, sys
import time
import datetime as dt
from math import *
# import defined retina Functions from another python file
from retinaFunc import *


#Define Simulation Paras
runtime = 32000
num_per_core = 256

#INIT pacman103
p.setup(timestep=1.0, min_delay = 1.0, max_delay = 32.0)
p.set_number_of_neurons_per_core('IF_curr_exp', num_per_core)      # this will set one population per core

retina_size = 128
input_size = 128 # Fisrt layer on SpiNNaker to combine both ON and OFF inputs
input_weights = 5.75
cell_input = { 'tau_m' : 64, 'v_init'  : -95, 'i_offset'  : 0,
    'v_rest'    : -95,  'v_reset'    : -95, 'v_thresh'   : -40,
    'tau_syn_E' : 15,   'tau_syn_I'  : 15,  'tau_refrac' : 1}


input_pop = p.Population(input_size * input_size,         # size
                       p.IF_curr_exp,   # Neuron Type
                       cell_input,   # Neuron Parameters
                       label="Input") # Label

  
spikeTrains = [ [] for i in range(retina_size * retina_size) ]
for i in range(retina_size * retina_size):
    spikeTrains[i].append( i * 2 )

sourcePop = p.Population(retina_size * retina_size, p.SpikeSourceArray, {'spike_times': spikeTrains }, label='retina_pop')
p.Projection(sourcePop, input_pop, p.OneToOneConnector(weights=input_weights, delays=1), label='input projection')
'''
pop_num = 2
spikeTrains =[ [ [] for i in range(retina_size * retina_size) ]  for j in range (pop_num)]
for i in range(retina_size * retina_size):
    index_i = i / (retina_size * retina_size / pop_num)
    spikeTrains[index_i][i].append( i * 2 )

sourcePop = []    
for i in range(pop_num):
    sourcePop.append( p.Population(retina_size * retina_size, p.SpikeSourceArray, {'spike_times': spikeTrains[i] }, label='retina_pop') )
    p.Projection(sourcePop[i], input_pop, p.OneToOneConnector(weights=input_weights, delays=1), label='input projection')
'''
input_pop.record()
p.run(runtime)
#filename = 'results/test.spikes'
#input_pop.printSpikes(filename)

'''
spikes = input_pop.getSpikes()
if spikes != None:
    print spikes
    pylab.figure()
    pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], ".") 
    pylab.xlabel('Time/ms')
    pylab.ylabel('spikes')
    pylab.title('recorded data')
     
else:
    print "No spikes received"

pylab.show()


pylab.figure()
spikes = load_recordedFile(filename)
pylab.plot([i[0] for i in spikes], [i[1] for i in spikes], ".") 
pylab.xlabel('Time/ms')
pylab.ylabel('spikes')
pylab.title('recorded data')
'''



p.end()

