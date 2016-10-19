
import pci
import pickle
import time
import numpy as np

# BEWARE: this takes ~17 min in a Intel Xeon CPU E5-2630 v3 @ 2.40GHz

print("Start: " + time.strftime("%c"))

# test 1D algorithm
lz = pci.lz_complexity('1001111011000010')
print '1D found: %d, should be %d' % (lz, 6)
assert lz == 6

# test 2D algorithm
with open('./lz_2D_example.pickle', 'r') as f:
    known_pci = pickle.load(f)

lz_columnwise = pci.lz_complexity_2D(known_pci['data'])
print '2D LZ columnwise found: %d, should be %d' % (lz_columnwise, known_pci['lz_columnwise'])
assert lz_columnwise == known_pci['lz_columnwise']

PCI_columnwise = lz_columnwise / pci.pci_norm_factor(known_pci['data'])
print 'PCI columnwise found: %f, should be %f' % (PCI_columnwise, known_pci['pci_columnwise'])
assert np.int(100000*PCI_columnwise) == np.int(100000*known_pci['pci_columnwise'])

#lz_linewise = pci.lz_complexity_2D(known_pci['data'].T)
#print '2D linewise found: %d, should be %d' % (lz_linewise, known_pci['lz_linewise'])
#assert lz_linewise == known_pci['lz_linewise']

#x = np.array([[0,0,1],[1,0,1],[1,0,1]])
#lz_2D = pci.lz_complexity_2D(x)
#print '2D linewise found: %d, should be %d' % (lz_2D, 5)

print("End: " + time.strftime("%c"))

