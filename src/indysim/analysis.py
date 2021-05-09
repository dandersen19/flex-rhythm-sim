# IndySim Project
# Copyright (C) 2021 Drake Andersen
# Package for simulating and analyzing experimental music

#####################
### ANALYSIS TOOLS ##
#####################

#####################
######  SETUP  ######
#####################

# import libraries
import music21 as m21
import random
import operator
import math

# SET_FREQ
# create a dictionary with set class prevalence given a list of pitch sets (list of lists)
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

# GET_LEWINS
# Calculating Lewins for Fourier balances 1-6 from pcset
# See Ian Quinn, General Equal-Tempered Harmony, PNM 44 no. 2 and 45 no. 1 (2006)

def arrow_end_coords(angle):
   angle = math.radians(angle)
   x = math.cos(angle)
   y = math.sin(angle)
   coords = [x,y]
   return coords

def total_distance(all_angles):
   x = 0
   y = 0
   for i in all_angles:
      x = x + arrow_end_coords(i)[0]
      y = y + arrow_end_coords(i)[1]
   return math.sqrt(pow(x,2)+pow(y,2))

def get_lewins(pcset):

   pcset = [p % 12 for p in pcset] # convert to pc

   lewins = [] # will become output list of Lewins for balances 1-6

   # fourier balance 1
   lewins.append(total_distance([balance1[i] for i in pcset]))

   # fourier balance 2
   lewins.append(total_distance([balance2[i] for i in pcset]))

   # fourier balance 3
   lewins.append(total_distance([balance3[i] for i in pcset]))

   # fourier balance 4
   lewins.append(total_distance([balance4[i] for i in pcset]))

   # fourier balance 5
   lewins.append(total_distance([balance5[i] for i in pcset]))

   # fourier balance 6
   lewins.append(total_distance([balance6[i] for i in pcset]))

   return lewins # [Lw(balance1), Lw(balance2), ... Lw(balance6)]

balance1 = {
   0: 90,
   1: 60,
   2: 30,
   3: 0,
   4: 330,
   5: 300,
   6: 270,
   7: 240,
   8: 210,
   9: 180,
   10: 150,
   11: 120
} 

balance2 = {
   0: 90,
   1: 30,
   2: 330,
   3: 270,
   4: 210,
   5: 150,
   6: 90,
   7: 30,
   8: 330,
   9: 270,
   10: 210,
   11: 150
} 

balance3 = {
   0: 90,
   1: 0,
   2: 270,
   3: 180,
   4: 90,
   5: 0,
   6: 270,
   7: 180,
   8: 90,
   9: 0,
   10: 270,
   11: 180
} 

balance4 = {
   0: 90,
   1: 330,
   2: 210,
   3: 90,
   4: 330,
   5: 210,
   6: 90,
   7: 330,
   8: 210,
   9: 90,
   10: 330,
   11: 210
} 

balance5 = {
   0: 90,
   1: 300,
   2: 150,
   3: 0,
   4: 210,
   5: 60,
   6: 270,
   7: 120,
   8: 330,
   9: 180,
   10: 30,
   11: 240
} 

balance6 = {
   0: 90,
   1: 180,
   2: 90,
   3: 180,
   4: 90,
   5: 180,
   6: 90,
   7: 180,
   8: 90,
   9: 180,
   10: 90,
   11: 180
} 