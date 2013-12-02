import matplotlib.pyplot as plt

plots = [{'title':'Title!', 'xlabel':'some x', 'ylabel':'some y', 'x':[1,2,3,4], 'y':[0,1,2,3]},
	     {'title':'Title2', 'xlabel':'some x', 'ylabel':'some y', 'x':[1,2,3,5], 'y':[2,1,2,3]}]

def plotFigs(plots):
	fig = plt.figure()
	rows = len(plots)
	for i in range(rows):
		ax = fig.add_subplot(rows, 1, i)
		p = plots[i]
		plt.plot(p.get('x', []), p.get('y', []))
		plt.title(p.get('title', ""))
		plt.ylabel(p.get('ylabel', ""))
		plt.xlabel(p.get('xlabel', ""))
	plt.tight_layout(1.08)
	plt.show()

plotFigs(plots)