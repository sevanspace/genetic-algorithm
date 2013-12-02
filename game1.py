#!/usr/bin/python

import gagame

reward = 10
temptation = 20
punishment = 5
sucker = 0

reward_matrix = [[punishment, temptation],
[sucker, reward]]

options = {'num_survivors':2,
	       'gene_pool_size':30,
	       'dna_length':24,
	       'max_num_mutations':1,
	       'min_num_mutations':0,
	       'reward_matrix':reward_matrix
	       }

plot_options = {'rows':5,
	            'cols':3,
	            'figsize':(12, 9.5),
	            'facecolor':'0.75' # gray
	           }	     


# For running tests on changing various option parameters:
# Uncomment any one or more of the commented tests and run this file

generations_array = [100]

plots = []

for g in generations_array:
	print 'Running ' + str(g) + ' generations...'

	# Un-comment 
	for i in range(5):
		print '   Test ' + str(i)
		# options['num_survivors'] = 2 + i
		# options['gene_pool_size'] = 8 * (2**i)
		# options['dna_length'] = 8 * (2**i)
		# options['max_num_mutations'] = 1 * (2**i)
		# options['min_num_mutations'] = 1 * (2**i) - 1
		# options['reward_matrix'][0][0] = [0,5,10,20,300][i] # punishment
		# options['reward_matrix'][0][1] = [0,5,10,20,300][i] # temptation
		# options['reward_matrix'][1][0] = [0,5,10,20,300][i] # sucker
		# options['reward_matrix'][1][1] = [0,5,10,20,300][i] # reward
		options['max_num_mutations'] = [0, 1, 2, 3, 4][i] 
		results = gagame.run(g, options)
		plots.append(gagame.fittestPlot(results))
		plots.append(gagame.cheatsPlot(results))
		plots.append(gagame.totalFitnessPlot(results))

gagame.plotFigs(plots, plot_options)


