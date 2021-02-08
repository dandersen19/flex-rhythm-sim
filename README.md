# indysim
A collection of functions for simulating performances of indeterminate music for analysis.

Computational methods can be used to analyze indeterminate music by generating virtual performances. These methods are especially well suited to music that is indeterminate with respect to duration, or which has flexible synchronization between parts, including works by Earle Brown using proportional notation and works by Morton Feldman such as his "Durations" series. In other words, works comprising a fixed sequence of notes, each of which has indeterminate duration.

This collection of functions can be used to generate a Monte Carlo simulation of such music, and to compare the results of multiple simulations of the same part (melody), or multiple simulations of multiple parts. All melodies are treated as lists of MIDI note numbers (no rhythmic information). Users can specify performance duration, and random durations are scaled accordingly.

Combine with music21 for more advanced pitch analysis. See examples.py for typical usage.

# Functions
## import_score
```bash
import_score(file_name, part=0)
```
Import and format MusicXML file for input (returns list of MIDI nn)
+ file_name - Name and path of MusicXML file enclosed in ''
+ part - specify part in score (for more see [music21 documentation](http://web.mit.edu/music21/doc/moduleReference/moduleStream.html#music21.stream.Score.parts))
## one_perf
```bash
one_perf(note_list_, perf_length, leading=True, trailing=True, between=False)
```
Generate a single virtual performance of a melody
+ note_list_ - melody to be performed (list of MIDI nn)
+ perf_length - Length of performance (number of time units)
+ leading - If true, begin performance with random duration of silence
+ trailing - If true, end perform with random duration of silence
+ between - If true, intersperse each note with random duration of silence
## build_sim
```bash
build_sim(melody_, perf_length, num_perfs, leading=True, trailing=True, between=False)
```
Generate multiple virtual performances of a melody
+ melody_ - melody to be performed (list of MIDI nn)
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
+ sim_in - simulation
## combine_sims
```bash
combine_sims(sims)
```
Combine multiple simulations (multiple melodies) into a single list of lists, organized by unit time
+ sims - list of simulations (of identical size and length)
