# coding=utf-8
#  Implements the PCI algorithm from
#
#Casali, Adenauer G, Olivia Gosseries, Mario Rosanova, Mélanie Boly, Simone Sarasso, Karina R Casali, Silvia Casarotto, et al. “A Theoretically Based Index of Consciousness Independent of Sensory Processing and Behavior.” Science Translational Medicine 5, no. 198 (August 2013): 198ra105-198ra105. doi:10.1126/scitranslmed.3006294.
#
# Leonardo Barbosa
# leonardo.barbosa@usp.br
# 21/09/2016
#

import numpy as np

DEBUG = False
#DEBUG = True

def pci(D):

    L = D.shape[0] * D.shape[1]
    p1 = sum(1.0 * (D.flatten() == 1)) / L
    p0 = 1 - p1
    H = -p1 * np.log2(p1) -p0 * np.log2(p0)

    S = (L * H) / np.log2(L)

    return lz_complexity_2D(D) / S

def lz_complexity_2D(D):

    if len(D.shape) != 2:
        raise Exception('data has to be 2D!')

    L1 = D.shape[0]
    L2 = D.shape[1]

    c=1
    r=1
    q=1
    k=1
    i=1

    stop = False

    def end_of_line(r, c, i, q, k, stop):

        # go to the next column
        r += 1

        # end line + end of column? end of the algorithm...
        if r > L2:
            c += 1
            stop = True
        else:
            # reset for next line
            i = 0
            q = r - 1
            k = 1

        return r, c, i, q, k, stop

    n_iterations = 0
    while not stop:

        if q == r:
            a = i+k-1
        else:
            a=L1

        if DEBUG:
            n_iterations += 1
            print "Iteration #%d: (c=%d, r=%d, q=%d ,k=%d ,i=%d ,a=%d)" % (n_iterations, c, r, q, k, i, a)

        d = D[i:i+k,r-1]
        e = D[0:a,q-1]

        found = np.all(rolling_window(e, len(d)) == d, axis=1)

        if found.any():

            k += 1
            if i+k > L1:

                (r, c, i, q, k, stop) = end_of_line(r, c, i, q, k, stop)

        else:

            q -= 1
            if q < 1:

                c += 1
                i = i + k
                if i + 1 > L1:

                    (r, c, i, q, k, stop) = end_of_line(r, c, i, q, k, stop)

                else:
                    q = r
                    k = 1

    return c

def rolling_window(a, size):
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a. strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

# 1D Lempel-Ziv implementation from: http://stackoverflow.com/questions/4946695/calculating-lempel-ziv-lz-complexity-aka-sequence-complexity-of-a-binary-str
# Kaspar, F. Schuster, H. Easily calculable measure for the complexity of spatiotemporal patterns. Physical Review A, vol 36, n. 2, p 842.
def lz_complexity(s):
    i, k, l = 0, 1, 1
    k_max = 1
    n = len(s) - 1
    c = 1
    while True:
        if s[i + k - 1] == s[l + k - 1]:
            k = k + 1
            if l + k >= n - 1:
                c = c + 1
                break
        else:
            if k > k_max:
               k_max = k
            i = i + 1
            if i == l:
                c = c + 1
                l = l + k_max
                if l + 1 > n:
                    break
                else:
                    i = 0
                    k = 1
                    k_max = 1
            else:
                k = 1
    return c


#data = (1 * (np.random.rand(100,100) > .5)).astype('str')
#data = 1 * (np.random.rand(100,100) > .5)
#
#data_c = pci(data)
#print "Complexity of data : %d" % data_c
#
## Compare to the 1D implementation
#
#data_1d = data.flatten()
#
# data_1d_c = pci(data_1d)
# print "Complexity of 1D data : %d" % data_1d_c
#
# data_1d_c2 = lz_complexity(data_1d)
# print "Complexity 2 of 1D data : %d" % data_1d_c2

