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
runtime = 70000
num_per_core = 256

#INIT pacman103
p.setup(timestep=1.0, min_delay = 1.0, max_delay = 32.0)
p.set_number_of_neurons_per_core('IF_curr_exp', num_per_core)      # this will set one population per core

#external stuff: population requiremenets
connected_chip_coords = {'x': 0, 'y': 0}
virtual_chip_coords = {'x': 0, 'y': 5}
link = 4

# ------------------1st Layer on SpiNNaker-----------------------------------
# Retina 128 * 128 --> Input 128 * 128

#Define network paras
retina_size = 128 # retina from the FPGA
input_size = 128 # Fisrt layer on SpiNNaker to combine both ON and OFF inputs
input_weights = 6
cell_input = { 'tau_m' : 20, 'v_init'  : -65, 'i_offset'  : 0,
    'v_rest'    : -65,  'v_reset'    : -65, 'v_thresh'   : -50,
    'tau_syn_E' : 5,   'tau_syn_I'  : 5,  'tau_refrac' : 1}

input_pop = p.Population(input_size * input_size,         # size
                       p.IF_curr_exp,   # Neuron Type
                       cell_input,   # Neuron Parameters
                       label="Input") # Label

#-------------------2nd Layer on SpiNNaker-----------------------------------
# Input 128 * 128 --> convoled (Gabor Filters) 112 * 112 

#Define network paras
gabor_size = 17
gabor_scale = 3
gabor_freq = 1
num_orient = 4
weight_scale = 2
convolved_pops = []

cell_convolve = { 'tau_m' : 20, 'v_init'  : -75, 'i_offset'  : 0,
    'v_rest'    : -75,  'v_reset'    : -75, 'v_thresh'   : -50,
    'tau_syn_E' : 9,   'tau_syn_I'  : 15,  'tau_refrac' : 1}

for iOrient in range (0, num_orient):
        
    gabor_orient = iOrient / float(num_orient) * pi
    gabor_weight = gaborFilter(gabor_size, gabor_orient, gabor_scale, gabor_freq) # generate a gabor filter with given parameters
    gabor_weight = [[weight_scale * x for x in y] for y in gabor_weight] # play with weight_scale to move from ANN simulation to Spiking Neural Networks
    exci_list, inhi_list, convolved_size = convConnector2(input_size, gabor_weight, 1, 1)  #split the connections into exci and inhi connections
    convolved_pops.append ( p.Population (convolved_size * convolved_size,      # Neuron Size
                       p.IF_curr_exp,   # Neuron Type
                       cell_input,
                       #cell_convolve,   # Neuron Parameters
                       label="Convolutoin_%d" % (iOrient)) ) # Label

    for i in range(0, len(exci_list)):
        p.Projection(input_pop, convolved_pops[iOrient], p.FromListConnector(exci_list[i]), target='excitatory')
                
    for i in range(0, len(inhi_list)):
        p.Projection(input_pop, convolved_pops[iOrient], p.FromListConnector(inhi_list[i]), target='inhibitory')

print "convolved_size:", convolved_size
#-------------------3rd Layer Pooling -----------------------------------
# convoled 112 * 112 --> pooling 36 * 36
# pooling 36 * 36 --> pool_integrate 36 * 36

pool_size = 5
pool_shift = 3
weights_pool = 4.5
#weights_pool = 5.75
conn_pool, pooling_out_size = pooling(convolved_size, pool_size, pool_shift, weights_pool, 1) # generate connection weights for pooling.
pooling_pops = []
print "pooling out size:", pooling_out_size
pool_integrate = p.Population(pooling_out_size * pooling_out_size,         # size
                               p.IF_curr_exp,   # Neuron Type
                               cell_input,
                               #cell_convolve,   # Neuron Parameters
                               label="pool_integrate") 
                               
for iOrient in range (0, num_orient):
    
    pooling_pops.append( p.Population(pooling_out_size * pooling_out_size,         # size
                               p.IF_curr_exp,   # Neuron Type
                               cell_input,
                               #cell_convolve,   # Neuron Parameters
                               label="pool_%d" % (iOrient))  )# Label
    p.Projection(convolved_pops[iOrient], pooling_pops[iOrient], p.FromListConnector(conn_pool), target='excitatory')
    p.Projection(pooling_pops[iOrient], pool_integrate, p.OneToOneConnector(weights = weights_pool, delays = 1), target='excitatory')
# -----------------First thing last, the spike source array since it changes according to the spike trains-----------

spikeTrains, source_Num = load_inputSpikes2('recorded_data_for_spinnaker/all.mat', 'retinaPop', retina_size)
retina_pop = []
print "source_Num:", source_Num
for i in range(source_Num):
#for i in range(1):
    pop = p.Population(retina_size * retina_size, p.SpikeSourceArray, {'spike_times': spikeTrains[i] }, label='retina_pop')
    retina_pop.append( pop )
    p.Projection(retina_pop[i], input_pop, p.OneToOneConnector(weights=input_weights, delays=1), label='input projection')

#input_pop.record()
#convolved_pops[0].record()
pool_integrate.record()
#retina_pop[0].record()
print 'Simulation started... on: {}\n'.format(dt.datetime.now())
p.run(runtime)

# write spikes out to files
#filename = 'results/input_all.spikes'
#input_pop.printSpikes(filename)
#filename = 'results/conv_all_0.spikes'
#convolved_pops[0].printSpikes(filename)
filename = 'results/integrate_all.spikes'
pool_integrate.printSpikes(filename)

p.end()
print 'Simulation end! on : {}\n'.format(dt.datetime.now())

