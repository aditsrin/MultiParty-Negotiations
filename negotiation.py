import random,time,sys,math,os,datetime
from parties import Party
from domain import Domain
import numpy as np
def Negotiation(deadline,parties,updaterate):
    number_of_parties = len(parties)
    iterator = 0
    myparty = parties[1]  ###my agent bayesian
    myparty.strategy = "bayesian"
    for rounds in range(deadline):
        print("*********************************************************************************************")
        print('Round ',rounds)
        print("*********************************************************************************************")
        time.sleep(1)
        updateflag = False
        if((rounds%updaterate==0 and rounds >=1) or rounds==1):
            updateflag = True
            for party in parties:
                party.checkupdate(updateflag,rounds,updaterate)
        for party in parties:
            party.roundrvlist.append(party.rv)
        print("yoboi",myparty.roundrvlist)
        myparty.mypedictedrvs(rounds)
        print("idhr",myparty.predictedrvs)
        for bidding_party in parties:
            print("Current Bid by Party #",bidding_party.name)
            current_bid,bid_issue = bidding_party.offerbid(rounds,bidding_party.strategy)
            print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue)
            votesevaluater = False
            for party in parties:
                if party!=bidding_party:
                    partyresponse = party.evaluate_bid_and_vote(current_bid,bid_issue,rounds,party.strategy)
                    if(partyresponse=="No"):
                        votesevaluater = False
                        break
                    else:
                        votesevaluater = True
            if(votesevaluater==True):
                #print("here")
                print("Negotiation Successfull Offered by Party #",bidding_party.name," in round number",rounds)
                return
            else:
                continue
    print("Sorry Deadline is over and negotiation could not be completed")


def main():
    random.seed(datetime.datetime.now())
    print("Welcome to Negotiation Platform")
    #domain_name = input("Enter The domain name : ")
    #domain_issues_number = int(input("Enter the number of issues : "))
    domain_issues_number = 10
    initial_issues_range = [i/10 for i in range(0,11)]
    initial_domain = {}
    issues_list = []
    issue_names = ['a','b','c','d','e','f','g','h','i','j']
    for domain_issues in range(0,domain_issues_number):
        #issue_name = input("Enter issue #" + str(domain_issues))
        initial_domain[issue_names[domain_issues]] = initial_issues_range
        issues_list.append(issue_names[domain_issues])
    #number_of_parties = int(input("Please Enter The number of negotiating parties : "))
    number_of_parties = 3
    parties = []
    current_domain = Domain(initial_domain)
    deadline = 100
    updaterate = 4
    for partynames in range(1,number_of_parties+1):
        tempparty = Party(str(partynames),deadline)
        tempparty.setutilityspace(issues_list)
        tempparty.utilitylistrv()                         ###### GenerateUtility list from rvlist
        tempparty.beiliefplot()                           ###### Belief Plot initialisation and roundprob init
        # print("check",tempparty.myutilitiesrv[3])
        # print("adsa",tempparty.Probabilitylist)
        # print("asfasf",tempparty.roundproblist)
        parties.append(tempparty)
    #deadline = int(input("Enter the deadline : "))
    #time.sleep(3)
    print("Starting Negotiation Protocol")
    Negotiation(deadline,parties,updaterate)
if __name__ == '__main__':
    main()