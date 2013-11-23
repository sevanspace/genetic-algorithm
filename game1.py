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

generations = 100

results = gagame.run(generations, options)
gagame.plotResults(results)
