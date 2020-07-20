import numpy.polynomial.polynomial as poly
import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

import numpy as np

if __name__ == '__main__':
	# T=[0.81264690482,0.809458201987,0.718123423633,0.636227485346,0.622134649271]
	# BR=[0.684020435479,0.733501818328,0.623964288599,0.612728875613,0.626143902764]
	# C=[0.646728340146,0.671610505837,0.572670337598,0.65114164946,0.676002165624]
	# # E=[0.828032515464,0.90472181626,0.699235613493,0.839920864407,0.727065676307]
	# l=[0.569756283902,0.529989667612,0.543375267219,0.563933950832,0.525653569458]

	# T=[0.1,0.1,0.1085,0.1715,0.2625,0.1,0.12,0.1855,0.255,0.3615]
	# BR=[0.4565,0.4055,0.4325,0.4985,0.3835,0.446,0.4305,0.423,0.4205,0.3755]
	# C=[0.423,0.434,0.4225,0.4075,0.3665,0.431,0.438,0.427,0.427,0.421]
	# l=[0.4,0.4,0.4,0.4,0.3,0.4,0.4,0.4,0.4,0.35]

	T = [0.29,0.2755,0.295,0.2395,0.247,0.308,0.254,0.2985,0.248,0.259]
	BR=[0.35,0.3445,0.335,0.3005,0.273,0.447,0.355,0.3515,0.302,0.301]
	C=[0.429,0.335,0.2635,0.363,0.238,0.432,0.326,0.358,0.324,0.317]
	l=[0.417,0.385,0.38,0.3675,0.251,0.446,0.381,0.374,0.369,0.395]

	lT=[0.583,0.615,0.62,0.6325,0.209,0.434,0.389,0.376,0.371,0.365]

	# T = [0.31987,0.344899,0.312099,0.303078,0.246754]
	# BR =[0.679603,0.654546,0.617366,0.546409,0.412775]
	# C= [0.6415,0.634,0.5945,0.523,0.411]

	# T=[0.636,0.69,0.67,0.69,0.688,0.631,0.63,0.635,0.641,0.658]
	# BR=[0.686,0.702,0.695,0.709,0.733,0.639,0.64,0.64,0.643,0.662]
	# C= [0.656,0.65,0.655,0.647,0.665,0.667,0.659,0.647,0.651,0.654]
	# l = [0.6315,0.6,0.6,0.6,0.639,0.6,0.6,0.6,0.6,0.604 ]


	# T=[0.529,0.528,0.543,0.586,0.677,0.558,0.56,0.577,0.598,0.6535]
	# BR =[0.691,0.696,0.681,0.706,0.647,0.649,0.649,0.641,0.648,0.671]
	# C= [0.646,0.646,0.661,0.638,0.627,0.647,0.652,0.65,0.657,0.648]
	# l=[0.6,0.6,0.6,0.6,0.656,0.6,0.6,0.6,0.6,0.628]

	# T= [0.315003,0.312674,0.245811,0.265072,0.272938]
	# BR =[0.318992,0.31917,0.332934,0.288322,0.258221]
	# C = [0.31515,0.278934,0.289327,0.290485,0.269499]
	# l =[0.036167,0.011098,0.098154,0.003923,0.006884]



	# T=[0.81264690482,0.809458201987,0.718123423633,0.636227485346,0.622134649271]
	# BR=[0.684020435479,0.733501818328,0.623964288599,0.612728875613,0.626143902764]
	# C=[0.646728340146,0.671610505837,0.572670337598,0.65114164946,0.676002165624]
	# E=[0.828032515464,0.90472181626,0.699235613493,0.839920864407,0.727065676307]
	# l=[0.569756283902,0.529989667612,0.543375267219,0.563933950832,0.525653569458]


	# T=[0.00116569,0.00037675,7.29110688e-05,2.49376086e-05,4.51792265e-06]
	# BR=[1.01142958e-06,4.27800953e-07,7.58679986e-07,2.20548496e-07,4.70505219e-07]
	
	# C=[2.55369224e-06,1.70300467e-06,1.24939737e-06,1.00997736e-06,9.51318949e-07]
	# E=[1.64179827e-05,4.78732686e-06,4.82786546e-06,2.90655909e-06,1.25580967e-06]

	# l=[4.33759299e-08,4.33759299e-08,4.33759299e-08,4.33759299e-08,4.33759299e-08]

	# T=[0.00442562,0.00318098,0.00140697,0.00092845,0.00123549]
	# BR=[0.00095516,0.00082508,0.00084339,0.00091535,0.0010098]

	# C=[0.00078907,0.00074429,0.00080286,0.00084817,0.00072078]
	# E=[0.00108474,0.00094274,0.00067166,0.00107201,0.00225723]

	# T=[0.24258,0.26151,0.25446,0.27204,0.25938,0.315,0.3402,0.3654,0.3528,0.2898]
	# BR=[0.228994,0.256638,0.223503,0.232683,0.239725,0.275277,0.286604,0.350886,0.342092,0.330918]
	# C=[0.202285,0.222893,0.226704,0.225414,0.22638,0.316512,0.30775,0.013769275,0.31689,0.29988,0.3276]
	# E=[0.203844,0.231634,0.214468,0.239115,0.22638,0.312317,0.252078,0.31815,0.2961,00.01731675.3276]

	PerBR=[]
	PerC =[]
	# PerE =[]
	Perl =[]

	x_axis=[]
	my_xticks=[]
	UpdateRate=[2,5,10,20,50]
	Intervals=[4,2]
	# Intervals = [9]

	for i in xrange(1,len(T)+1):
		x_axis.append(i)
	for i in xrange(0,len(Intervals)):
		for j in xrange(0,len(UpdateRate)):
			tup=(Intervals[i],UpdateRate[j])
			my_xticks.append(tup)
	# print len(my_xticks)		
	# x_axis=[2,5,10,20,50]
	# my_xticks=x_axis
	# print x_axis
	# x_axis=[1,1.2,1.4,1.6]

	# for i in xrange(0,len(T)):
	# 	PerBR.append((float(T[i]-BR[i])/T[i])*100)
	# 	PerC.append((float(T[i]-C[i])/T[i])*100)
	# 	# PerE.append((float(T[i]-E[i])/T[i])*100)
	# 	Perl.append((float(T[i]-l[i])/T[i])*100)

	for i in xrange(0,len(T)):
		PerBR.append((float(BR[i]-T[i])/T[i])*100)
		PerC.append((float(C[i]-T[i])/T[i])*100)
		# PerE.append((float(T[i]-E[i])/T[i])*100)
		Perl.append((float(l[i]-lT[i])/lT[i])*100)


	plt.figure('smoothness')
	font = {'weight' : 'bold','size'   : 20 }
	# fig, ax = plt.subplots(1, 1)
	# axes = plt.gca()
	# axes.set_xlim([1,50])
	# axes.set_ylim([-42,55])
	# fig, ax = plt.subplots(1,1)
	
	plt.xticks(x_axis,my_xticks)
	
	# print len(x_axis)
	# print len(PerBR)
	# ax.xaxis.set_major_locator(ticker.MultipleLocator(1.0))
	plt.yticks(fontsize=14,fontweight='bold')
	plt.xticks(fontsize=13,fontweight='bold')

	# plt.xaxis.set_major_locator(ticker.MultipleLocator(1))

	legend_properties = {'weight':'bold', 'size':15}

	lineBR,=plt.plot(x_axis,PerBR, marker='o', linestyle='--', color='r', linewidth=6, markersize=12)
	lineC, =plt.plot(x_axis,PerC, marker='^', linestyle='-.', color='g', linewidth=7, markersize=12)
	# lineE, =plt.plot(x_axis,PerE, marker='s', linestyle=':', color='b', linewidth=7, markersize=12)
	linel, =plt.plot(x_axis,Perl, marker='d', linestyle='-', color='m', linewidth=2, markersize=12)
	

	# plt.legend([lineBR,lineC,lineE,linel],["Bayesian","Counter","Exponential","LSTM"],loc=0,ncol=1, handlelength=4,prop=legend_properties)
	plt.legend([lineBR,lineC,linel],["Bayesian","Counter","LSTM"],loc=0,ncol=1, handlelength=4,prop=legend_properties)
	plt.xlabel("Hypothesis,UpdateRate",**font)
	plt.ylabel("Average Percentage Utility",**font)
	# plt.ylim(-20,40)
	# ax.set_xticks(x_axis, minor=True)
	# plt.title("Residual Error for Meeting Scheduling Domain",**font)
	# print np.mean(PerBR)
	# print np.mean(PerC)
	# # print np.mean(PerE)
	# print np.mean(Perl)

	plt.show()
	# plt.savefig('outcutilityonac.pdf', format='pdf', dpi=1000)