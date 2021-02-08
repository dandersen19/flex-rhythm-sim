# indysim
Monte Carlo simulation of the performance of a melody with flexible rhythm. Specifically, it is designed for computational analysis of indeterminate or improvised music where the duration of notes in a fixed sequence is free. In simulated performance, all notes are played in sequence, but with random duration.

Simply specify a melody (as a list of MIDI note numbers), the performance duration (as a number of discrete time units), and the number of performnaces to simulate. The performance will begin and end with silence of random duration.

Output is a matrix (list of lists) where columns = time, rows = individual performances.
