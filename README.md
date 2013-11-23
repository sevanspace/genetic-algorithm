genetic-algorithm
=================

Python re-purposing of David Kendrick's [Genetic Algorithms and Evolutionary Games in MATLAB](http://www.laits.utexas.edu/compeco/Courses/ga_matlab.pdf).

Flow:
-----

Fill Gene Pool -> Determine Fitness -> Select Survivors -> Fill Gene Pool


Gene Pool
	-array of DNA strands

DNA
	-array of 1, 0

Fitness
	-array of fitness



Cooperation Matrix:   
	    Coop:   Defect:   
Coop:   (R,R)    (S,T)   
Defect: (T,S)    (P,P)   

For prisoner's dilemma,
	T > R > P > S

where T is 'temptation'
	  R is 'reward'
	  P is 'punishment'
	  S is 'sucker'

If iterative, and prisoner's remember previous action and change plan accordingly, then
	2R > T + S
to prevent alternating cooperation and defection from giving a bigger reward than mutual cooperation


