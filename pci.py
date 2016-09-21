# Implements the PCI algorithm from
#
# Casali, Adenauer G, Olivia Gosseries, Mario Rosanova, Mélanie Boly, Simone Sarasso, Karina R Casali, Silvia Casarotto, et al. “A Theoretically Based Index of Consciousness Independent of Sensory Processing and Behavior.” Science Translational Medicine 5, no. 198 (August 2013): 198ra105-198ra105. doi:10.1126/scitranslmed.3006294.
#
# Leonardo Barbosa
# leonardo.barbosa@usp.br
# 21/09/2016
#

import numpy as np

def rolling_window(a, size):
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a. strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def pci(L):
    l1 = L.shape[0]-1

    if len(L.shape) > 1:
        if len(L.shape) > 2:
            raise Exception('data has to be 1D or 2D')
        l2 = L.shape[1]-1
    else:
        L = L.reshape([len(L), 1])
        l2 = 0

    c=1
    r=0
    q=0
    k=1
    i=0

    stop = False

    n_iterations = 0
    while not stop:

        if q == r:
            a = i+k-1
        else:
            a=l1

#        n_iterations += 1
#        print "Iteration #%d: (c=%d, r=%d, q=%d ,k=%d ,i=%d ,a=%d)" % (n_iterations, c, r, q, k, i, a)


        d = L[i:i+k,r]
        e = L[0:a,q]
        found = np.all(rolling_window(e, len(d)) == d, axis=1)

        if found.any():

            k += 1
            if i+k > l1:
                r += 1
                if r > l2:
                    c += 1
                    stop = True
                else:
                    i = 0
                    q = r - 1
                    k = 1
        else:

            q -= 1
            if q > 0:

                c += 1
                i = i + k
                if i + 1 > l1:

                    r += 1
                    if r > l2:
                        c += 1
                        stop = True
                    else:
                        i = 0
                        q = r - 1
                        k = 1
                else:

                    q = r
                    k = 1

    return c

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


def main():
    lz = lz_complexity('1001111011000010')
    assert lz == 6
    print lz



#data = (1 * (np.random.rand(100,100) > .5)).astype('str')
data = 1 * (np.random.rand(30,30) > .5)

data_c = pci(data)
print "Complexity of data : %d" % data_c

# Compare to the 1D implementation

data_1d = data.flatten()

data_1d_c = pci(data_1d)
print "Complexity of 1D data : %d" % data_1d_c

data_1d_c2 = lz_complexity(data_1d)
print "Complexity 2 of 1D data : %d" % data_1d_c2

