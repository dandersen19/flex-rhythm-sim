# indysim
Package for simulating and analyzing experimental music.

Computational methods can be used to analyze experimental music by generating virtual performances. These methods are especially well suited to music that is indeterminate with respect to duration, or which has flexible synchronization between parts, including works by Earle Brown using proportional notation and works by Morton Feldman such as his "Durations" series. In other words, works comprising a fixed sequence of notes, each of which has flexible duration.

This collection of functions can be used to generate a Monte Carlo simulation of indeterminate music, and to compare the results of multiple simulations of the same part (melody), or multiple simulations of multiple parts. All melodies are treated as lists of MIDI note numbers (no rhythmic information; chords are represented as sub-lists). Users can specify performance duration, and random durations are scaled accordingly.

Combine with music21 for more advanced pitch analysis. See examples.py for typical usage.

# Functions
## import_part
```bash
import_part(file_name, part=0, excerpt=False, first_bar=0, last_bar=1)
```
Import and format MusicXML file for input (returns list of MIDI nn)
+ file_name - Name and path of MusicXML file enclosed in ''
+ part - Specify part in score (for more see [music21 documentation](http://web.mit.edu/music21/doc/moduleReference/moduleStream.html#music21.stream.Score.parts))
+ excerpt - If true, melody imported for measure range specified by first_bar, last_bar
+ first_bar - If excerpt=True, first measure in range (pickup bar=0)
+ last_bar - If excerpt=True, last measure in range (inclusive)
## import_multistaff
```bash
import_multistaff(file_name, part_nums=[0,1], excerpt=False, first_bar=0, last_bar=1)
```
Import and format multiple staves from MusicXML file as a single part
+ file_name - Name and path of MusicXML file enclosed in ''
+ part_nums - Specify parts in score as list (for more see [music21 documentation](http://web.mit.edu/music21/doc/moduleReference/moduleStream.html#music21.stream.Score.parts))
+ excerpt - If true, melody imported for measure range specified by first_bar, last_bar
+ first_bar - If excerpt=True, first measure in range (pickup bar=0)
+ last_bar - If excerpt=True, last measure in range (inclusive)
## one_perf
```bash
one_perf(note_list_, perf_length, leading=True, trailing=True, between=False)
```
Generate a single virtual performance of a melody
+ note_list_ - Melody to be performed (list of MIDI nn)
+ perf_length - Length of performance (number of time units)
+ leading - If true, begin performance with random duration of silence
+ trailing - If true, end perform with random duration of silence
+ between - If true, intersperse each note with random duration of silence
## build_sim
```bash
build_sim(note_list_, perf_length, num_perfs, leading=True, trailing=True, between=False)
```
Generate multiple virtual performances of a melody
+ note_list_ - Melody to be performed (list of MIDI nn)
+ perf_length - Length of performance (number of time units)
+ num_perfs - Number of performances to simulate
+ leading - If true, begin performance with random duration of silence
+ trailing - If true, end perform with random duration of silence
+ between - If true, intersperse each note with random duration of silence
## sim_time
```bash
sim_time(sim_in)
```
Organize results of a single simulation by unit time
+ sim_in - Simulation
## combine_sims
```bash
combine_sims(sims)
```
Combine multiple simulations (multiple melodies) into a single list of lists, organized by unit time
+ sims - List of simulations (of identical size and length)
## set_freq
```bash
set_freq(set_list)
```
Generates a dictionary with prevalence of all set classes in a given list of pitch (or pc) sets
+ set_list - List of pitch sets (list of lists)
## get_lewins
```bash
get_lewins(pcset)
```
Calculates Lewins on Fourier balances 1-6 for any pitch set (per Ian Quinn 2006/2007)
+ pitch_set - List of pitch classes (or pitches)
