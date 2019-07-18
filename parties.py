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
    def setutilityspace(self,issues):
        for i in issues:
            self.utilityspace[i] = random.uniform(0, 1)
        self.utilitylist = self.boulwareUtilities(self.rv,self.deadline)
        print(self.utilityspace)

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
        print("check here",opponent_offered,bid_issue,utility_return)
        if(opponent_offered > utility_return):
            return "Yes"
        else:
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
        return ut
