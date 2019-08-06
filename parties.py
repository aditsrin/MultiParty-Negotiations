import random
import math
import numpy as np
class Party:
    '''This is Party Class'''
    def __init__(self,name,deadline):
        self.name = name
        self.utilityspace = {}
        self.response = ["Yes","No"]
        self.rv = 0.0
        self.deadline = deadline
        self.rvlist = [0.12,0.321,0.57,0.75]
        self.flag = 1
        self.roundrvlist = []
        self.means_offers=[]
        self.gamma=[0]*len(self.rvlist)
        self.new_gamma=[0]*len(self.rvlist)
        self.bayesianutilitylist = []
        self.strategy = "boulware"
    def checkupdate(self,updateflag,rounds,updaterate):
        if(updateflag==False):
            return
        else:
            #print(updateflag,updaterate,rounds)
            if(rounds==1):
                self.rv = random.choice(self.rvlist)
            else:
                if(self.flag==1):
                    prob = random.randint(1,4)
                    if(prob < 4):
                        cur_pos = self.rvlist.index(self.rv)
                        if(cur_pos < len(self.rvlist)-1 ):
                            if(len(self.rvlist[cur_pos+1:]) > 0):
                                self.rv = random.choice(self.rvlist[cur_pos+1:])
                    else:
                        cur_pos = self.rvlist.index(self.rv)
                        if(len(self.rvlist[:cur_pos])>0):
                            self.rv = random.choice(self.rvlist[:cur_pos])
                        self.flag = -1
                elif(self.flag == -1):
                    prob = random.randint(1,4)
                    if(prob < 4):
                        cur_pos = self.rvlist.index(self.rv)
                        if(cur_pos > 0):
                            if(len(self.rvlist[:cur_pos])>0):
                                self.rv = random.choice(self.rvlist[:cur_pos])
                    else:
                        cur_pos = self.rvlist.index(self.rv)
                        if(cur_pos < len(self.rvlist)-1):
                            if(len(self.rvlist[cur_pos+1:]) > 0):
                                self.rv = random.choice(self.rvlist[cur_pos+1:])
                        self.flag = 1
        self.utilitylist = self.boulwareUtilities(self.rv,self.deadline)


    def setutilityspace(self,issues):
        for i in issues:
            self.utilityspace[i] = random.uniform(0, 1)
        self.utilitylist = self.boulwareUtilities(self.rv,self.deadline)
       # print (self.utilitylist)
       # print(self.utilityspace)

    def offerbid(self,round_number,strategy):
        if(strategy=="bayesian"):
            mystrategybid = self.bayesianutilitylist[round_number]
        elif(strategy=="boulware"):
            mystrategybid = self.utilitylist[round_number]
        closest_value = 2
        utility_return = mystrategybid
        for issue_vals in self.utilityspace:
            temp = min(closest_value,abs(self.utilityspace[issue_vals]-mystrategybid))
            if(temp!=closest_value):
                closest_value = temp
                utility_return = self.utilityspace[issue_vals]
                index = issue_vals
        return utility_return,index
    
    def evaluate_bid_and_vote(self,offered_value,bid_issue,round_number,strategy):
        #print(self.utilitylist)
        if(strategy=="bayesian"):
            mystrategybid = self.bayesianutilitylist[round_number]
        elif(strategy=="boulware"):
            mystrategybid = self.utilitylist[round_number]
        closest_value = 2
        utility_return = mystrategybid
        for issue_vals in self.utilityspace:
            temp = min(closest_value,abs(self.utilityspace[issue_vals]-mystrategybid))
            if(temp!=closest_value):
                closest_value = temp
                utility_return = self.utilityspace[issue_vals]
                index = issue_vals
        opponent_offered = self.utilityspace[bid_issue]
        print("The bid offered by the current bidding party is ",offered_value," and the bid issue is",bid_issue," and my utility for this issue is ",opponent_offered)
        print("The current utility of the party is",utility_return)
        if(opponent_offered > utility_return):
            print("Oh higher bid offered..accepting..")
            return "Yes"
        else:
            print("Oh lower bid offered..rejecting..")
            return "No"

    def boulwareUtilities (self,rv,Deadline):
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
        ut.reverse()
        return ut
    def utilitylistrv(self):
        self.myutilitiesrv = []
        for i in range(0,len(self.rvlist)):
            self.myutilitiesrv.append(self.boulwareUtilities(self.rvlist[i],self.deadline))

    def beiliefplot(self):
        self.Probabilitylist = []
        self.roundproblist = []
        for i in range(0,len(self.rvlist)):
            self.roundproblist.append(1.0/len(self.rvlist))
        self.Probabilitylist.append(self.roundproblist)
    
    def mypedictedrvs(self,roundnum):
        self.predictedrvs = []
        for rvs in self.rvlist:
            self.predictedrvs.append(self.tempgenerate(rvs,self.deadline,roundnum,self.roundrvlist))
        self.Means()
        if(roundnum > 1):
            # print("check here boi",self.means_offers)
            self.calculategamma(self.predictedrvs,self.means_offers,self.roundrvlist,np.mean(self.roundrvlist))
            # print("asfafafafew",self.gamma,"new gamma here",self.new_gamma)
            self.updateprobs(self.roundproblist)
            # print("let us see",self.roundproblist,self.Probabilitylist)
        print("--------------------------------------------------------------------")
        self.generatebayesianutility(roundnum)
        print("final check",self.bayesianutilitylist)
        print("--------------------------------------------------------------------")

    def tempgenerate(self,i,Deadline,roundnum,RV):
        temp=[0]
        #print str(i) + "  " + str(RV[roundnum-2])
        t1=0	
        b=0
        t=0
        #print (str(roundnum) + " " + str(len(RV)))
        #print("adsfsdfsf",self.roundrvlist)
        for roundno in range(1,roundnum+1):
            t+=(np.log(float(roundno)/Deadline))*(np.log(float(roundno)/Deadline))

            # if(RV[0]-RV[roundno]==0 or (RV[0]-i)==0):
            #print (str(RV[0]) + " " + str(RV[roundno]) + " " + str(i) +" " +str(roundno))

            p=np.log ( float(RV[0]-RV[roundno])/ (RV[0]-i) )
            t1=t1+(np.log(float(roundno)/Deadline))*p
            b=float(t1)/t
            #print  ("t: ",t,"t1: ",t1,"p: ",p,"b: ",b,"check r/d: ",float(roundno)/Deadline)
            # print str(b) + " " + str(t1) + " " + str(t) + " " + str(float(roundno)/Deadline)

            x = RV[0] + (i-RV[0])*(math.pow(float(roundno)/Deadline,b))

            #print ("x: ",x, "RV[0]: ",RV[0], "i : ",i, "math: ",math.pow(float(roundno)/Deadline,b) )

            x=float("{0:.4f}".format(x))
            temp.append(x)
        #print ("aditya ------------------temp: ",temp)
        return temp

    def  Means(self):
        templist = []
        for predictions in self.predictedrvs:
            templist.append(np.mean(predictions))
        self.means_offers = templist
    
    def calculategamma(self,offers,means_offers,RV,mean_RV):
        # print("offers here",offers,len(offers),len(self.gamma),len(self.new_gamma))
        for i in range(0,len(offers)):
            variation=0
            d1=0
            d2=0
            for j in range(1,len(offers[i])):
                variation += (RV[j] - mean_RV) * (offers[i][j]-means_offers[i])
                d1+=math.pow((RV[j] - mean_RV),2)
                d2+=math.pow((offers[i][j]-means_offers[i]),2)
                # print("here i am","RV[j] :",RV[j],"mean_RV : ",mean_RV,"offfers :",offers[i][j],"means_offers :",means_offers[i])
            denominator=math.sqrt(d1*d2)
            #if(roundnum>=1):
            self.gamma[i] = float("{0:.4f}".format(float(variation)/denominator))
            self.new_gamma[i]=float(self.gamma[i]+1)/2


    def updateprobs(self,new_probability):
        print(self.Probabilitylist)
        new_total=0
        for i in range(0,len(new_probability)):
            new_probability[i]=new_probability[i]*self.new_gamma[i]
            # print "------"
            # print new_probability[i]
            # print "------"
            new_total+=new_probability[i]   
        for i in range(0,len(new_probability)):
            new_probability[i]=float("{0:.4f}".format(new_probability[i]/new_total))
            if(new_probability[i]<=0.0002):
                new_probability[i]=0.0002
            if(new_probability[i]>=0.9998):
                new_probability[i]=0.9998
            self.Probabilitylist.append(new_probability)                 ###check here for resolving

    def generatebayesianutility(self,roundnum):
        bayesian_utility = 0
        for i in range(0,len(self.roundproblist)):
            bayesian_utility += self.roundproblist[i]*self.myutilitiesrv[i][roundnum]
        self.bayesianutilitylist.append(bayesian_utility)
