# IndySim Project
# Copyright (C) 2021 Drake Andersen
# Functions for simulating performances of indeterminate music for analysis

#####################
######  SETUP  ######
#####################

# import libraries
import music21 as m21
import random
import operator

######################
#### INPUT FORMAT ####
######################

# melody as list of MIDI note numbers
# my_melody = [60, 67, 65, 62, 60, 59, 60]

# melodies can contain chords (as sub-lists)
# polyphonic_melody = [73, 71, 69, [52, 56, 59, 68], 76, [49, 52, 55, 58], 67]

# see IMPORT_PART function below

#####################
####  FUNCTIONS  ####
#####################

# IMPORT_PART
# import one part from XML score file into list of midi notes (chords represented as sub-lists)
def import_part(file_name, part=0, excerpt=False, first_bar=0, last_bar=1):
    if excerpt == True:
        part_in = m21.converter.parse(file_name).measures(first_bar, last_bar).parts[part]
    else:
        part_in = m21.converter.parse(file_name).parts[part]
    
    # iterates over arbitrarily polyphonic melody (i.e. if it contains single notes and/or chords)
    return [[j.pitch.midi for j in i] if hasattr(i, '__iter__') else i.pitch.midi for i in part_in.recurse().notes]

# ONE_PERF
# function to generate an individual performance
def one_perf(note_list_, perf_length, leading=True, trailing=True, between=False):
    
    note_list = note_list_[:] # copy to not affect source
    
    # whether we include leading, trailing, or interspersed silences (zeroes)
    if between==True:
        for list_pos in range(1, len(note_list)*2-1, 2): # adds silence between each note
            note_list.insert(list_pos, 0)
    if leading==True:
        note_list.insert(0,0) # add silence at beginning
    if trailing==True:
        note_list.append(0) # add silence at end
    
    seq_length = len(note_list) # number of notes plus any zeroes added above
    
    if seq_length > perf_length: # stop if seq_length > perf_length
        print("Sequence length cannot be greater than performance length.")
        return
    
    random_vals = [0,0] # assign var (and allow while loop to start)
    
    # generate random values    
    while len(set(random_vals)) != len(random_vals): # check for duplicates
        i = 0
        random_vals = []
        while i < (seq_length-1): # generate and append values
            random_vals.append(random.random())
            i +=1    
        random_vals.sort() # sort
        random_vals = [int(val * perf_length) for val in random_vals] # scale to perf_length range
        
        # add start and end of performance to list (needed to calculate differences below)
        # note: we do it inside loop to avoid potential duplicate leading 0 in random_vals
        random_vals.insert(0,0)
        random_vals.append(perf_length)
    
    # generate differences between random values
    # differences indicate number of repetitions of each element
    random_diffs = [j - i for i, j in zip(random_vals, random_vals[1:])]
    
    # create a single list representing the performance
    the_perf = []
    for i in range(len(random_diffs)):
        the_perf += random_diffs[i] * [note_list[i]] # adds a note x times where x = random_diffs[i]
    return the_perf

# BUILD_SIM
# build matrix of performances of single melody where each row is random performance
def build_sim(note_list_, perf_length, num_perfs, leading=True, trailing=True, between=False):    
    
    note_list = note_list_[:] # copy of note_list
    l = [] # list of lists (output matrix)
    
    for i in range(num_perfs):
        # call nested function to generate random performance and append to list
        l.append(one_perf(note_list, perf_length, leading, trailing, between))
    
    return l # return list of lists

# SIM_TIME
# organize simulation results by unit time (like heat map for notes)
def sim_time(sim_in):
    return [[sim_in[j][i] for j in range(len(sim_in))] for i in range(len(sim_in[0]))]

# COMBINE_SIMS
# combine two or more simulations (simulation = multiple performances of same melody, same length)
def combine_sims(sims):
    
    # initial tests
    
    # does each sim contain multiple performances? perform depth count
    def depthCount(all_sims):
        return 1 + max(map(depthCount, all_sims)) if all_sims and isinstance(all_sims, list) else 0
    
    # if each sim contains only a single performance, algo is slight different as given:
    if depthCount(sims) == 2:
        perf_length_list = []
        
        # make sure each perf is same length
        for elem in sims:
            perf_length_list.append(len(elem))
        if len(set(perf_length_list)) != 1:
            print("Length of performances do not match.")
            return
        
        # join multiple single-perf sims
        return [[sims[i][j] for i in range(len(sims))] for j in range(perf_length_list[0])]
        
    # if each sim does contain multiple performances, continue from here with tests
    
    # first, make sure it's same number of performances in each
    sim_length_list = [len(elem) for elem in sims]
    if len(set(sim_length_list)) != 1:
        print("Number of performances do not match.")
        return
	
    # check for uniform length in each performance
    perf_length_list = []
    for perf in sims:
        for elem in perf:
            perf_length_list.append(len(elem))
    if len(set(perf_length_list)) != 1:
        print("Length of performances do not match.")
        return

    # join multiple sims (with multiple perfs) into a single list of lists (of lists...) 
    return [[[sims[i][j][k] for i in range(len(sims))] for j in range(sim_length_list[0])] for k in range(perf_length_list[0])]

# SET_FREQ
# create a dictionary with set class prevalence per unit time
def set_freq(set_list):
	freq_dict = {}
	
	# going directly from MIDI notes to m21 chords is very slow
	# much faster to recreate table of integers as list of list of m21 pitches
	# then convert list of pitches to chords (thanks @jacobtylerwalls)
    
	time_list = []
	for chord in set_list:
		chord_list = []
		for note in chord:
			if hasattr(note, '__iter__'): # if "note" is actually a chord
				for subnote in note:
					chord_list.append(m21.pitch.Pitch(subnote))
			if note != 0 and hasattr(note, '__iter__') == False:
				chord_list.append(m21.pitch.Pitch(note))
		time_list.append(chord_list)
    
	# pitches to chords to prime form string
	final_list = [m21.chord.Chord(elem).primeFormString for elem in time_list if elem]
	
	# count using dictionary
	for item in final_list:
		if (item in freq_dict):
			freq_dict[item] += 1
		else:
			freq_dict[item] = 1
	# empty sets counted as silence
	freq_dict['<Silence>'] = len(set_list) - sum(freq_dict.values())
	return freq_dict # return dictionary