import random
import math
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
    def checkupdate(self,updateflag,rounds,updaterate):
        if(updateflag==False):
            return
        else:
            #print(updateflag,updaterate,rounds)
            if(updaterate==rounds):
                self.rv = random.choice(self.rvlist)
            else:
                if(self.flag==1):
                    prob = random.randint(1,4)
                    if(prob < 4):
                        cur_pos = self.rvlist.index(self.rv)
                        if(cur_pos < 3):
                            self.rv = self.rvlist[cur_pos+1]
                    else:
                        cur_pos = self.rvlist.index(self.rv)
                        self.rv = random.choice(self.rvlist[:cur_pos])
                        self.flag = -1
                elif(self.flag == -1):
                    prob = random.randint(1,4)
                    if(prob < 4):
                        cur_pos = self.rvlist.index(self.rv)
                        if(cur_pos > 0):
                            self.rv = random.choice(self.rvlist[:cur_pos])
                    else:
                        cur_pos = self.rvlist.index(self.rv)
                        if(cur_pos < 3):
                            self.rv = self.rvlist[cur_pos+1]
                        self.flag = 1
        self.utilitylist = self.boulwareUtilities(self.rv,self.deadline)


    def setutilityspace(self,issues):
        for i in issues:
            self.utilityspace[i] = random.uniform(0, 1)
        self.utilitylist = self.boulwareUtilities(self.rv,self.deadline)
       # print (self.utilitylist)
       # print(self.utilityspace)

    def offerbid(self,round_number):
        boulware = self.utilitylist[round_number]
        closest_value = 2
        utility_return = boulware
        for issue_vals in self.utilityspace:
            temp = min(closest_value,abs(self.utilityspace[issue_vals]-boulware))
            if(temp!=closest_value):
                closest_value = temp
                utility_return = self.utilityspace[issue_vals]
                index = issue_vals
        return utility_return,index
    
    def evaluate_bid_and_vote(self,offered_value,bid_issue,round_number):
        #print(self.utilitylist)
        boulware = self.utilitylist[round_number]
        closest_value = 2
        utility_return = boulware
        for issue_vals in self.utilityspace:
            temp = min(closest_value,abs(self.utilityspace[issue_vals]-boulware))
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
