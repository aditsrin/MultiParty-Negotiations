import random
import numpy as np
import math
import numpy.polynomial.polynomial as poly
import matplotlib
import matplotlib.pyplot as plt
import operator
import matplotlib.backends.backend_pdf
from scipy.stats import *


############# Finding squares #########

def square(list):
    return map(lambda x: x ** 2, list)

#############################################################

############# Generating rv functions #########

def TDTrv(cdf,RV,roundno,UpdateRate,Deadline):

	if(roundno%UpdateRate==0):
		# print cdf[len(cdf)-1]
		x=random.uniform(cdf[len(cdf)-1],cdf[len(cdf)-1]+0.2)
		cdf.append(x)
		y=expon.cdf(x,0,1)
		# print str(x) + " " + str(y)
		# X= truncnorm(0,1)
		# X=truncexpon(1)
		# x= X.rvs(1)
		return float("{0:.4f}".format(y))

	else:
		return RV[len(RV)-1]


#############################################################

############# Generating Utilities according to Boulware #########
def boulwareUtilities (rv,Deadline):
	# print "-----Boulware----------"
	ut = []
	beta = 0.2
	beta = float(1)/beta
	for i in range(1,Deadline+1):
		minm = min(i,Deadline)
		time = float(minm)/Deadline
		curr_ut = rv + (1-rv)*(math.pow(time,beta))
		# print "================"
		# print minm
		# print time
		# print beta
		# print "================"
		ut.append(float("{0:.4f}".format(curr_ut)))
	return ut

#############################################################

############# Generating Utilities according to Tim Barslaab #########

def GenerateTimUtility( rv,rounds):
	# print "-----ONAC-------"
	l=[]
	l.append(rv);
	for i in range(1,rounds):
		l.append(float((l[i-1]+1)*(l[i-1]+1))/4)
	return l

#############################################################


############# Generating random reservation values #########
def generaterandomRV(random_rv,intervals,dif):
	temp1=0
	for i in xrange(0,intervals+1):
		#print (i*float(rv_high-rv_low)/intervals);
		if(i!=0):
			#rv = random.uniform(temp1,(i*float(dif)/intervals))
			rv=temp1+((i*float(dif)/intervals)-temp1)/2
			#print rv
			random_rv.append(float("{0:.4f}".format(rv)))
			temp1=i*float(dif)/intervals;
		#random_rv.append((i*float(rv_high-rv_low)/intervals));

	#print random_rv
#############################################################

#################Generate values from random reservation values#######################
def tempgenerat(i,Deadline,roundnum,RV):
	temp=[0]
	#print str(i) + "  " + str(RV[roundnum-2])
	t1=0	
	b=0
	t=0
	#print str(roundnum) + " " + str(len(RV))
	for roundno in xrange(1,roundnum+1):

		t+=(np.log(float(roundno)/Deadline))*(np.log(float(roundno)/Deadline))

		# if(RV[0]-RV[roundno]==0 or (RV[0]-i)==0):
		# 	print str(RV[0]) + " " + str(RV[roundno]) + " " + str(i) +" " +str(roundno)

		p=np.log ( float(RV[0]-RV[roundno])/ (RV[0]-i) )
		t1=t1+(np.log(float(roundno)/Deadline))*p
		b=float(t1)/t

		# print str(b) + " " + str(t1) + " " + str(t) + " " + str(float(roundno)/Deadline)

		x = RV[0] + (i-RV[0])*(math.pow(float(roundno)/Deadline,b))

		

		x=float("{0:.4f}".format(x))
		temp.append(x)
	return temp

#############################################################

def calculatemeans(temp_offers):
	means=[]
	for i in xrange(0,len(temp_offers)):
		total=0
		for j in xrange(0,len(temp_offers[i])):
			total+=temp_offers[i][j]
		means.append(float(total)/len(temp_offers[i]))
	return means
#############################################################

def getindex(RV,intervals):
	# Utilities=[0.12,0.75]
	# for i in xrange(0,len(Utilities)):
	# 	if(RV==Utilities[i]):
	# 		return i

	low=0
	a=float(1)/intervals
	high=a
	for i in xrange(1,intervals+1):
		if(RV >=low and RV < high ):
			return i-1
		else:
			low=high
			high+=a

############################################################
def getReservationUtility(x):
	if(x<=4):
		return 1
	else:
		y=(1-math.pow(float(x)/12,2)) + 0.01
		return y

def getflag(direction,Gridcoords,GridSize):
	flag=0
	if(direction==1):
		if(Gridcoords[0]!=0):
			Gridcoords[0]-=1                 ### Moving North
		if(Gridcoords[1]==GridSize-1):
			flag=3
		elif(Gridcoords[1]==0):
			flag=2
		elif(Gridcoords[0]+1==GridSize-1):
			flag=4
	elif(direction==2):
		if(Gridcoords[1]!=0):
			Gridcoords[1]-=1                 ### Moving West
		if(Gridcoords[0]==0):
			flag=1
		elif(Gridcoords[1]+1==GridSize-1):
			flag==3
		elif(Gridcoords[0]==GridSize-1):
			flag=4

	elif(direction==3):
		if(Gridcoords[1]!=GridSize-1):
			Gridcoords[1]+=1                 ### Moving East
		if(Gridcoords[0]==GridSize-1):
			flag=4
		elif(Gridcoords[0]==0):
			flag=1
		elif(Gridcoords[1]-1==0):
			flag=2
	else:
		if(Gridcoords[0]!=GridSize-1):
			Gridcoords[0]+=1                 ### Moving South
		if(Gridcoords[0]-1==0):
			flag=1
		elif(Gridcoords[1]==GridSize-1):
			flag=3
		elif(Gridcoords[1]==0):
			flag=2
	return flag
	
#############################################################
def ReservationValues(RV,roundnum,Deadline,UpdateRate,GridSize,Gridcoords):
	ManPower=[12,10,7,4]
	Utilities=[0.75,0.57,0.321,0.12]
	
	if(roundnum==0):
		# print "---round 1: =="
		# direction=random.randint(1,4)    #  ---> 4
		direction=random.choice([1,4])     #  ---> 2
		### Gridcoords Updation 
		flag=getflag(direction,Gridcoords,GridSize)
		# print "------"
		# print direction
		# print Gridcoords
		# print "------"
		if(flag==0 ):
			return Utilities[direction-1]
			#return getReservationUtility(ManPower[direction-1])

		else:	
			# print "This case: "+str(flag) + " "+ str(ManPower[direction-1] )
			# return getReservationUtility( max (ManPower[flag-1], ManPower[direction-1] )) 
			return max (Utilities[flag-1], Utilities[direction-1] )

	elif(roundnum%UpdateRate==0):
		# print "---update == " + str(roundnum)   
		# direction=random.randint(1,4)
		direction=random.choice([1,4])
		flag=getflag(direction,Gridcoords,GridSize)
		# print "------"
		# print direction
		# print Gridcoords
		# print "------"
		if(flag==0 ):
			# return getReservationUtility(ManPower[direction-1])
			return Utilities[direction-1]

		else:	
			# print "This case: "+str(flag) + " "+ str(ManPower[direction-1] )
			# return getReservationUtility( max (ManPower[flag-1], ManPower[direction-1] ) )
			return max (Utilities[flag-1], Utilities[direction-1] )

	else:
		return RV[len(RV)-1]


#############################################################

def getdelayfor4(delay_list,prevdelay):
	p=random.randint(1,5)
	if(p<=2):
		return prevdelay
	elif(p>2 and p<4):
		#increase
		l=[]
		ind=(prevdelay/10)-1
		end=min(ind+1,len(delay_list))
		# print str(ind) + " " + str(end)
		for i in xrange(ind,end):
			l.append(delay_list[i])
		return random.choice(l)
	else:
		#decrease
		l=[]
		ind=(prevdelay/10)-1
		# print ind
		end=max(ind-1,0)
		# print str(end) + " " + str(ind)
		for i in xrange(end,ind+1):
			l.append(delay_list[i])
		return random.choice(l)


def getdelay(delay_list,prevdelay):
	p=random.randint(1,10)
	if(p<=5):
		return prevdelay
	elif(p>5 and p<8):
		#increase
		l=[]
		ind=(prevdelay/5)-1
		end=min(ind+3,len(delay_list))
		# print str(ind) + " " + str(end)
		for i in xrange(ind,end):
			l.append(delay_list[i])
		return random.choice(l)
	else:
		#decrease
		l=[]
		ind=(prevdelay/5)-1
		end=max(ind-3,0)
		# print str(end) + " " + str(ind)
		for i in xrange(end,ind+1):
			l.append(delay_list[i])
		return random.choice(l)

#############################################################

def getmeetingrv(RV,roundnum,UpdateRate,delaylist,Deadline):
	delay_list=[45,40,35,30,25,20,15,10,5]
	# delay_list=[40,30,20,10]
	if(roundnum==0):
		delay=random.choice(delay_list)
		delaylist.append(delay)
		utility=getdelaycost(delay)
		# print str(utility) + " " + str(delay)
		return utility

	elif(roundnum%UpdateRate==0):
		# print "in" 
		delay=getdelay(delay_list,delaylist[len(delaylist)-1])   #### -> 9
		# delay=getdelayfor4(delay_list,delaylist[len(delaylist)-1])    #### -> 4
		delaylist.append(delay)
		# print delay
		utility=getdelaycost(delay)
		# print str(utility) + " "+ str(delay)
		return utility

	else:
		return RV[len(RV)-1]



#############################################################

def getdelaycost(delay):
	
	alpha=1.2
	Value=200
	cost=math.pow(delay,alpha)*2
	maxm=Value-math.pow(5,alpha)*2
	minm=Value-math.pow(45,alpha)*2
	# print str(maxm) + " " + str(minm)
	minm=Value-math.pow(45,alpha)*2
	if(float(Value-cost -minm)/(maxm-minm) ==0):
		return 0.01
	return float("{0:.4f}".format(float(Value-cost -minm)/(maxm-minm)))


#############################################################

def meetingrandomRV(random_rv):
	# print "----- "+str(n)+ "  ---------"
	# delay_list=[5,10,15,20,25,30,35,40,45]
	
	alpha=1.2
	delay_list=[45,40,35,30,25,20,15,10,5]
	# delay_list=[40,30,20,10]
	Value=200
	maxm=Value-math.pow(5,alpha)*2
	minm=Value-math.pow(45,alpha)*2
	for i in xrange(0,len(delay_list)):
		cost=math.pow(delay_list[i],alpha)*2
		u=float(Value-cost -minm)/(maxm-minm)
		if(u==0):
			u=0.01
		random_rv.append(float("{0:.4f}".format(u)))

#############################################################

def getpenalty(BeliefPlots):
	penalty=0
	for i in xrange(0,len(BeliefPlots)):
		for j in xrange(1,len(BeliefPlots[i])):
			penalty+=math.fabs(BeliefPlots[i][j]-BeliefPlots[i][j-1])

	return penalty

#############################################################

def geterror(l,r):
	error=[]
	sums=0
	for i in xrange(0,len(l)):
		sums+=math.pow( (l[i]-r[i]) ,2 )
		# sums=math.fabs(l[i]-r[i])
	error.append(math.sqrt(sums/len(l)))

	return error

def absoldiff(l,r):
	error=[]
	sums=0
	for i in xrange(0,len(l)):
		# sums+=math.pow( (l[i]-r[i]) ,2 )
		sums=math.fabs(l[i]-r[i])
	error.append(math.sqrt(sums))

	return error

#############################################################
def generatereservationvalue(flag,roundnum,RV):
	if(flag==1):
		if(roundnum==1):
		 	return random.choice([0.1,0.2,0.6,0.9])
		elif(roundnum%(50)==0):
			return random.choice([0.1,0.2,0.6,0.9])
		else:
			return RV[len(RV)-1]

	elif(flag==2):
		if(roundnum==1):
		 	return random.choice([0.1,0.2,0.6,0.9])
		elif(roundnum%(20)==0):
			return random.choice([0.1,0.2,0.6,0.9])
		else:
			return RV[len(RV)-1]
	elif(flag==3):
		if(roundnum==1):
		 	return random.choice([0.1,0.2,0.6,0.9])
		elif(roundnum%(10)==0):
			return random.choice([0.1,0.2,0.6,0.9])
		else:
			return RV[len(RV)-1]
	elif(flag==4):
		if(roundnum==1):
		 	return random.choice([0.1,0.2,0.6,0.9])
		elif(roundnum%(5)==0):
			return random.choice([0.1,0.2,0.6,0.9])
		else:
			return RV[len(RV)-1]

	elif(flag==5):
		if(roundnum==1):
		 	return random.choice([0.1,0.2,0.6,0.9])
		elif(roundnum%(2)==0):
			return random.choice([0.1,0.2,0.6,0.9])
		else:
			return RV[len(RV)-1]
		
	elif(flag==6):
		#l=[0.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.6]
		#l=[0.0, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.4]
		l=[  0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.4]
		return l[roundnum-1]

	elif(flag==7):
		l=[0.9,0.1,0.36 ,0.75, 0.75 ,0.12 ,0.75,0.12 ,0.75,0.12]
		# l=[0.2,0.3,0.4,0.5,0.6,0.7]
		return l[(roundnum/2)%2]

###################### Main function #######################################
if __name__ == '__main__':

	#average_belief=[]
	All_UpdateRates = [2]
	for UpdateRate in All_UpdateRates:

		print "------ " + str(UpdateRate)  +  " -------"

		check_lstm=[]

		Average_rv=[]
		AverageUtilities_Tims=[]
		AverageUtilities_Normalised=[]
		AverageUtilities_Counter=[]
		AverageUtilities_Exponential=[]

		# AveragePenalty_Tims=0.0
		# AveragePenalty_Bay =0.0
		# AveragePenalty_Cou =0.0
		# AveragePenalty_Exp =0.0

		# Average_PredictRV_Tims = []
		# Average_PredictRV_bayesian = []
		# Average_PredictRV_counter = []
		# Average_PredictRV_exponential = []

		Average_Diff_Tims=0
		Average_Diff_bayesian =0
		Average_Diff_counter =0
		Average_Diff_exponential =0

		# AverageVar_Tims = 0
		# AverageVar_Bayesian =0
		# AverageVar_Counter =0
		# AverageVar_Exponential=0

		misclassified_BR=0
		misclassified_C =0
		misclassified_E =0

		AverageError_ONAC = 0
		AverageError_Bay  = 0
		AverageError_Cou  = 0
		AverageError_Exp  = 0

		AverageAbsError_ONAC = 0
		AverageAbsError_Bay  = 0
		AverageAbsError_Cou  = 0
		AverageAbsError_Exp  = 0

		check_rv= []
		#counter=1
		for iterations in xrange(1,2):
			# print "------------------------------------------------------------------"
		#	cond=0
			RV=[0]
			mean_RV=0
			Deadline = 100
			rv_low=0 
			rv_high=1
			random_rv=[]
			meetingrandom_rv=[]
			# intervals=4
			# UpdateRate=2
			lastRV=0

			GridSize=20

			# Gridcoords=[GridSize/2 ,GridSize/2]

			Gridcoords=[GridSize/2 +random.choice([-4,0,4]),GridSize/2+random.choice([-4,0,4])]
			
			# print Gridcoords
			


			means_offers=[]
			gamma=[]
			new_gamma=[]
			new_probability=[]
			new_belief_plots=[]

			counter = []
			counter_weights = []
			counter_belief_plots = []
			counter_probabilities = []
			counter_weighted_utility=[]

			exponential=[]
			exponential_weights = []
			exponential_belief_plots = []
			exponential_probabilities = []
			exponential_weighted_utility=[]

			PredictRV_Tims = []
			PredictRV_bayesian = []
			PredictRV_counter = []
			PredictRV_exponential = []

			# rv_bayesian=[]
			# rv_Counter=[]
			# rv_Exponential=[]

			Diff_Tims=0
			Diff_bayesian =0
			Diff_counter =0
			Diff_exponential =0

			# meetingrandomRV(meetingrandom_rv)
			# random_rv=meetingrandom_rv

			# print meetingrandom_rv
			
			# print random_rv
			# generaterandomRV(random_rv,intervals,rv_high-rv_low)
			# random_rv=[0.12,0.321,0.57,0.75]
			random_rv=[0.12,0.75]
			# random_rv=[0.1,0.9]

			intervals = len(random_rv)
			# print intervals

			x=[]
			for i in xrange(1,Deadline+1):
				x.append(i)

			x_belief=[]
			for i in xrange(0,Deadline+1):
				x_belief.append(i)

			for i in xrange(0,intervals):
				gamma.append(0)
				new_gamma.append(0)
				new_belief_plots.append([0])

				counter_belief_plots.append([0])
				counter_weights.append(0)
				counter.append(0)
				counter_probabilities.append(float(1)/intervals)

				exponential_belief_plots.append([0])
				exponential_weights.append(0)
				exponential.append(0)
				exponential_probabilities.append(float(1)/intervals)

				new_probability.append(float("{0:.4f}".format(float(1)/intervals)))
				new_belief_plots[i][0]=new_probability[i]

			

			total=0	
			Utilities=[]
			actual_utility=[]
			new_WeightedUtility=[]
			
			

			Tims_n=0
			Bay_n =0
			Cou_n =0
			Exp_n =0

			# print random_rv
			# break

			for rv in random_rv:
				Utilities.append(GenerateTimUtility(rv,Deadline))     ######   ----> Tims
				# Utilities.append(boulwareUtilities(rv,Deadline))        ######   -----> Boulware

			# print Utilities
			
			# print len(random_rv)
			# print "#############################################################"

			offers=[]
			mean1_RV=0
			delaylist=[]
			cdf=[0]
			for roundnum in xrange(1,Deadline+1):

				# print gaussianrv(roundnum-1,UpdateRate,Deadline)
				
				if(RV[roundnum-1]!=RV[roundnum-2]):
					Tims_n+=1
		
				# if(roundnum==1):
				# RV.append( float( "{0:.4f}".format( ReservationValues(RV,roundnum-1,Deadline,UpdateRate,GridSize,Gridcoords) ) ) )
				# RV.append(TDTrv(cdf,RV,roundnum-1,UpdateRate,Deadline))
				# RV.append(float("{0:.4f}".format( getmeetingrv(RV,roundnum-1,UpdateRate,delaylist,Deadline) ) ) )
				RV.append(float("{0:.4f}".format(generatereservationvalue(7,roundnum,RV)) ))
				# 
				# else:
				# 	RV.append( float( "{0:.4f}".format( ReservationValues(RV,roundnum-1,Deadline,UpdateRate,GridSize,Gridcoords) ) ) )
				# 	# RV.append(float("{0:.4f}".format( getmeetingrv(RV,roundnum-1,UpdateRate,delaylist,Deadline) ) ) )
				# 	# RV.append(float("{0:.4f}".format(generatereservationvalue(7,roundnum-1,RV)) ))
				
				if(RV[roundnum-1]!=lastRV):
					lastRV=RV[roundnum-1]

				

				utility_RV=GenerateTimUtility(RV[roundnum-1],Deadline)              ###### -> Tims
				# utility_RV=boulwareUtilities(RV[roundnum-1],Deadline)             ###### -> Boulware

				temp_offers=[]
				
				# print "--------"
				for i in random_rv:
					
					#print str(i) + "  " + str(RV[0]) + " " +str(roundnum)
					temp_offers.append(tempgenerat(i,Deadline,roundnum,RV))
				
					# offers.append(offers(i,Deadline,roundnum,RV))

				# print temp_offers
				# print "--------"
				mean_RV=np.mean(RV)
				means1=[]
				for i in xrange(0,intervals):
					means1.append(np.mean(temp_offers[i]))

				# if(roundnum%UpdateRate==0):
				# 	print offers[bla]
				offers=temp_offers
				means_offers=means1

				# if(roundnum%UpdateRate==0):
				# 	print offers[bla]
				##################### Calculate Gamma value ####################

				#print "#####################"
				for i in xrange(0,len(offers)):

					variation=0
					d1=0
					d2=0
					for j in xrange(0,len(offers[i])):
						variation += (RV[j] - mean_RV) * (offers[i][j]-means_offers[i])
						d1+=math.pow((RV[j] - mean_RV),2)
						d2+=math.pow((offers[i][j]-means_offers[i]),2)
					denominator=math.sqrt(d1*d2)
					#if(roundnum>=1):
					gamma[i] = float("{0:.4f}".format(float(variation)/denominator))
					new_gamma[i]=float(gamma[i]+1)/2
						
				########################################################" 
				

				##################### Updating weights using Bayesian technique ########################################
			
				#if(roundnum>=1):

				new_total=0
				for i in xrange(0,len(new_probability)):
					new_probability[i]=new_probability[i]*new_gamma[i]
					# print "------"
					# print new_probability[i]
					# print "------"
					new_total+=new_probability[i]
					
					
				for i in xrange(0,len(new_probability)):
					new_probability[i]=float("{0:.4f}".format(new_probability[i]/new_total))
					if(new_probability[i]<=0.0002):
						new_probability[i]=0.0002
					if(new_probability[i]>=0.9998):
						new_probability[i]=0.9998
					new_belief_plots[i].append(new_probability[i])

				########################################################" 


				##################### Counter and Exponential ########################################

				ind=getindex(RV[roundnum],intervals)
				# print RV[roundnum]
				# print ind
				counter[ind]+=1
				# print counter

				total+=1
				for i in xrange(0,len(counter)):
					counter_weights[i]=float(counter[i])/total
					counter_weights[i]=float("{0:.4f}".format(counter_weights[i]))
					counter_belief_plots[i].append(counter_weights[i])
					counter_probabilities[i]=counter_weights[i]

				summation=0
				for i in xrange(0,len(exponential_weights)):
					exponential_weights[i]=math.pow(2,counter[i])
					summation+=exponential_weights[i]

				# print "--------"
				# print exponential_weights
				for i in xrange(0,len(exponential_weights)):
					exponential_weights[i]=float(exponential_weights[i])/summation
					exponential_weights[i]=float("{0:.4f}".format(exponential_weights[i]))
					exponential_belief_plots[i].append(exponential_weights[i])
					exponential_probabilities[i]=exponential_weights[i]

				#############################################################
					
				
				# print counter
				# print summation
				# print "--------"			
				
		
				
				# if(roundnum==Deadline):
				#  	print random_rv	
				# 	print new_probability
				#	print RV
				# print len(Utilities[0])

				##################### Generating Utilites to be bid ########################################

				new_CombinedUtility=0
				for i in xrange(0,len(new_probability)):
					new_CombinedUtility+=new_probability[i]*Utilities[i][len(Utilities[i])-roundnum]
		
				new_WeightedUtility.append(float("{0:.4f}".format(new_CombinedUtility)) )
				actual_utility.append(float("{0:.4f}".format(utility_RV[len(utility_RV)-roundnum])))


				counter_combined_utility=0
				exponential_combined_utility=0
				for i in xrange(0,len(counter_probabilities)):	
					counter_combined_utility+=counter_probabilities[i]*Utilities[i][len(Utilities[i])-roundnum]
					exponential_combined_utility+=exponential_probabilities[i]*Utilities[i][len(Utilities[i])-roundnum]

				counter_weighted_utility.append(float("{0:.4f}".format(counter_combined_utility)) )
				exponential_weighted_utility.append(float("{0:.4f}".format(exponential_combined_utility)) )

				#############################################################

				# print "------------"
				# print "The round number is: "+str(roundnum)
				# print "By using Equation number 9 , x is 0.12: ",
				# print offers[0]
				# print "By using Equation number 9 , x is 0.75: ",
				# print offers[1]
				# print "By using Equation number 11 and 12 ,rv_i is {0.25,0.75} :",
				# print new_gamma
				# print "By using Equation number 13 , H_i is {0.25,0.75}: ",
				# print new_probability
				# print "------------"
				
				# print "******************"
				# print counter
				# print new_probability
				# print counter_probabilities
				# print exponential_probabilities
				# print "******************"

			# print RV
			# plt.plot(RV)
			# plt.show()
			# print geterror(Utilities[getindex(RV[-1],2)],actual_utility)
			# print geterror(Utilities[getindex(RV[-1],2)],new_WeightedUtility)
			# errorUtilities = GenerateTimUtility(RV[-1],Deadline)         ##### ---> Tims
			# # errorUtilities = boulwareUtilities(RV[-1],Deadline)          ##### ---> Boulware
			# errorUtilities = list(reversed(errorUtilities))
			# # print len(errorUtilities)
			# AverageError_ONAC += sum(geterror(errorUtilities,actual_utility))
			# AverageError_Bay  += sum(geterror(errorUtilities,new_WeightedUtility))
			# AverageError_Cou  += sum(geterror(errorUtilities,counter_weighted_utility))
			# AverageError_Exp  += sum(geterror(errorUtilities,exponential_weighted_utility))

			# l= geterror(errorUtilities,actual_utility)
			# r= geterror(errorUtilities,new_WeightedUtility)



			# print (l[-1])
			# print (r[-1])

			# for i in xrange(0,100):
			# 	print str(l[i]) + "   " + str(r[i])  +" --- "+ str(l[i]-r[i])

			# print sum(map(operator.sub,l,r)	)		
			############-------------Calculating Penalties --------##########################
			# print new_belief_plots[0]
			# print new_belief_plots
			# break
			# Bay_n=getpenalty(new_belief_plots)
			# Cou_n=getpenalty(counter_belief_plots)
			# Exp_n=getpenalty(exponential_belief_plots)

			# print len(new_belief_plots)
			# print str(new_belief_plots[0][0]) + " " + str(new_belief_plots[0][1]) + " " + str(new_belief_plots[0][2])
			# lstm=[]
			# for i in xrange(2,len(new_belief_plots[0])):
			# 	for j in xrange(0,len(new_belief_plots)):
			# 		lstm.append(new_belief_plots[j][i])

			# check_lstm.append(lstm)		

			#############################################################################

			#print actual_utility
			#print str(len(new_belief_plots[0])) + " " + str(len(counter_belief_plots[0]) )


			###############-----------Generating Predicted RV and utilities at each round -------- #################

			# print len(new_belief_plots[0])
			# print len(offers[0])
			for i in xrange(0,len(offers[0])):
				prob_bayesian=0
				for j in xrange(0,intervals):
					prob_bayesian+=new_belief_plots[j][i]*offers[j][i]
				PredictRV_bayesian.append(float("{0:.4f}".format(prob_bayesian)))


			for i in xrange(0,len(counter_belief_plots[0])):
				prob_counter=0
				for j in xrange(0,intervals):
					prob_counter+= random_rv[j]*counter_belief_plots[j][i]
				PredictRV_counter.append(float("{0:.4f}".format(prob_counter)))
				# Offers_Counter.append(float("{0:.4f}".format(prob_counter)))

			for i in xrange(0,len(exponential_belief_plots[0])):
				prob_exponential=0
				for j in xrange(0,intervals):
					prob_exponential+=random_rv[j] * exponential_belief_plots[j][i]
				PredictRV_exponential.append(float("{0:.4f}".format(prob_exponential))) 
				# Offers_Exponential.append(float("{0:.4f}".format(prob_exponential))) 

			pred_BR = PredictRV_bayesian[len(PredictRV_bayesian)-1]
			pred_C = PredictRV_counter[len(PredictRV_counter)-1]
			pred_E = PredictRV_exponential[len(PredictRV_exponential)-1]

			######---------- distance metric on an average---########

			# RV=np.array(RV)
			# RV_mean1 = np.mean(RV)
			# RV_mean = 0 
			# for i in xrange(0,len(RV)):
			# 	RV_mean+= i * (RV[i])
			# RV_mean = RV_mean * 1.0 / 5050 
			# # RV_var = np.var(RV)
			# RV_var=0
			# for i in xrange(0,len(RV)):
			# 	RV_var+=math.pow(RV[i] -  RV_mean, 2)

			# RV_var= math.sqrt(RV_var)

			# Bayesian_var=0
			# for i in xrange(0,len(PredictRV_bayesian)):
			# 	Bayesian_var+=math.pow(PredictRV_bayesian[i] -  RV_mean, 2)
				

			# Counter_var=0
			# for i in xrange(0,len(PredictRV_counter)):
			# 	Counter_var+=math.pow(PredictRV_counter[i]-RV_mean,2)

			# Exponential_var=0
			# for i in xrange(0,len(PredictRV_exponential)):
			# 	Exponential_var+=math.pow(PredictRV_exponential[i]-RV_mean,2)
				

			# Bayesian_var = math.sqrt(Bayesian_var)
			# Counter_var = math.sqrt(Counter_var)
			# Exponential_var = math.sqrt(Exponential_var)

			# print "prev: "+ str(RV[len(RV)-2])
			# nextRV = float( "{0:.4f}".format(TDTrv(cdf,RV,roundnum,UpdateRate,Deadline) ))
			nextRV = float( "{0:.4f}".format( ReservationValues(RV,Deadline,Deadline,UpdateRate,GridSize,Gridcoords) ) )
			 
			# nextRV =float("{0:.4f}".format( getmeetingrv(RV,Deadline,UpdateRate,delaylist,Deadline) ) ) 
			# nextRV =float("{0:.4f}".format(generatereservationvalue(7,roundnum-1,RV)) ) 
			# print "next: " + str(nextRV)
			# check_rv.append(nextRV)

			# print getindex(nextRV,intervals)
			# print str(pred_BR)+ " " + str(getindex(pred_BR,intervals))
			# print str(pred_C)+ " " + str(getindex(pred_C,intervals))
			# print str(pred_E)+ " " + str(getindex(pred_E,intervals))

			if(getindex(nextRV,intervals)!=getindex(pred_BR,intervals)):
				misclassified_BR = misclassified_BR + 1

			if(getindex(nextRV,intervals)!=getindex(pred_C,intervals)):
				misclassified_C = misclassified_C + 1

			if(getindex(nextRV,intervals)!=getindex(pred_E,intervals)):
				misclassified_E = misclassified_E + 1

			errorUtilities = GenerateTimUtility(nextRV,Deadline)         ##### ---> Tims
			# errorUtilities = boulwareUtilities(nextRV,Deadline)          ##### ---> Boulware
			errorUtilities=list(reversed(errorUtilities))
			# print errorUtilities
			# print len(geterror(errorUtilities,actual_utility))
			# break
			AverageError_ONAC += sum(geterror(errorUtilities,actual_utility))
			AverageError_Bay  += sum(geterror(errorUtilities,new_WeightedUtility))
			AverageError_Cou  += sum(geterror(errorUtilities,counter_weighted_utility))
			AverageError_Exp  += sum(geterror(errorUtilities,exponential_weighted_utility))

			
			AverageAbsError_ONAC += sum(absoldiff(errorUtilities,actual_utility))
			AverageAbsError_Bay  += sum(absoldiff(errorUtilities,new_WeightedUtility))
			AverageAbsError_Cou  += sum(absoldiff(errorUtilities,counter_weighted_utility))
			AverageAbsError_Exp  += sum(absoldiff(errorUtilities,exponential_weighted_utility))

			# print errorUtilities
			
			

			# # DT=[]
			# # for i in xrange(0,len(RV)):
			# # 	DT.append(math.fabs(RV[i]))
			Diff_Tims = math.fabs(RV[-1]-nextRV)

			Average_Diff_Tims += Diff_Tims

			# print Diff_Tims

			# # DB=[]
			# # for i in xrange(0,len(PredictRV_bayesian)):
			# # 	DB.append(math.fabs(PredictRV_bayesian[i]))
			# Diff_bayesian = math.fabs(PredictRV_bayesian[len(PredictRV_bayesian)-1]-nextRV)

			# # DC=[]
			# # for i in xrange(0,len(PredictRV_counter)):
			# # 	DC.append(math.fabs(PredictRV_counter[i]))
			# Diff_counter = math.fabs(PredictRV_counter[len(PredictRV_counter)-1]-nextRV)
			# # DE=[]
			# # for i in xrange(0,len(PredictRV_exponential)):
			# # 	DE.append(math.fabs(PredictRV_exponential[i]))
			# Diff_exponential = math.fabs(PredictRV_exponential[len(PredictRV_exponential)-1]-nextRV)

			

			# print PredictRV_bayesian[len(PredictRV_bayesian)-1]
			# print PredictRV_counter[len(PredictRV_counter)-1]
			# print PredictRV_exponential[len(PredictRV_exponential)-1]

			# print '----------'
			# print Diff_Tims
			# print Diff_bayesian
			# print Diff_counter
			# print Diff_exponential
			# print '----------'


			if(iterations==1):
				Average_rv=RV
				AverageUtilities_Tims=actual_utility
				AverageUtilities_Normalised=new_WeightedUtility
				AverageUtilities_Counter=counter_weighted_utility
				AverageUtilities_Exponential=exponential_weighted_utility

				# print AverageUtilities_Tims
				# print AverageUtilities_Normalised


				# AveragePenalty_Tims+=Tims_n
				# AveragePenalty_Bay+=Bay_n
				# AveragePenalty_Cou+=Cou_n
				# AveragePenalty_Exp+=Exp_n

				# Average_Diff_Tims=Diff_Tims
				# Average_Diff_bayesian = Diff_bayesian
				# Average_Diff_counter = Diff_counter
				# Average_Diff_exponential = Diff_exponential

				# AverageVar_Tims = RV_var
				# AverageVar_Bayesian = Bayesian_var
				# AverageVar_Counter = Counter_var
				# AverageVar_Exponential= Exponential_var

				
			else:
				#print iterations-1
				Average_rv=np.array(Average_rv,dtype=float)*(iterations-1)
				AverageUtilities_Tims=np.array(AverageUtilities_Tims,dtype=float)*(iterations-1)
				AverageUtilities_Normalised=np.array(AverageUtilities_Normalised,dtype=float)*(iterations-1)
				AverageUtilities_Counter=np.array(AverageUtilities_Counter,dtype=float)*(iterations-1)
				AverageUtilities_Exponential=np.array(AverageUtilities_Exponential,dtype=float)*(iterations-1)
				# AveragePenalty_Tims=AveragePenalty_Tims*(iterations-1)
				# AveragePenalty_Bay=AveragePenalty_Bay*(iterations-1)
				# AveragePenalty_Cou=AveragePenalty_Cou*(iterations-1)
				# AveragePenalty_Exp=AveragePenalty_Exp*(iterations-1)
				# Average_Diff_Tims=Average_Diff_Tims * (iterations-1)
				# Average_Diff_bayesian=Average_Diff_bayesian * (iterations-1)
				# Average_Diff_counter=Average_Diff_counter *(iterations-1)
				# Average_Diff_exponential=Average_Diff_exponential *(iterations-1)
				# AverageVar_Tims=AverageVar_Tims*(iterations-1)
				# AverageVar_Bayesian=AverageVar_Bayesian*(iterations-1)
				# AverageVar_Counter=AverageVar_Counter*(iterations-1)
				# AverageVar_Exponential=AverageVar_Exponential*(iterations-1)


				Average_rv=map(operator.add,Average_rv,RV)
				AverageUtilities_Tims=map(operator.add,AverageUtilities_Tims,actual_utility)
				AverageUtilities_Normalised=map(operator.add,AverageUtilities_Normalised,new_WeightedUtility)
				AverageUtilities_Counter=map(operator.add,AverageUtilities_Counter,counter_weighted_utility)
				AverageUtilities_Exponential=map(operator.add,AverageUtilities_Exponential,exponential_weighted_utility)	
				# AveragePenalty_Tims+=Tims_n
				# AveragePenalty_Bay+=Bay_n
				# AveragePenalty_Cou+=Cou_n
				# AveragePenalty_Exp+=Exp_n
				# Average_Diff_Tims+=Diff_Tims 
				# Average_Diff_bayesian+=Diff_bayesian 
				# Average_Diff_counter+=Diff_counter 
				# Average_Diff_exponential+=Diff_exponential
				# AverageVar_Tims+=RV_var
				# AverageVar_Bayesian+=Bayesian_var
				# AverageVar_Counter+=Counter_var 
				# AverageVar_Exponential+=Exponential_var


									
				Average_rv=np.array(Average_rv)/iterations
				AverageUtilities_Tims=np.array(AverageUtilities_Tims)/iterations
				AverageUtilities_Normalised=np.array(AverageUtilities_Normalised)/iterations
				AverageUtilities_Counter=np.array(AverageUtilities_Counter)/iterations
				AverageUtilities_Exponential=np.array(AverageUtilities_Exponential)/iterations
				# AveragePenalty_Tims=AveragePenalty_Tims/iterations
				# AveragePenalty_Bay=AveragePenalty_Bay/iterations
				# AveragePenalty_Cou=AveragePenalty_Cou/iterations
				# AveragePenalty_Exp=AveragePenalty_Exp/iterations
				# Average_Diff_Tims=Average_Diff_Tims /(iterations)
				# Average_Diff_bayesian=Average_Diff_bayesian / (iterations)
				# Average_Diff_counter=Average_Diff_counter /(iterations)
				# Average_Diff_exponential=Average_Diff_exponential /(iterations)
				# AverageVar_Tims = AverageVar_Tims/(iterations)
				# AverageVar_Bayesian= AverageVar_Bayesian/(iterations)
				# AverageVar_Counter=AverageVar_Counter/(iterations)
				# AverageVar_Exponential=AverageVar_Exponential/(iterations)


				#counter+=1
			# print lastRV
			# print RV
			# print new_belief_plots
			# print  str(iterations)

			# print PredictRV_bayesian[len(PredictRV_bayesian)-1]
			# print PredictRV_counter[len(PredictRV_counter)-1]
			# print PredictRV_exponential[len(PredictRV_exponential)-1]



		# with open('last_valmeet_2.txt','w') as fd:
		# 	fd.write(str(check_rv))
		# check_lstm=np.array(check_lstm)
		# with open('pred_fire2.npy','wb') as pr: 
		# 	np.save(pr,check_lstm ) 
	 	# print len(check_lstm)
	 	# print len(new_belief_plots)
	 	# print len(new_belief_plots[0])
	 	lstm_belief=[]
	 	l1=[0.5,0.5,0.6666666666666666, 0.75, 0.8, 0.8333333333333334, 0.8571428571428571, 0.875, 0.8888888888888888, 0.9, 0.9090909090909091, 0.9166666666666666, 0.9230769230769231, 0.9285714285714286, 0.9333333333333333, 0.9375, 0.9411764705882353, 0.9444444444444444, 0.9473684210526315, 0.95, 0.9523809523809523, 0.9545454545454546, 0.9565217391304348, 0.9583333333333334, 0.96, 0.9615384615384616, 0.9629629629629629, 0.9642857142857143, 0.9655172413793104, 0.9666666666666667, 0.967741935483871, 0.96875, 0.9696969696969697, 0.9705882352941176, 0.9714285714285714, 0.9722222222222222, 0.972972972972973, 0.9736842105263158, 0.9743589743589743, 0.975, 0.975609756097561, 0.9761904761904762, 0.9767441860465116, 0.9772727272727273, 0.9777777777777777, 0.9782608695652174, 0.9787234042553191, 0.9791666666666666, 0.9795918367346939, 0.98, 0.9803921568627451, 0.9807692307692307, 0.9811320754716981, 0.9814814814814815, 0.9818181818181818, 0.9821428571428571, 0.9824561403508771, 0.9827586206896551, 0.9830508474576272, 0.9833333333333333, 0.9836065573770492, 0.9838709677419355, 0.9841269841269841, 0.984375, 0.9846153846153847, 0.9848484848484849, 0.9850746268656716, 0.9852941176470589, 0.9855072463768116, 0.9857142857142858, 0.9859154929577465, 0.9861111111111112, 0.9863013698630136, 0.9864864864864865, 0.9866666666666667, 0.9868421052631579, 0.987012987012987, 0.9871794871794872, 0.9873417721518988, 0.9875, 0.9876543209876543, 0.9878048780487805, 0.9879518072289156, 0.9880952380952381, 0.9882352941176471, 0.9883720930232558, 0.9885057471264368, 0.9886363636363636, 0.9887640449438202, 0.9888888888888889, 0.989010989010989, 0.9891304347826086, 0.989247311827957, 0.9893617021276596, 0.9894736842105263, 0.9895833333333334, 0.9896907216494846, 0.9897959183673469, 0.98989898989899, 0.99, 0.9900990099009901]
	 	
	 	l2=[0.5,0.5,0.3333333333333333, 0.25, 0.2, 0.16666666666666666, 0.14285714285714285, 0.125, 0.1111111111111111, 0.1, 0.09090909090909091, 0.08333333333333333, 0.07692307692307693, 0.07142857142857142, 0.06666666666666667, 0.0625, 0.058823529411764705, 0.05555555555555555, 0.05263157894736842, 0.05, 0.047619047619047616, 0.045454545454545456, 0.043478260869565216, 0.041666666666666664, 0.04, 0.038461538461538464, 0.037037037037037035, 0.03571428571428571, 0.034482758620689655, 0.03333333333333333, 0.03225806451612903, 0.03125, 0.030303030303030304, 0.029411764705882353, 0.02857142857142857, 0.027777777777777776, 0.02702702702702703, 0.02631578947368421, 0.02564102564102564, 0.025, 0.024390243902439025, 0.023809523809523808, 0.023255813953488372, 0.022727272727272728, 0.022222222222222223, 0.021739130434782608, 0.02127659574468085, 0.020833333333333332, 0.02040816326530612, 0.02, 0.0196078431372549, 0.019230769230769232, 0.018867924528301886, 0.018518518518518517, 0.01818181818181818, 0.017857142857142856, 0.017543859649122806, 0.017241379310344827, 0.01694915254237288, 0.016666666666666666, 0.01639344262295082, 0.016129032258064516, 0.015873015873015872, 0.015625, 0.015384615384615385, 0.015151515151515152, 0.014925373134328358, 0.014705882352941176, 0.014492753623188406, 0.014285714285714285, 0.014084507042253521, 0.013888888888888888, 0.0136986301369863, 0.013513513513513514, 0.013333333333333334, 0.013157894736842105, 0.012987012987012988, 0.01282051282051282, 0.012658227848101266, 0.0125, 0.012345679012345678, 0.012195121951219513, 0.012048192771084338, 0.011904761904761904, 0.011764705882352941, 0.011627906976744186, 0.011494252873563218, 0.011363636363636364, 0.011235955056179775, 0.011111111111111112, 0.01098901098901099, 0.010869565217391304, 0.010752688172043012, 0.010638297872340425, 0.010526315789473684, 0.010416666666666666, 0.010309278350515464, 0.01020408163265306, 0.010101010101010102, 0.01, 0.009900990099009901]
	 	lstm_belief.append(l1)
	 	lstm_belief.append(l2)
	 	# print len(lstm_belief[0])
	    
	    # print lstm_belief

	    ################------------ Belief Update -------------###########

		for i in xrange(0,intervals):
			if(i==0):
				plt.figure('Belief Plots 1')
				plt.title('Belief Plot 1',fontsize=20, fontweight='bold')

				# print len(x)
				# print len(new_belief_plots[i])
				Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=2, markersize=10)
				BP1_bay,=plt.plot(x_belief,new_belief_plots[i], linestyle='-', color='k', linewidth=1.5)
				BP1_con,=plt.plot(x_belief,counter_belief_plots[i], linestyle='--', color='g', linewidth=1.5)
				# BP1_exp,=plt.plot(x_belief,exponential_belief_plots[i], marker='^',linestyle=':', color='b', linewidth=1.5)
				BP1_lst,=plt.plot(x_belief,lstm_belief[i], marker='*',linestyle='--', color='m', linewidth=1.5)

				plt.yticks(fontsize=20,fontweight='bold')
				plt.xticks(fontsize=20,fontweight='bold')
				plt.plot(RV,'ro')
				plt.legend([Res,BP1_bay,BP1_con,BP1_lst],["RV's Utilities","Bayesian","Counter","LSTM"],loc=4,ncol=1, handlelength=4)
				# plt.legend([Res,BP1_bay,BP1_con,BP1_exp,BP1_lst],["Reservation Utilities","Bayesian","Counter","Exponential","LSTM"],loc=4,ncol=2, handlelength=4)
				# plt.plot(new_belief_plots[i],'k--',counter_belief_plots[i],'r--',exponential_belief_plots[i],'g--')
				plt.xlabel('Rounds',fontsize=20, fontweight='bold')
				plt.ylabel('Probabilities',fontsize=20, fontweight='bold')
				plt.savefig('firePlots1.pdf',format='pdf', dpi=1000)
			else:
				plt.figure('Belief Plots 2')
				plt.title('Belief Plot 2',fontsize=20, fontweight='bold')
				Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', markersize=10)
				BP1_bay,=plt.plot(x_belief,new_belief_plots[i], linestyle='-', color='k', linewidth=3.5)
				BP1_con,=plt.plot(x_belief,counter_belief_plots[i], linestyle='--', color='g', linewidth=1.5)
				# BP1_exp,=plt.plot(x_belief,exponential_belief_plots[i],marker='^' ,linestyle=':', color='b', linewidth=3.5)
				BP1_lst,=plt.plot(x_belief,lstm_belief[i], marker='*',linestyle='--', color='m', linewidth=1.5)
				
				plt.yticks(fontsize=20,fontweight='bold')
				plt.xticks(fontsize=20,fontweight='bold')
				# plt.plot(RV,'ro')
				# plt.plot(new_belief_plots[i],'k--',counter_belief_plots[i],'r--',exponential_belief_plots[i],'g--')
				# plt.legend([Res,BP1_bay,BP1_con,BP1_exp],["Reservation Utilities","Bayesian","Counter","Exponential"],loc=2,ncol=4, handlelength=4)
				plt.xlabel('Rounds',fontsize=20, fontweight='bold')
				plt.ylabel('Probabilities',fontsize=20, fontweight='bold')
				plt.savefig('firePlots2.pdf',format='pdf', dpi=1000)


		# errorUtilities = GenerateTimUtility(Average_rv[-1],Deadline)         ##### ---> Tims
		# # errorUtilities = boulwareUtilities(Average_rv[-1],Deadline)          ##### ---> Boulware
		# errorUtilities = list(reversed(errorUtilities))
		# AverageError_ONAC += sum(geterror(errorUtilities,AverageUtilities_Tims))
		# AverageError_Bay  += sum(geterror(errorUtilities,AverageUtilities_Normalised))
		# AverageError_Cou  += sum(geterror(errorUtilities,AverageUtilities_Counter))
		# AverageError_Exp  += sum(geterror(errorUtilities,AverageUtilities_Exponential))

		# chec12 = GenerateTimUtility(0.12,Deadline)
		# chec75 = GenerateTimUtility(0.75,Deadline)

		# print sum(geterror(chec12,chec75))

		# print iterations
		# print RV
		print "---ssr---"
		print "avg diff in rv: " + str(Average_Diff_Tims) 
		print AverageError_ONAC / iterations
		print AverageError_Bay  / iterations
		print AverageError_Cou  / iterations
		print AverageError_Exp  / iterations


				
		# print "--abs dif---"
		# print AverageAbsError_ONAC /iterations
		# print AverageAbsError_Bay /iterations
		# print AverageAbsError_Cou  /iterations
		# print AverageAbsError_Exp/iterations


		#print offers
		TimsError=0
		NormalisedError=0

		counter_weights_error=0
		exponential_weights_error=0

		for i in xrange(2,19):
			Tims_fit=np.polyfit(x,AverageUtilities_Tims,i,full=True)
			Normalised_fit=np.polyfit(x,AverageUtilities_Normalised,i,full=True)
			counter_Generated_fit=np.polyfit(x,AverageUtilities_Counter,i,full=True)
			exponential_Generated_fit=np.polyfit(x,AverageUtilities_Exponential,i,full=True)


			if(i==18):
				TimsError=Tims_fit[1]
				NormalisedError=Normalised_fit[1]
				counter_weights_error=counter_Generated_fit[1]
				exponential_weights_error=exponential_Generated_fit[1]

				Tims_index=i
				Normalised_index=i
				counter_weights_index=i
				exponential_weights_index=i

			else:
				if(Tims_fit[1]<TimsError):
					TimsError=Tims_fit[1]
					Tims_index=i
				if(Normalised_fit[1]<NormalisedError):
					NormalisedError=Normalised_fit[1]
					Normalised_index=i
				if(counter_Generated_fit[1]<counter_weights_error):
					counter_weights_error=counter_Generated_fit[1]	
					counter_weights_index=i
				if(exponential_Generated_fit[1]<exponential_weights_error):
					exponential_weights_error=exponential_Generated_fit[1]	
					exponential_weights_index=i

			# print Tims_fit[1]
			# print Normalised_fit[1]
			# print counter_Generated_fit[1]
			# print exponential_Generated_fit[1]


		# print AverageUtilities_Tims
		# print AverageUtilities_Normalised
		# print counter_weights_index
		# print exponential_weights_index

		

		# ############----------Prediction Plots---------############
		# lstm_utilities=[0.967, 0.9652, 0.9641, 0.9633, 0.9627, 0.9621, 0.9615, 0.961, 0.9605, 0.96, 0.9595, 0.959, 0.9585, 0.958, 0.9575, 0.957, 0.9565, 0.956, 0.9555, 0.9549, 0.9544, 0.9538, 0.9532, 0.9526, 0.9521, 0.9514, 0.9508, 0.9502, 0.9495, 0.9488, 0.9482, 0.9474, 0.9467, 0.946, 0.9452, 0.9444, 0.9436, 0.9428, 0.9419, 0.941, 0.9401, 0.9392, 0.9382, 0.9372, 0.9362, 0.9351, 0.934, 0.9329, 0.9317, 0.9305, 0.9292, 0.9279, 0.9265, 0.9251, 0.9237, 0.9221, 0.9205, 0.9189, 0.9172, 0.9153, 0.9135, 0.9115, 0.9094, 0.9072, 0.905, 0.9026, 0.9001, 0.8974, 0.8946, 0.8917, 0.8885, 0.8852, 0.8817, 0.878, 0.874, 0.8697, 0.8651, 0.8602, 0.8549, 0.8492, 0.843, 0.8363, 0.8289, 0.8208, 0.8119, 0.8021, 0.7911, 0.7788, 0.7648, 0.749, 0.7308, 0.7095, 0.6845, 0.6544, 0.6176, 0.5713, 0.5111, 0.429, 0.3085, 0.1079]
		
		# AvgONAC = GenerateTimUtility(Average_rv[-1],Deadline)

		# legend_properties = {'weight':'bold', 'size':20}

		# plt.figure("errors")


		# Res,=plt.plot(x_belief,Average_rv, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
		# Tim,=plt.plot(x,AverageUtilities_Tims, linestyle='-', color='k', linewidth=1.5)
		# Bay,=plt.plot(x,AverageUtilities_Normalised, linestyle='-', color='g', linewidth=1.5)
		# plt.legend([Tim,Bay],["ONAC","Bayesian"],loc=0,ncol=1, handlelength=4,prop=legend_properties)
		# plt.show()


		# print len(x)
		# print len(lstm_utilities)
		
		# plt.figure('Prediction')
		# # DiffT,=plt.plot(x,DT, linestyle='-', color='k', linewidth=1.5)
		# # DiffB,=plt.plot(x,DB, linestyle='-', color='r', linewidth=1.5)
		# # DiffC,=plt.plot(x,DC, linestyle='-', color='b', linewidth=1.5)
		# # DiffE,=plt.plot(x,DE, linestyle='-', color='g', linewidth=1.5)
		# # plt.legend([DiffT,DiffB,DiffC,DiffE],["ONAC","Bayesian","Counter",Exponential],loc=6,ncol=1, handlelength=4,prop=legend_properties)
		# plt.plot(DT,'r')
		# plt.plot(DB,'k')
		# plt.plot(DC,'g')
		# plt.plot(DE,'b')
		# plt.show()

		# plt.figure('Error Utilities')
		# # plt.plot(errorUtilities,'r')
		# # plt.plot(actual_utility,'k')
		# # plt.plot(new_WeightedUtility,'g')

		# DiffT,=plt.plot(x,errorUtilities, linestyle='-', color='k', linewidth=1.5)
		# DiffB,=plt.plot(x,actual_utility, linestyle='-', color='r', linewidth=1.5)
		# DiffC,=plt.plot(x,new_WeightedUtility, linestyle='-', color='b', linewidth=1.5)
		# # DiffE,=plt.plot(x,DE, linestyle='-', color='g', linewidth=1.5)
		# plt.legend([DiffT,DiffB,DiffC],["ONAC-S","ONAC-D","ONAC-Bay"],loc=6,ncol=1, handlelength=4,prop=legend_properties)

		# # plt.plot(DE,'b')
		# plt.show()

		###################-----------------###################

		# # # # print str(np.mean(AverageUtilities_Tims)) + " " + str(len(AverageUtilities_Tims))
		# # # # print str(np.mean(AverageUtilities_Normalised)) + " " + str(len(AverageUtilities_Normalised))
		# # # # print str(np.mean(AverageUtilities_Counter)) + " " + str(len(AverageUtilities_Counter))
		# # # # print str(np.mean(AverageUtilities_Exponential)) + " " + str(len(AverageUtilities_Exponential))

		# plt.figure('LSTM Utilities')
		# # plt.title('LSTM Utilities',fontsize=20, fontweight='bold')
		# coefs = poly.polyfit(x, lstm_utilities, 10)
		# ffit = poly.polyval(x,coefs)
		# Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
		# Tim,=plt.plot(x,lstm_utilities, linestyle='-', color='k', linewidth=1.5)
		# Timfit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=2.5)
		# plt.yticks(fontsize=20,fontweight='bold')
		# plt.xticks(fontsize=20,fontweight='bold')
		# plt.legend([Res,Tim,Timfit],["Reservation Utilities","LSTM's Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
		# # plt.legend([Res,Tim],["Reservation Utilities","ONAC's Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
		# plt.xlabel('Rounds',fontsize=20, fontweight='bold')
		# plt.ylabel('Utilities',fontsize=20, fontweight='bold')
		# plt.savefig('lstm.pdf',format='pdf', dpi=1000)

		# plt.figure('AverageUtilities Tims')
		# plt.title('ONAC Utilities',fontsize=20, fontweight='bold')
		# coefs = poly.polyfit(x, AverageUtilities_Tims, Tims_index)
		# ffit = poly.polyval(x,coefs)
		# Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
		# Tim,=plt.plot(x,AverageUtilities_Tims, linestyle='-', color='k', linewidth=1.5)
		# Timfit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=2.5)
		# plt.yticks(fontsize=20,fontweight='bold')
		# plt.xticks(fontsize=20,fontweight='bold')
		# plt.legend([Res,Tim,Timfit],["Reservation Utilities","ONAC's Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
		# # plt.legend([Res,Tim],["Reservation Utilities","ONAC's Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
		# plt.xlabel('Rounds',fontsize=20, fontweight='bold')
		# plt.ylabel('Utilities',fontsize=20, fontweight='bold')
		# # plt.savefig('tim.pdf',format='pdf', dpi=1000)

		# # plt.plot(Average_rv,'ro')
		# # plt.plot(AverageUtilities_Tims,'r--')
		# # plt.plot(AverageUtilities_Tims,'r--',ffit,'g--')
		# # print np.polyfit(x,AverageUtilities_Tims,5,full=True)[1]
		
		# plt.figure('AverageUtilities Bayesian')
		# plt.title('Bayesian Learning',fontsize=20, fontweight='bold')
		# coefs=poly.polyfit(x,AverageUtilities_Normalised,Normalised_index)
		# ffit=poly.polyval(x,coefs)

		# Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
		# Bay,=plt.plot(x,AverageUtilities_Normalised, linestyle='-', color='k', linewidth=1.5)
		# Bayfit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=3.5)
		# plt.legend([Res,Bay,Bayfit],["Reservation Utilities","Bayesian Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)

		# plt.yticks(fontsize=20,fontweight='bold')
		# plt.xticks(fontsize=20,fontweight='bold')
		# # plt.plot(Average_rv,'ro')
		# # plt.plot(AverageUtilities_Normalised,'r--',ffit,'g--')
		# plt.xlabel('Rounds',fontsize=20, fontweight='bold')
		# plt.ylabel('Utilities',fontsize=20, fontweight='bold')
		# # plt.savefig('normalised.pdf',format='pdf', dpi=1000)
		# # # # # #print np.polyfit(x,AverageUtilities_Tims,5,full=True)[1]
		# # # # # #print np.polyfit(x,AverageUtilities_Normalised,5,full=True)[1]
		
		# plt.figure('AverageUtilities_Counter')
		# plt.title('Counter Learning',fontsize=20, fontweight='bold')
		
		# y=counter_weighted_utility
		# coefs = poly.polyfit(x, AverageUtilities_Counter, counter_weights_index)
		# ffit = poly.polyval(x,coefs)


		# Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
		# Con,=plt.plot(x,AverageUtilities_Counter, linestyle='-', color='k', linewidth=1.5)
		# Confit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=3.5)
		# plt.legend([Res,Con,Confit],["Reservation Utilities","Counter Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)

		# plt.yticks(fontsize=20,fontweight='bold')
		# plt.xticks(fontsize=20,fontweight='bold')
		# # plt.plot(Average_rv,'ro')
		# # plt.plot(x,ffit,'g--')
		# # plt.plot(x,AverageUtilities_Counter,'r--')
		# plt.xlabel('Rounds',fontsize=20, fontweight='bold')
		# plt.ylabel('Utilities',fontsize=20, fontweight='bold')
		# # plt.savefig('counter.pdf',format='pdf', dpi=1000)
		
		# plt.figure('AverageUtilities_Exponential')
		# plt.title('Exponential Learning',fontsize=20, fontweight='bold')
		
		# y=exponential_weighted_utility
		# coefs = poly.polyfit(x, AverageUtilities_Exponential, exponential_weights_index)
		# ffit = poly.polyval(x,coefs)
		
		# Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
		# Exp,=plt.plot(x,AverageUtilities_Exponential, linestyle='-', color='k', linewidth=1.5)
		# Expfit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=3.5)
		# plt.legend([Res,Exp,Expfit],["Reservation Utilities","Exponential Utilities","Fitted Utilities"],loc=0,ncol=1, handlelength=4,prop=legend_properties)
		# plt.yticks(fontsize=20,fontweight='bold')
		# plt.xticks(fontsize=20,fontweight='bold')
		# # plt.plot(Average_rv,'ro')
		# # plt.plot(x,ffit,'g--')
		# # plt.plot(x,AverageUtilities_Exponential,'r--')
		# plt.xlabel('Rounds',fontsize=20, fontweight='bold')
		# plt.ylabel('Utilities',fontsize=20, fontweight='bold')
		# # plt.savefig('exponential.pdf',format='pdf', dpi=1000)

		# plt.figure('Averages')
		# # plt.title('Averages Utilities generated by each algorithm',fontsize=18, fontweight='bold')

		# Res,=plt.plot(x_belief,RV, marker='o',linestyle='', color='r', linewidth=1.5,markersize=8)
		# Tim,=plt.plot(x,AverageUtilities_Tims, marker ='*',linestyle='-.', color='m', linewidth=2.5,markersize=4)
		# Bay,=plt.plot(x,AverageUtilities_Normalised, linestyle='--', color='k', linewidth=1.5)
		# Con,=plt.plot(x,AverageUtilities_Counter, linestyle='-', color='g', linewidth=1.5)
		# Exp,=plt.plot(x,AverageUtilities_Exponential ,linestyle=':', color='b', linewidth=3.5)
		# LSTM,=plt.plot(x,lstm_utilities,linestyle='-.' , color='#A52A2A', linewidth=1.5)

		# plt.legend([Res,Tim,Bay,Con,Exp,LSTM],["Reservation Utilities","ONAC Utilities","Bayesian Utilities","Counter Utilities","Exponential Utilities","LSTM Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
		# plt.yticks(fontsize=20,fontweight='bold')
		# plt.xticks(fontsize=20,fontweight='bold')
		# # plt.plot(Average_rv,'ro')
		# # plt.plot(AverageUtilities_Tims,'k--',AverageUtilities_Normalised,'r--',AverageUtilities_Counter,'b--',AverageUtilities_Exponential,'g--')
		# # plt.plot(AverageUtilities_Normalised,'r--',AverageUtilities_Counter,'b--',AverageUtilities_Exponential,'g--')
		# plt.xlabel('Rounds',fontsize=20, fontweight='bold')
		# plt.ylabel('Utilities',fontsize=20, fontweight='bold')
		# plt.savefig('averages.pdf',format='pdf', dpi=1000)

		# print '######################'
		# print "Misclassification"
		
		# print misclassified_BR
		# print misclassified_C
		# print misclassified_E
		# print '#################'

		# print "-----"
		# print "difference"
		# # print str(len(RV)) + " "  + str(len(PredictRV_exponential))
		# print Average_Diff_Tims 
		# print Average_Diff_bayesian
		# print Average_Diff_counter
		# print Average_Diff_exponential
		# print "-----"
		
		# print "----------"
		# print AveragePenalty_Tims
		# print AveragePenalty_Bay 	
		# print AveragePenalty_Cou
		# print AveragePenalty_Exp
		# print "----------"

		# # print '***********************'
		# # print "Variance"
		# # print AverageVar_Tims
		# # print AverageVar_Bayesian
		# # print AverageVar_Counter
		# # print AverageVar_Exponential
		# # print '***********************'

		# print '######################'
		# print "Smoothness"
		# print TimsError
		# print NormalisedError
		# print counter_weights_error
		# print exponential_weights_error
		# print '######################'
		
		# plt.show()
	
	

