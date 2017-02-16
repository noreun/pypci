# coding=utf-8
#  Implements the PCI algorithm from
#
#Casali, Adenauer G, Olivia Gosseries, Mario Rosanova, Mélanie Boly, Simone Sarasso, Karina R Casali, Silvia Casarotto, et al. “A Theoretically Based Index of Consciousness Independent of Sensory Processing and Behavior.” Science Translational Medicine 5, no. 198 (August 2013): 198ra105-198ra105. doi:10.1126/scitranslmed.3006294.
#
# Leonardo Barbosa
# leonardo.barbosa@usp.br
#
# 21/09/2016 : First version with rolling window
# 19/10/2016 : Fixed bug due to indexing problem
#              Implemented normalization
# 20/10/2016 : Implemented search with bitarray (3x faster)
# 15/2/2016:    added the "calculate_pci_lower" function to compute the lower bound of the time-dependent PCI (Thierry Nieus thierry.nieus@unimi.it, University of Milan, Dipartimento di Scienze Biomediche e Cliniche L.Sacco)


import numpy as np
from bitarray import bitarray

def calculate_pci_lower(D):
    '''
        Computes a lower bound of the PCI for the binary matrix D. 
        
        The PCI is computed on the ordered matrix D (i.e. the channels are ranked based on the evoked activity).  
        A speed up in the calculation is achieved removing the zero-rows (see Casali's MATLAB code).
    '''
    global ct 
    Irank=np.sum(D,axis=1).argsort()
    S=D[Irank,:].sum(axis=1)
    Izero=np.where(S==0)[0]
    number0removed=D.shape[1]*len(Izero)
    Dnew=D[Irank,:][Izero[-1]+1:,:]
    a=lz_complexity_2D(Dnew)

    nValues=float(D.shape[0]*D.shape[1])
    p1=np.sum(D)/nValues
    p0=1-p1

    N=np.log2(nValues)/nValues
    H=-p1*np.log2(p1)-p0*np.log2(p0)
    PCI=N*np.array(ct)/H
    return PCI

def calculate(D):
    return lz_complexity_2D(D) / pci_norm_factor(D)

def pci_norm_factor(D):

    L = D.shape[0] * D.shape[1]
    p1 = sum(1.0 * (D.flatten() == 1)) / L
    p0 = 1 - p1
    H = -p1 * np.log2(p1) -p0 * np.log2(p0)

    S = (L * H) / np.log2(L)

    return S

def lz_complexity_2D(D):
    global ct   # time dependent complexity 
    if len(D.shape) != 2:
        raise Exception('data has to be 2D!')

    # initialize
    (L1, L2) = D.shape
    c=1; r=1; q=1; k=1; i=1
    stop = False

    # convert each column to a sequence of bits
    bits = [None] * L2
    for y in range(0,L2):
        bits[y] = bitarray(D[:,y].tolist())

    # action to perform every time it reaches the end of the column
    def end_of_column(r, c, i, q, k, stop):
        r += 1
        if r > L2:
            c += 1
            stop = True
        else:
            i = 0
            q = r - 1
            k = 1
        return r, c, i, q, k, stop

    ct=[]

    # main loop
    while not stop:

        if q == r:
            a = i+k-1
        else:
            a=L1

        # binary search
        #d = bits[r-1][i:i+k]
        #e = bits[q-1][0:a]
        #found = not not e.search(d, 1)
        found = not not bits[q-1][0:a].search(bits[r-1][i:i+k], 1)

        ## rowlling window (3x slower)
        #d = D[i:i+k,r-1]
        #e = D[0:a,q-1]
        #found = np.all(_rolling_window(e, len(d)) == d, axis=1).any()

        if found:
            k += 1
            if i+k > L1:
                (r, c, i, q, k, stop) = end_of_column(r, c, i, q, k, stop)
                ct.append(c)     
        else:
            q -= 1
            if q < 1:
                c += 1
                i = i + k
                if i + 1 > L1:
                    (r, c, i, q, k, stop) = end_of_column(r, c, i, q, k, stop)
                    ct.append(c)      
                else:
                    q = r
                    k = 1
    return c
