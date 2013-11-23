#!/usr/bin/python
import random
import matplotlib.pyplot as plt

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

# run the game with given number of generations and dictionary of settings
def run(generations, options):
	# INITIALIZE:
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

# graph results
def plotResults(results):
	generations = range(len(results))


	c = '0'
#	cheat_results = [sum(dna.count(c) for dna in result['gene_pool']) for result in results]
	
	fittest_results = []
	for result in results:
		fittest = result['fitness'].index(max(result['fitness']))
		fittest_results.append(result['gene_pool'][fittest].count(c))

	plt.plot(generations, fittest_results)
	plt.title('Total Cheats in Fittest Individual for each Generation')	
	plt.ylabel('Cheats in Fittest Individual')
	plt.xlabel('Generation')
	plt.show()

#plotResults(run(1000, {}))

