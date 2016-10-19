
import pci
import pickle
import time

# BEWARE: this takes ~17 min in a Intel Xeon CPU E5-2630 v3 @ 2.40GHz

print("Start: " + time.strftime("%c"))

# test 1D algorithm

lz = pci.lz_complexity('1001111011000010')
print '1D found: %d, should be %d' % (lz, 6)
#assert lz == 6

# test 2D algorithm (beware: this might take a few minutes!)

with open('./lz_2D_example.pickle', 'r') as f:
    known_lz = pickle.load(f)

# lz_columnwise = pci.lz_complexity_2D(known_lz['data'])
# print '2D columnwise found: %d, should be %d' % (lz_columnwise, known_lz['lz_columnwise'])
# #assert lz_columnwise == known_lz['lz_columnwise']


#lz_linewise = pci.lz_complexity_2D(known_lz['data'].T)
x = known_lz['data'].T
#x = x[:100,:100]
lz_linewise = pci.lz_complexity_2D(x)
print '2D linewise found: %d, should be %d' % (lz_linewise, known_lz['lz_linewise'])
#assert lz_linewise == known_lz['lz_linewise']

print("End: " + time.strftime("%c"))

#Start: Tue Oct 18 12:20:04 2016
#1D found: 6, should be 6
#2D columnwise found: 16841, should be 16842
#2D linewise found: 7486, should be 7518
#End: Tue Oct 18 12:37:07 2016

