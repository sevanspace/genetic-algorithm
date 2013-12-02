#!/usr/bin/python
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy

'''
reward_matrix:
	    TheirBit:
MyBit:   0    1
	0 [ P  ,  T ]
	1 [ S  ,  R ]
where
	1 = cooperation
	0 = defection/cheat

r[0][0] = my punishment
r[1][0] = my temptation
r[1][1] = my reward
'''
# cheat bit, i.e. the bit representation of a cheating action by a player
CHEAT_BIT = '0'

'''
 _______       _______    
(  ____ \     (  ___  )   
| (    \/     | (   ) |   
| |           | (___) |   
| | ____      |  ___  |   
| | \_  )     | (   ) |   
| (___) |  _  | )   ( |  _ 
(_______) (_) |/     \| (_)
                 
(Genetic Algorithm)
'''

# return an array of DNA strands created from survivor/parent DNAs
def fillGenePool(survivors, size, min_num_mutations, max_num_mutations):
	gene_pool = []
	# fill gene pool from mutations/crossovers of parent DNAs
	for i in range(size):
		parents = randomCouple(survivors)
		child = mutate(crossover(parents[0],parents[1]), min_num_mutations, max_num_mutations)
		gene_pool.append(child)
	return gene_pool

# return a randomized gene pool of given size and DNA length
def createGenePool(size, dna_length):
	# initialize a gene pool filled with random DNA
	gene_pool = [randomDNA(dna_length) for i in range(size)]
	return gene_pool

# return a fitness vector by competing every dna in the genepool against every other
def determineFitness(gene_pool, reward_matrix):
	# create a fitness vector from the given population
	fitness = [sum(compete(dna, opponent, reward_matrix) for opponent in gene_pool if opponent is not dna) for dna in gene_pool]
	return fitness
				
# return a score result from comparing given dna to opponent
# higher score means given dna performs better against opponent
# go through dna, compare each against the rest
def compete(dna, opponent, reward_matrix):
	return sum(getReward(dna[i], opponent[i], reward_matrix) for i in range(len(dna)))


# get reward based on "my" vs "their" decision as specified in reward_matrix
def getReward(my_bit, their_bit, reward_matrix):
	return reward_matrix[int(my_bit)][int(their_bit)]

# return an array of DNA from genePool based on matching fitness array
def selectSurvivors(gene_pool, fitness, num_survivors):
	# get N highest fitness DNA from genePool
	f = fitness[:]
	survivors = []
	for n in range(num_survivors):
		max_i = f.index(max(f))
		survivors.append(gene_pool[max_i])
		f.pop(max_i)
	return survivors

# return a random binary string of N length
def randomDNA(d): 
    mx = (2 ** d) - 1 
    b = bin(random.randint(0, mx)) 
    return b[2:].rjust(d, '0')

# return a child DNA with a random crossover between 2 parent DNAs
def crossover(parent1, parent2):
	crossover_point = random.randint(0,len(parent2))
	child = parent1[:crossover_point] + parent2[crossover_point:]
	return child

# return a randomly mutated version of the given DNA
def mutate(dna, minm, maxm):
	num_mutations = random.randint(minm, maxm)
	for i in range(num_mutations):
		mutate_index = random.randint(0, (len(dna) - 1))
		if int(dna[mutate_index]) == 0:
			bit = '1'
		else:
			bit = '0'
		dna = dna[:mutate_index] + bit + dna[(mutate_index + 1):]
	return dna

# return 2 different parents from a given array of survivor DNAs
def randomCouple(survivors):
	s = survivors[:]
	parent1 = s.pop(random.randint(0,(len(s)- 1)))
	parent2 = s.pop(random.randint(0,(len(s)- 1)))
	return [parent1, parent2]

'''
 _______             _       
(  ____ ) |\     /| ( (    /|
| (    )| | )   ( | |  \  ( |
| (____)| | |   | | |   \ | |
|     __) | |   | | | (\ \) |
| (\ (    | |   | | | | \   |
| ) \ \__ | (___) | | )  \  |
|/   \__/ (_______) |/    )_)
                           
'''

# run the game with given number of generations and options
# repeat for given number of trials
# return array of results
def runTrials(trials=1, generations=50, options=None):
	return [run(generations,options) for i in range(trials)]

# run the game with given number of generations and options
def run(generations=50, options=None):
	if options is None:	options = {}

	# save results
	results = []

	# number of survivors selected from gene pool
	num_survivors = options.get('num_survivors') or 2

	# size of gene_pool
	gene_pool_size = options.get('gene_pool_size') or 8

	# length of DNA a.k.a number of "rounds"
	dna_length = options.get('dna_length') or 24

	# max and min number of mutations in a new DNA (uniform probability)
	max_num_mutations = options.get('max_num_mutations') or 4
	min_num_mutations = options.get('min_num_mutations') or 1

	# default cooperation/defection payoffs
	reward = 10
	temptation = 20
	punishment = 5
	sucker = 0

	reward_matrix = options.get('reward_matrix') or [[punishment, temptation],
                 [sucker, reward]]
	
	# RUN:
	gene_pool = createGenePool(gene_pool_size, dna_length)

	for i in range(generations):
		fitness_vector = determineFitness(gene_pool, reward_matrix)
		survivors = selectSurvivors(gene_pool, fitness_vector, num_survivors)

		# record results before replacing gene_pool
		result = {}
		result['gene_pool'] = gene_pool
		result['fitness'] = fitness_vector
		results.append(result)

		gene_pool = fillGenePool(survivors, gene_pool_size, min_num_mutations, max_num_mutations)

	return results

'''
 _______   _______   _______             _     _________  _______ 
(  ____ ) (  ____ \ (  ____ \ |\     /| ( \    \__   __/ (  ____ \
| (    )| | (    \/ | (    \/ | )   ( | | (       ) (    | (    \/
| (____)| | (__     | (_____  | |   | | | |       | |    | (_____ 
|     __) |  __)    (_____  ) | |   | | | |       | |    (_____  )
| (\ (    | (             ) | | |   | | | |       | |          ) |
| ) \ \__ | (____/\ /\____) | | (___) | | (____/\ | |    /\____) |
|/   \__/ (_______/ \_______) (_______) (_______/ )_(    \_______)
'''                                                          

# builds plot info from result data for the fittest individual in each generation
def fittestPlot(results):
	return _makePlot(results, 'Total Cheat Bits in Fittest Individual for each Generation',
		      'Cheat Bits in Fittest Individual', _getFitnessPlotY)

# builds plot info from array of results for average fittest individual in each generation
def avgFittestPlot(results_array):
	return _makePlot(results_array, 'Avg Total Cheat Bits in Fittest Individuals',
		       'Cheat Bits', _getAvgFitnessPlotY, generations=len(results_array[0]))
#	return numpy.mean(numpy.array([fittestPlot(r).get('y') for r in results_array]), axis=0)
	
# helper function for generating Y for fittestPlot
def _getFitnessPlotY(results):
	global CHEAT_BIT
	return [r['gene_pool'][r['fitness'].index(max(r['fitness']))].count(CHEAT_BIT) for r in results]

# helper function returns average fittestPlot Y values
def _getAvgFitnessPlotY(results_array):
	return _getAvg(results_array, _getFitnessPlotY)

# builds plot info from result data for total cheats in gene pool in each generation
def cheatsPlot(results):
	return _makePlot(results, 'Total Cheat Bits in Gene Pool for each Generation',
		      'Cheat Bits in Gene Pool', _getCheatsPlotY)

# builds plot info from array of results for total cheats in gene pool in each generation
def avgCheatsPlot(results_array):
	return _makePlot(results_array, 'Avg Total Cheat Bits in Gene Pools',
		       'Cheat Bits', _getAvgCheatsPlotY, generations=len(results_array[0]))

# helper function for generating Y for cheatsPlot
def _getCheatsPlotY(results):
	global CHEAT_BIT
	return [sum(dna.count(CHEAT_BIT) for dna in r['gene_pool']) for r in results]

# helper function returns average cheatsPlot Y values
def _getAvgCheatsPlotY(results_array):
	return _getAvg(results_array, _getCheatsPlotY)

def totalFitnessPlot(results):
	return _makePlot(results, 'Total Fitness of Gene Pool',
		        'Fitness', _getTotalFitnessPlotY)

def avgTotalFitnessPlot(results_array):
	return _makePlot(results_array, 'Avg Total Fitness of Gene Pool',
		        'Fitness', _getAvgTotalFitnessPlotY, generations=len(results_array[0]))

def _getTotalFitnessPlotY(results):
	return [sum(fitness for fitness in r['fitness']) for r in results]

def _getAvgTotalFitnessPlotY(results_array):
	return _getAvg(results_array, _getTotalFitnessPlotY)


# helper function averages columns of Y values in array of results
def _getAvg(results_array, y_function):
	return numpy.mean(numpy.array([y_function(r) for r in results_array]), axis=0)

# helper function generates generational data given a function to run on results to generate y
def _makePlot(results, title, ylabel, y_function, generations=None):
	try:
		y = y_function(results)
	except KeyError:
		print "Unrecognized result data."
		return None

	return {'title':title,
	        'xlabel':'Generation',
	        'x': range(generations or len(results)),
	        'ylabel':'Cheat Bits', # ylabel,
	        'y':y }

# takes array of plot data, and plots all as a column of subplots in a figure
def plotFigs(plots, options=None):
	if options is None: options = {}

	rows = options.get('rows') or len(plots)
	cols = options.get('cols') or 1
	figsize = options.get('figsize') or (9,9)
	facecolor = options.get('facecolor') or 'w'

	fig = plt.figure(figsize=figsize, facecolor=facecolor)

	gs = gridspec.GridSpec(rows, cols)

	for i in range(len(plots)):
		ax = plt.subplot(gs[i])
		p = plots[i]
		plt.plot(p.get('x', []), p.get('y', []))
		plt.title(p.get('title', ""))
		plt.ylabel(p.get('ylabel', ""))
		plt.xlabel(p.get('xlabel', ""))

	gs.tight_layout(fig)
	plt.show()
