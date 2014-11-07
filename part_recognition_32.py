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
runtime = 5000 # just for gesture single
num_per_core = 256

#INIT pacman103
p.setup(timestep=1.0, min_delay = 1.0, max_delay = 32.0)
p.set_number_of_neurons_per_core('IF_curr_exp', num_per_core)      # this will set one population per core

#external stuff: population requiremenets
connected_chip_coords = {'x': 0, 'y': 0}
virtual_chip_coords = {'x': 0, 'y': 5}
link = 4

integrate_size = 28
#spikeTrains, source_Num = load_inputSpikes3('recorded_data_for_spinnaker/integrate_32_all.mat', 'integrate', integrate_size)
spikeTrains, source_Num = load_inputSpikes4('recorded_data_for_spinnaker/integrate_32_all.mat', 'integrate', integrate_size, runtime)
print 'source_Num: ', source_Num
'''
integrate_pop = []
print "source_Num:", source_Num
for i in range(source_Num):
#for i in range(1):
    pop = p.Population(integrate_size * integrate_size, p.SpikeSourceArray, {'spike_times': spikeTrains[i] }, label='retina_pop')
    integrate_pop.append( pop )
'''

#-------------------4th Layer on SpiNNaker-----------------------------------
# pool_integrate 36 * 36 (pooling_out_size) --> recogntion_pops 16 * 16

#Define network paras

num_templates = 5
templates_names = ['fist', 'one', 'two', 'hand', 'thumb']
templates_file = 'template_32.mat'
#template_scale = 0.2
template_scale = [0.18, 0.2, 0.4, 0.18, 0.11] * 3
recognition_pops = []
recognition_size = 14
cell_recognition = { 'tau_m' : 20, 'v_init'  : -75, 'i_offset'  : 0,
    'v_rest'    : -75,  'v_reset'    : -75, 'v_thresh'   : -60,
    'tau_syn_E' : 5,   'tau_syn_I'  : 10,  'tau_refrac' : 1}

for iTemplate in range (0, num_templates):
    #template = load_template(iTemplate, templates_names, templates_file ) # lading tempaltes
    #template_weight = [[template_scale * x for x in y] for y in template] # play with weight_scale to move from ANN simulation to Spiking Neural Networks
    #exci_list, inhi_list, recognition_size = convConnector2(integrate_size, template_weight, 1, 1) #generate the weights for the template convolution
    recognition_pops.append ( p.Population (recognition_size * recognition_size,         # size
                       p.IF_curr_exp,   # Neuron Type
                       cell_recognition,   # Neuron Parameters
                       label="recognition_%d" % ( iTemplate) )  ) # Label

source_count = 7;                       
pool_integrate = p.Population(integrate_size * integrate_size, p.SpikeSourceArray, {'spike_times': spikeTrains[source_count] }, label='pool_integrate')

for iTemplate in range (0, num_templates):
    template = load_template(iTemplate, templates_names, templates_file ) # lading tempaltes
    #template_weight = [[template_scale * x for x in y] for y in template] # play with weight_scale to move from ANN simulation to Spiking Neural Networks
    template_weight = [[template_scale[iTemplate] * x for x in y] for y in template] # play with weight_scale to move from ANN simulation to Spiking Neural Networks
    exci_list, inhi_list, recognition_size = convConnector2(integrate_size, template_weight, 1, 1) #generate the weights for the template convolution
    for i in range(0, len(exci_list)):
        p.Projection(pool_integrate, recognition_pops[iTemplate], p.FromListConnector(exci_list[i]), target='excitatory')
                
    for i in range(0, len(inhi_list)):
        p.Projection(pool_integrate, recognition_pops[iTemplate], p.FromListConnector(inhi_list[i]), target='inhibitory')
    recognition_pops[iTemplate].record()
    
print "recognition_size:", recognition_size

pool_integrate.record()
print 'Simulation started... on: {}\n'.format(dt.datetime.now())
p.run(runtime)

# write spikes out to files
filename = 'results/2_32_%2d/integrate.spikes' %(source_count+1)
pool_integrate.printSpikes(filename)
for iTemplate in range (0, num_templates):
    filename = 'results/2_32_%2d/recog_%d.spikes' %(source_count+1, iTemplate)
    recognition_pops[iTemplate].printSpikes(filename)

p.end()
print 'Simulation end! on : {}\n'.format(dt.datetime.now())
