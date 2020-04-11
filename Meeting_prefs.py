import math
import random
def shuffler(prefs):
	temp = []
	for i in prefs:
		dic = i
		keys =  list(dic.items())
		random.shuffle(keys)
		dic = dict(keys)
		temp.append(dic)
	return temp
def meeting():
	delay = [i for i in range(61)]
	# alphas = [1.4,1.41,1.42,1.43,1.44]
	alphas = [1.4,1.42,1.44]
	alpha = 1.35
	value = 800
	# values = [750,738,742,734,729]
	values = [750,700,730]
	preferences = []
	for i in range(len(alphas)):
		costs = {}
		check = [k for k in range(61)]
		random.shuffle(check)
		for j in delay:
			cost = (values[i] - (j**alphas[i])*2)/value
			costs[j]= cost
		preferences.append(costs)
	# preferences =  shuffler(preferences)
	# for cost in preferences:
	# 	cur_max = -1
	# 	for items in cost:
	# 		cur_max = max(cur_max,cost[items])
	# 	for items in cost:
	# 		cost[items] = cost[items]/cur_max
	return preferences
pred = meeting()
# print(pred)