# IndySim Project
# Copyright (C) 2021 Drake Andersen
# Functions for simulating performances of indeterminate music for analysis

####################
####  EXAMPLES  ####
####################

# update examples (and sample score file) to show how polyphony, multi-staff parts work

# import file (imports random and music21 as m21)
exec(open('/Users/User/indysim.py').read())

# import a melody from an XML file
my_melody = import_part('/Users/User/sample_score.xml')

# import a second melody using optional args to specify part (1) and measure range (1-3)
my_melody2 = import_part('/Users/User/sample_score.xml', part=1, excerpt=True, first_bar=1, last_bar=3)

# you can also enter a melody as a list of MIDI note numbers
my_melody3 = [72, 71, 69, 67, 65, 62]

# one virtual performance, length = 100, no leading silence
perf1 = one_perf(my_melody, 100, leading=False)

# simulate ten performances of melody, length = 100, with silences interspersed...
sim1 = build_sim(my_melody, 100, 10, between=True)

# ...and ten performances of another melody without interspersed silences
sim2 = build_sim(my_melody2, 100, 10, between=False)

# organize simulation results by unit time...
sim_by_time = sim_time(sim1)

# ...in order to examine pitch content over time
for elem in sim_by_time:
	print(set(elem))

# combine simulations to get verticalities between parts (sims must have same length/number of perfs)
combine_sims([sim1, sim2])

#####################
#####   NOTES   #####
#####################

# performance length should generally be at least one order of magnitude greater than sequence length
# (sequence length = melody length plus any leading, trailing, or interspersed zeroes)
# if the two values are too close it will take too long to get random values that don't duplicate
