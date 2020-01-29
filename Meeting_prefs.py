import math

def meeting():
	delay = [i for i in range(61)]
	alphas = [1.35,1.4,1.454]
	alpha = 1.35
	value = 800
	values = [600,550,575]
	preferences = []
	for i in range(len(alphas)):
		costs = {}
		for j in delay:
			cost = (values[i] - (j**alphas[i])*2)/value
			costs[j]= cost
		preferences.append(costs)
	return preferences
pred = meeting()
# print(pred)	