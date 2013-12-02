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

plot_options = {'rows':3,
	            'cols':2,
	            'figsize':(12, 9.5),
	            'facecolor':'0.75' # gray
	           }	     


generations_array = [20, 50, 100]
plots = []

for g in generations_array:
	print 'Running ' + str(g) + ' generations...'
	results = gagame.run(g, options)
	plots.append(gagame.fittestPlot(results))
	plots.append(gagame.cheatsPlot(results))

gagame.plotFigs(plots, plot_options)


