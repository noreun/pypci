import pci

# test 1D algorithm

lz = pci.lz_complexity('1001111011000010')
print '1D found: %d, should be %d' % (lz, 6)
#assert lz == 6

# test 2D algorithm (beware: this might take a few minutes!)

import pickle

with open('./lz_2D_example.pickle', 'r') as f:
    known_lz = pickle.load(f)

lz_columnwise = pci.pci(known_lz['data'])
print '2D columnwise found: %d, should be %d' % (lz_columnwise, known_lz['lz_columnwise'])
#assert lz_columnwise == known_lz['lz_columnwise']

lz_linewise = pci.pci(known_lz['data'].T)
print '2D linewise found: %d, should be %d' % (lz_linewise, known_lz['lz_linewise'])
#assert lz_linewise == known_lz['lz_linewise']
