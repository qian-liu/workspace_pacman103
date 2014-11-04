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
link = 6

integrate_size = 36
cell_input = { 'tau_m' : 20, 'v_init'  : -65, 'i_offset'  : 0,
    'v_rest'    : -65,  'v_reset'    : -65, 'v_thresh'   : -50,
    'tau_syn_E' : 5,   'tau_syn_I'  : 5,  'tau_refrac' : 1}
input_weights = 4
    
integrate = p.Population(integrate_size * integrate_size,
                        p.IF_curr_exp,   # Neuron Type
                       cell_input,   # Neuron Parameters
                       label="Integrate") # Label

spikeTrains, source_Num = load_inputSpikes2('recorded_data_for_spinnaker/integrate_all.mat', 'integrate', integrate_size)
integrate_pop = []
print "source_Num:", source_Num
for i in range(source_Num):
#for i in range(1):
    pop = p.Population(integrate_size * integrate_size, p.SpikeSourceArray, {'spike_times': spikeTrains[i] }, label='integrate_pop')
    integrate_pop.append( pop )
    p.Projection(integrate_pop[i], integrate, p.OneToOneConnector(weights=input_weights, delays=1), label='input projection')

integrate.record()
#retina_pop[0].record()
print 'Simulation started... on: {}\n'.format(dt.datetime.now())
p.run(runtime)

# write spikes out to files
#filename = 'results/input_0.spikes'
#input_pop.printSpikes(filename)


p.end()
print 'Simulation end! on : {}\n'.format(dt.datetime.now())
