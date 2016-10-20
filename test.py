
import pci
import pickle
import time
import numpy as np

# BEWARE: this takes ~3 min in a Intel Xeon CPU E5-2630 v3 @ 2.40GHz

print("Start: " + time.strftime("%c"))

with open('./lz_2D_example.pickle', 'r') as f:
    known_pci = pickle.load(f)

# columnwise...
t = time.time()
lz_columnwise = pci.lz_complexity_2D(known_pci['data'])
elapsed = time.time() - t
print '2D LZ columnwise found: %d, should be %d (Elapsed time : %.2f s)' % (lz_columnwise, known_pci['lz_columnwise'], elapsed)
assert lz_columnwise == known_pci['lz_columnwise']

# rolling window : 2D LZ columnwise found: 16842, should be 16842 (Elapsed time : 437.64 s)  426.53 s
# bits sequence : 2D LZ columnwise found: 16842, should be 16842 (Elapsed time : 125.72 s)

PCI_columnwise = lz_columnwise / pci.pci_norm_factor(known_pci['data'])
print 'PCI columnwise found: %f, should be %f' % (PCI_columnwise, known_pci['pci_columnwise'])
assert np.int(100000*PCI_columnwise) == np.int(100000*known_pci['pci_columnwise'])

# linewise...
t = time.time()
lz_linewise = pci.lz_complexity_2D(known_pci['data'].T)
elapsed = time.time() - t
print '2D LZ linewise found: %d, should be %d (Elapsed time : %.2f s)' % (lz_linewise, known_pci['lz_linewise'], elapsed)
assert lz_linewise == known_pci['lz_linewise']

# rolling window :
# bits sequence : 2D LZ linewise found: 7518, should be 7518 (Elapsed time : 75.44 s)

PCI_linewise = lz_linewise / pci.pci_norm_factor(known_pci['data'].T)
print 'PCI linewise found: %f, should be %f' % (PCI_linewise, known_pci['pci_linewise'])
assert np.int(100000*PCI_linewise) == np.int(100000*known_pci['pci_linewise'])

print("End: " + time.strftime("%c"))

