import random
import math,datetime
import numpy as np
import copy
class Party:
    '''This is Party Class'''
    def __init__(self,name,deadline):
        self.name = name
        self.utilityspace = {}
        self.response = ["Yes","No"]
        self.rv = 0.0
        self.deadline = deadline
        # self.rvlist = [0.12,0.321,0.57,0.75]
        # self.rvlist = [i for i in range(5,50,5)]   ## utility of rvs
        self.rvlist = [0.12,0.75]
        self.flag = 1
        self.roundrvlist =  []
        self.means_offers = []
        self.gamma = [0]*len(self.rvlist)
        self.new_gamma = [0]*len(self.rvlist)
        self.bayesianutilitylist = []
        self.counterutilitylist  = []
        self.strategy = "boulware"
        self.countlist = [0]*len(self.rvlist)
        self.lstmlist = [0]*len(self.rvlist)
        self.lstmutilitylist = []
        self.optimallist = []
        self.probupdatesround = []
        self.Probabilitylist = []
        self.roundproblist = []

    def checkupdate(self,updateflag,rounds,updaterate):
        if(updateflag==False):
            pass
        else:
            # print(updateflag,updaterate,rounds)
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
                # print("updating rv",self.rv)
            if self.strategy == "optimal":
                self.utilitylist = self.optimalbidder(self.rvutils[self.rvlist.index(self.rv)],self.deadline)        #optimalbidder
            else:
                # self.utilitylist = self.boulwareUtilities(self.rvutils[self.rvlist.index(self.rv)],self.deadline)      #boulware
                self.utilitylist = self.optimalbidder(self.rvutils[self.rvlist.index(self.rv)],self.deadline)        #optimalbidder

        return self.rv


    def initialiselistboulware(self,cur_rv):
        if self.strategy == "optimal":
            self.utilitylist = self.optimalbidder(cur_rv,self.deadline)  #optimal
        else:
            # self.utilitylist = self.boulwareUtilities(cur_rv,self.deadline) #boulware
            self.utilitylist = self.optimalbidder(cur_rv,self.deadline)  #optimal


    def offerbid(self,round_number,strategy):
        if(strategy=="bayesian"):
            mystrategybid = self.bayesianutilitylist[round_number]
            # print("offering",mystrategybid,self.strategy,self.bayesianutilitylist)
        elif(strategy=="boulware"):
            mystrategybid = self.utilitylist[round_number]
        elif(strategy=="optimal"):
            mystrategybid = self.utilitylist[round_number]
            # print("offering",mystrategybid,self.strategy)
        elif(strategy=="counter"):
            mystrategybid = self.counterutilitylist[round_number]
            # print("offering",mystrategybid,self.strategy,self.counterutilitylist)
        elif(strategy=="lstm"):
            mystrategybid = self.lstmutilitylist[round_number]
            # print("offering",mystrategybid,self.strategy,self.lstmutilitylist)
        closest_value = 2
        utility_return = mystrategybid
        for issue_vals in self.utilityspace:
            temp = min(closest_value,abs(self.utilityspace[issue_vals]-mystrategybid))
            if(temp<closest_value):
                closest_value = temp
                utility_return = self.utilityspace[issue_vals]
                index = issue_vals
        # print("MYYYYYY",utility_return,index)
        return utility_return,index
    
    def evaluate_bid_and_vote(self,offered_value,bid_issue,round_number,strategy):
        #print(self.utilitylist)
        if(strategy=="bayesian"):
            mystrategybid = self.bayesianutilitylist[round_number]
        elif(strategy=="boulware"):
            mystrategybid = self.utilitylist[round_number]
        elif(strategy=="optimal"):
            mystrategybid = self.utilitylist[round_number]
        elif(strategy=="counter"):
            mystrategybid = self.counterutilitylist[round_number]
        elif(strategy=="lstm"):
            mystrategybid = self.lstmutilitylist[round_number]
        closest_value = 2
        utility_return = mystrategybid        
        # print("evaluating",mystrategybid,self.name,self.strategy)
        for issue_vals in self.utilityspace:
            temp = min(closest_value,abs(self.utilityspace[issue_vals]-mystrategybid))
            if(temp<closest_value):
                closest_value = temp
                utility_return = self.utilityspace[issue_vals]
                index = issue_vals
        opponent_offered = self.utilityspace[bid_issue]
        # print("The bid offered by the current bidding party is ",offered_value," and the bid issue is",bid_issue," and my utility for this issue is ",opponent_offered)
        # print("The current utility of the party is",utility_return,self.strategy)
        if(opponent_offered > utility_return):
            # print("Oh higher bid offered..accepting..")
            return "Yes",opponent_offered
        else:
            # print("Oh lower bid offered..rejecting..")
            return "No",opponent_offered

    def boulwareUtilities (self,rv,Deadline):
        # print("checkhere",rv)
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

    def optimalbidder(self,rv,Deadline):
        ut = []
        # ut.append(.25+.25*rv)
        # for i in range(1,Deadline):
        #     ut.append(.25*math.pow(ut[i-1]+1,2))
        # ut.reverse()
        ut.append(rv)
        for i in range(1,Deadline):
            ut[i] = (((ut[i-1]+1)/2)**2)        
        ut.reverse()
        # print(ut)
        return ut
    
    def utilitylistrv(self):
        self.myutilitiesrv = []
        # print("check",self.rvutils)
        for i in range(0,len(self.rvutils)):
            # self.myutilitiesrv.append(self.boulwareUtilities(self.rvutils[i],self.deadline))
            self.myutilitiesrv.append(self.optimalbidder(self.rvutils[i],self.deadline))
        # print(self.myutilitiesrv)

    def beiliefplot(self):
        for i in range(0,len(self.rvutils)):
            self.roundproblist.append(1.0/len(self.rvutils))
        self.Probabilitylist.append(copy.deepcopy(self.roundproblist))
    
    def mypedictedrvs(self,roundnum):
        self.predictedrvs = []
        for rvs in self.rvutils:
            self.predictedrvs.append(self.tempgenerate(rvs,self.deadline,roundnum,self.roundrvlist))
        self.Means()
        if(roundnum >= 1):
            # print("check here boi",self.means_offers)
            self.calculategamma(self.predictedrvs,self.means_offers,self.roundrvlist,np.mean(self.roundrvlist))
            # print("asfafafafew",self.gamma,"new gamma here",self.new_gamma)
            self.updateprobs(self.roundproblist)
            # print("let us see",self.roundproblist,self.Probabilitylist)
        #print("--------------------------------------------------------------------")
        self.generatebayesianutility(roundnum)
        #print("final check",self.bayesianutilitylist)
        #print("--------------------------------------------------------------------")

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
        #print(self.Probabilitylist)
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
        # self.Probabilitylist.append(new_probability)                 ###check here for resolving
        self.Probabilitylist.append(copy.deepcopy(new_probability))


    def generatebayesianutility(self,roundnum):
        bayesian_utility = 0
        # print(self.roundproblist)   
        for i in range(0,len(self.roundproblist)):
            bayesian_utility += self.roundproblist[i]*self.myutilitiesrv[i][roundnum]
        self.bayesianutilitylist.append(bayesian_utility)

    def updatecounts(self):
        cur_rv = self.rv
        cur_pos =self.rvlist.index(self.rv)
        self.countlist[cur_pos]+=1
    def updateprobscounter(self):
        for i in range(0,len(self.rvlist)):
            self.roundproblist[i] = self.countlist[i]/np.sum(self.countlist)
        self.Probabilitylist.append(copy.deepcopy(self.roundproblist))
        # print("here",self.roundproblist,self.countlist,self.Probabilitylist)
    def counterinitialize(self,rounds):
        if(rounds >=1):
            self.updatecounts()
            #print("checking counter",self.countlist)
            self.updateprobscounter()
            #print("checking counter problist",self.roundproblist)
        self.generatecounterutility(rounds)
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #print(self.counterutilitylist)
        #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    def generatecounterutility(self,roundnum):
        counter_utility = 0
        for i in range(0,len(self.roundproblist)):
            counter_utility += self.roundproblist[i]*self.myutilitiesrv[i][roundnum]
        self.counterutilitylist.append(counter_utility)
    
    def findclosest(self,cur_rv):
        temp = []
        for i in range(len(self.rvlist)):
            temp.append(abs(cur_rv-self.rvlist[i]))
        ans = temp.index(min(temp))
        ans = self.rvlist[ans]
        return ans
    def lstmcountsupdate(self,rounds,test_count):
        # print(rounds,test_count)
        cur_rv = self.lstmrv[test_count][rounds-1]
        cur_rv = self.findclosest(cur_rv)
        cur_pos = self.rvlist.index(cur_rv)
        self.lstmlist[cur_pos]+=1

    def updatelstmpreds(self):
        for i in range(len(self.rvlist)):
            self.roundproblist[i] = self.lstmlist[i]/np.sum(self.lstmlist)
        self.Probabilitylist.append(copy.deepcopy(self.roundproblist))


    def generate_lstmrules(self,roundnum):
        lstm_utlity = 0
        for i in range(len(self.roundproblist)):
            lstm_utlity += self.roundproblist[i]*self.myutilitiesrv[i][roundnum]
        self.lstmutilitylist.append(lstm_utlity)

    def lstminitialize(self,updaterate,rounds,test_count):
        # print("Lstm here")
        # self.lstmrv = np.load('LSTM/Data_100_4hyp/Preds/pred_fire'+str(updaterate)+'.npy')   ### 4 Hypo fire
        self.lstmrv = np.load('LSTM/Data_100_2hyp/Preds/pred_fire'+str(updaterate)+'.npy')   ### 2 Hypo fire
        self.lstmrv = self.lstmrv.reshape(300,99)
        # print("here",self.lstmrv.shape)
        if(rounds>=1):
            self.lstmcountsupdate(rounds,test_count)
            self.updatelstmpreds()
        self.generate_lstmrules(rounds)


