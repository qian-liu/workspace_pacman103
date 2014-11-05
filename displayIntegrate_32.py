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
runtime = 70000 # just for gesture single
num_per_core = 256

#INIT pacman103
p.setup(timestep=1.0, min_delay = 1.0, max_delay = 32.0)
p.set_number_of_neurons_per_core('IF_curr_exp', num_per_core)      # this will set one population per core

#external stuff: population requiremenets
connected_chip_coords = {'x': 0, 'y': 0}
virtual_chip_coords = {'x': 0, 'y': 5}
link = 4

integrate_size = 28
spikeTrains, source_Num = load_inputSpikes('recorded_data_for_spinnaker/integrate_1.mat', 'integrate', integrate_size)
integrate_pop = []
print "source_Num:", source_Num
#for i in range(source_Num):
for i in range(1):
    pop = p.Population(integrate_size * integrate_size, p.SpikeSourceArray, {'spike_times': spikeTrains[i] }, label='retina_pop')
    integrate_pop.append( pop )

integrate_pop[0].record()
#retina_pop[0].record()
print 'Simulation started... on: {}\n'.format(dt.datetime.now())
p.run(runtime)

# write spikes out to files
#filename = 'results/input_0.spikes'
#input_pop.printSpikes(filename)


p.end()
print 'Simulation end! on : {}\n'.format(dt.datetime.now())
