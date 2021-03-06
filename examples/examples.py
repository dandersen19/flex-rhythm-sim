# IndySim Project
# Copyright (C) 2021 Drake Andersen
# Functions for simulating performances of indeterminate music for analysis

####################
####  EXAMPLES  ####
####################

import operator

from indysim import analysis
from indysim import simulation

# import a melody from an XML file
my_melody = simulation.import_part('/Users/User/sample_score.xml')

# import a second melody using optional args to specify part (1) and measure range (1-3)
my_melody2 = simulation.import_part('/Users/User/sample_score.xml', part=1, excerpt=True, first_bar=1, last_bar=3)

# import two staves from a score (parts 0 and 1) into a single part (for multistaff instruments like piano)
my_melody3 = simulation.import_multistaff('/Users/User/sample_score.xml', [0,1])

# you can also enter a melody directly as a list of MIDI note numbers
# melodies can contain single notes, chords, or both (chords are imported as sub-lists)
my_melody4 = [73, 71, 69, [52, 56, 59, 68], 76, [49, 52, 55, 58], 67]

# one virtual performance, length = 100, no leading silence
perf1 = simulation.one_perf(my_melody, 100, leading=False)

# simulate ten performances of melody, length = 100, with silences interspersed...
sim1 = simulation.build_sim(my_melody, 100, 10, between=True)

# ...and ten performances of another melody without interspersed silences
sim2 = simulation.build_sim(my_melody2, 100, 10, between=False)

# organize simulation results by unit time...
sim_by_time = simulation.sim_time(sim1)

# ...in order to examine pitch content over time
for elem in sim_by_time:
	print(set(elem))

# combine simulations to get verticalities between parts (sims must have same length/number of perfs)
combined = simulation.combine_sims([sim1, sim2])

# see the most prevalent set class per unit time (over the first 100 time units)
for i in range(100):
   print("Time Unit:",i)
   max(analysis.set_freq(combined[i]).items(), key=operator.itemgetter(1))[0]

# get Lewins for a given pitch set (pitches or pc, in MIDI note numbers)
analysis.get_lewins([60, 62, 64])

# get Lewins of most prevalent set class per unit time (over the first 100 time units)
for i in range(100):
   print("Time Unit:",i)
   set_out = (str_to_list(max(analysis.set_freq(combined[i]).items(), key=operator.itemgetter(1))[0]))
   if set_out != None:
      analysis.get_lewins(set_out)

# N.B. above requires this function to convert string-based m21 labels to lists for get_lewins()
def str_to_list(set_in):
   if set_in == '<Silence>':
      return
   else:
      set_in = [pc for pc in set_in[1:-1]] # make into a list and trim '<' and '>'
      if 'A' in set_in:
         set_in[set_in.index('A')] = '10' # in case set class contains 10 (represented in m21 as "A")
      if 'B' in set_in:
         set_in[set_in.index('B')] = '11' # in case set class contains 11 (represented in m21 as "B")
      return [int(pc) for pc in set_in]

#####################
#####   NOTES   #####
#####################

'''
performance length should generally be at least one order of magnitude greater than sequence length
(sequence length = melody length plus any leading, trailing, or interspersed zeroes)
if the two values are too close it will take too long to get random values that don't duplicate
'''
