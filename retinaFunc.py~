from math import *
import scipy.io

# DEFINE MOTHEDS
def subSamplerConnector2D(size_in, size_out, weights, delays):
    """
    size_in = size of the input population (2D = size_in x size_in)    
    size_out = size of the sampled population
    weights = averaging weight value (each connection will have this value) must be float
    delays = averaging delay value (each connection will have this value)
    """
    out = []
    step = size_in/size_out
    for i in range(size_in):
         for j in range(size_in):
            i_out = i/step
            j_out = j/step
            out.append((i*size_in + j, i_out*size_out + j_out, weights, delays))
    return out
    
def gaborFilter(gabor_size, orientation, scale, frequency):
    """
    gabor_size = size of the kernel
    orientaion = preferred direction of the kernel
    scale = the scale of gabor filter
    frequency = the frequency of the Gaussian wave
    output is the weight matrix
    """
    gabor_half = gabor_size/2
    w = [[0 for i in range(gabor_size)] for i in range(gabor_size)]
    
    for kx in range(-1 * gabor_half - 1, gabor_half):
        for ky in range(-1 * gabor_half - 1, gabor_half):
            x1=kx*cos(orientation)+ky*sin(orientation)
            y1=-1*kx*sin(orientation)+ky*cos(orientation)
            realPart= exp(-1*(x1*x1+y1*y1)/(2*scale*scale))*cos(x1*frequency)
            w[kx+gabor_half+1][ky+gabor_half+1]=realPart
    '''        
    for i in range(0, len(w)):         # convolutional kernel is flipud and fliplr
        w[i].reverse()
    w.reverse()
    '''
    return w

def convConnector(input_size, kernel, delays, shift):
    """
    size = size of input and the convolutional layer   
    kernel = weight matrix of the convolution kernel
    delays = averaging delay value (each connection will have this value)
    """
    exci_list = []
    inhi_list = []
    kernel_size = len(kernel);
    kernel_half = kernel_size/2
    valid_size = input_size - 2 * kernel_half
    for cx in range(0, valid_size, shift):     # cx and cy are the index of width and length of convolutional layer      
        for cy in range(0, valid_size, shift):
            conv_index = cx * valid_size + cy
            for kx in range(0, kernel_size):
                for ky in range(0, kernel_size):
                    ix = cx + kx
                    iy = cy + ky
                    input_index = ix * input_size + iy
                    weight = kernel[ky][kx]
                    if weight >= 0:
                        exci_list.append((input_index, conv_index, weight, delays))
                    else:
                        inhi_list.append((input_index, conv_index, weight, delays))
    return exci_list, inhi_list, valid_size


def convConnector2(input_size, kernel, delays, shift):
    """
    size = size of input and the convolutional layer   
    kernel = weight     matrix of the convolution kernel
    delays = averaging delay value (each connection will have this value)
    """
    exci_list = []
    inhi_list = []
    kernel_size = len(kernel);
    kernel_half = kernel_size/2
    valid_size = input_size - 2 * kernel_half
    print valid_size
    for cx in range(0, valid_size, shift):     # cx and cy are the index of width and length of convolutional layer
        exci = []
        inhi = []        
        for cy in range(0, valid_size, shift):
            conv_index = cx * valid_size + cy
            for kx in range(0, kernel_size):
                for ky in range(0, kernel_size):
                    ix = cx + kx
                    iy = cy + ky
                    input_index = ix * input_size + iy
                    weight = kernel[ky][kx]
                    if weight >= 0:
                        exci.append((input_index, conv_index, weight, delays))
                    else:
                        inhi.append((input_index, conv_index, weight, delays))
        exci_list.append(exci)
        inhi_list.append(inhi)
    return exci_list, inhi_list, valid_size
    
def pooling(input_size, pool_size, shift, weights, delays):
    """
    input_size = size of the input
    pool_size = size of the pool
    shift = shift between the pooling region
    """
    conn = []
    output_size = (input_size - pool_size)/shift + 1
    weights = weights/(pool_size * pool_size)
    for ox in range(0, output_size):
        for oy in range(0, output_size):
            output_index = ox * output_size + oy
            for px in range(0, pool_size):
                for py in range(0, pool_size):
                    input_index = (ox * shift + px) * input_size + oy * shift + py
                    conn.append((input_index, output_index, weights, delays))
    return conn, output_size
    

    
def load_template(iTemplate, templates_names, templates_file):
    mat = scipy.io.loadmat(templates_file)
    template = mat[ templates_names[iTemplate] ].tolist()
    # flip up-down is the correct image
    #template = [[ i if i > 0 else 2 * i for i in j] for j in template]

    template.reverse()
    return template
    
    
def load_inputSpikes(file_name, input_name, retina_size):
    mat = scipy.io.loadmat(file_name)
    spike = mat[input_name]
    spike_len = len(spike)
    #source_len = 10000  #10ms
    source_len = spike[spike_len - 1][0] + 1
    source_Num = spike[spike_len - 1][0]/source_len + 1
    spikeTrains = [ [[] for i in range(retina_size * retina_size)] for j in range(source_Num) ]

    for i in range( spike_len ):
        index = spike[i][1]
        source_id = spike[i][0]/source_len
        spikeTrains[source_id][index].append( float(spike[i][0] ) )
    return spikeTrains, source_Num

def load_inputSpikes2(file_name, input_name, retina_size):
    mat = scipy.io.loadmat(file_name)
    spike = mat[input_name]
    spike_len = len(spike)
    source_len = 10000  #10ms
    #source_len = spike[spike_len - 1][0] + 1
    source_Num = spike[spike_len - 1][0]/source_len + 1
    spikeTrains = [ [[] for i in range(retina_size * retina_size)] for j in range(source_Num) ]

    for i in range( spike_len ):
        index = spike[i][1]
        source_id = spike[i][0]/source_len
        spikeTrains[source_id][index].append( float(spike[i][0] ) )
    return spikeTrains, source_Num

def load_inputSpikes3(file_name, input_name, retina_size):
    mat = scipy.io.loadmat(file_name)
    spike = mat[input_name]
    spike_len = len(spike)
    source_len = 10000  #10ms
    #source_len = spike[spike_len - 1][0] + 1
    source_Num = spike[spike_len - 1][0]/source_len + 1
    spikeTrains = [ [[] for i in range(retina_size * retina_size)] for j in range(source_Num) ]

    for i in range( spike_len ):
        index = spike[i][1]
        source_id = spike[i][0]/source_len
        spikeTrains[source_id][index].append( float(spike[i][0] % source_len ) )
    return spikeTrains, source_Num

def load_recordedFile( filename ):
    with open(filename) as f:
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        array = [[int(x) for x in line.split()] for line in f]
    return array






