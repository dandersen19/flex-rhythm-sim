# This simulates multiple performances of a melody with flexible rhythm

# import random library
import random

# melody as MIDI note numbers
line1 = [60, 67, 65, 62, 60, 59, 60]

# build simulation matrix based on a melody, where each row is randomized
# args: melody as list of MIDI nn, performance length, number of performances
# perf_length as number of discrete time units
def build_sim(melody_, perf_length, num_perfs):
    melody = melody_[:] # copy of melody
    l = [] # list of lists (output matrix)
    for i in range(1, num_perfs+1):
        # call nested function to generate random performance and append to list of lists
        l.append(random_performance(melody, perf_length))
    return l

# nested function to generate an individual performance
def random_performance(note_list, perf_length):
    # startup
    num_rnd_vals = len(note_list) + 1 # to account for end of last note
    random_vals = [0, 0] # store random values
    # generate random values    
    while len(set(random_vals)) != len(random_vals): # check if contains duplicates
        i = 0
        random_vals = []
        while i < num_rnd_vals:
            random_vals.append(random.random())
            i +=1
            # clean random values
        random_vals.sort()
        random_vals = [int(i * perf_length) for i in random_vals] # scale to perf_length range   
    # add start/end time values
    random_vals.append(perf_length) # end of performance
    random_vals.insert(0,0) # start of performance 
    # generate differences between random values
    # differences indicate number of repetitions of each element
    random_diffs = [j - i for i, j in zip(random_vals, random_vals[1:])]
    # create a single list representing the performance
    one_perf = []
    note_list.append(0) # add silence at end
    note_list.insert(0,0) # ...and beginning
    for i in range(0, num_rnd_vals+1): # n+1 works because of half-open range
        one_perf += random_diffs[i] * [note_list[i]] # adds a note x times where x = random_diffs[i]
    return one_perf

# simulate performance of line1 melody ten times over 100 time units
build_sim(line1, 100, 10)