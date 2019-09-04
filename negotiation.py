import random,time,sys,math,os,datetime
from parties import Party
from domain import Domain
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from Generator import utilitygen
testa = []
testb = []
testc = []
tempa = 0
tempb = 0
tempc = 0
def Negotiation(deadline,parties,updaterate):
    number_of_parties = len(parties)
    iterator = 0
    myparty = parties[2]  ###my agent bayesian
    myparty.strategy = "bayesian"
    mycounterparty = parties[1]
    mycounterparty.strategy = "counter"
    for rounds in range(deadline):
        #print("*********************************************************************************************")
        #print('Round ',rounds)
        #print("*********************************************************************************************")
        #time.sleep(1)
        updateflag = False
        if((rounds%updaterate==0 and rounds >=1) or rounds==1):
            updateflag = True
            for party in parties:
                party.checkupdate(updateflag,rounds,updaterate)
        for party in parties:
            party.roundrvlist.append(party.rv)
        #print("yoboi",myparty.roundrvlist)
        myparty.mypedictedrvs(rounds)
        mycounterparty.counterinitialize(rounds)
        #print("idhr",myparty.predictedrvs)
        for bidding_party in parties:
            #print("Current Bid by Party #",bidding_party.name)
            random.seed(datetime.datetime.now())
            current_bid,bid_issue = bidding_party.offerbid(rounds,bidding_party.strategy)
            #print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue)
            votesevaluater = False
            tempcheck = False
            for party in parties:
                if party!=bidding_party:
                    partyresponse,partyvalue = party.evaluate_bid_and_vote(current_bid,bid_issue,rounds,party.strategy)
                    if(partyresponse=="No"):
                        votesevaluater = False
                        tempa = 0
                        tempb = 0
                        tempc = 0
                        break
                    else:
                        votesevaluater = True
                        tempcheck = True
                        if(party.name=='1'):
                            tempa = partyvalue
                        elif(party.name=='2'):
                            tempb = partyvalue
                        elif(party.name=='3'):
                            tempc = partyvalue
            if(votesevaluater==True):
                #print("here")
                if(bidding_party.name=='1'):
                    testa.append(current_bid)
                    testb.append(tempb)
                    testc.append(tempc)
                elif(bidding_party.name=='2'):
                    testb.append(current_bid)
                    testa.append(tempa)
                    testc.append(tempc)
                elif(bidding_party.name=='3'):
                    testc.append(current_bid)
                    testa.append(tempa)
                    testb.append(tempb)
                print("Negotiation Successfull Offered by Party #",bidding_party.name," in round number",rounds)
                #print(len(parties[1].bayesianutilitylist),len(parties[2].counterutilitylist))
                #print(testa,testb,tempc)

                return current_bid
            else:
                continue
    print("Sorry Deadline is over and negotiation could not be completed")
    #print(parties[1].bayesianutilitylist,parties[2].counterutilitylist)
    return  0.0


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
    pref1 = utilitygen('car-Profile1.xml')
    pref2 = utilitygen('car-Profile2.xml')
    pref3 = utilitygen('car-Profile3.xml')
    # parties[0].utilityspace = {'a' : 1.0 , 'b' : 0.4 , 'c' : 0.6 , 'd' : 0.4 , 'e' : 0.2  }
    # parties[1].utilityspace = {'a' : 0.2 , 'b' : 0.4 , 'c' : 0.6 , 'd' : 0.4 , 'e' : 1.0  }
    # parties[2].utilityspace = {'a' : 0.2 , 'b' : 0.4 , 'c' : 1.0 , 'd' : 0.4 , 'e' : 0.2  } 
    # 
    #   
    parties[0].utilityspace = pref3
    parties[1].utilityspace = pref2
    parties[2].utilityspace = pref1 
    # deadline = int(input("Enter the deadline : "))
    #time.sleep(3)
    print("Starting Negotiation Protocol")
    tests = 100
    accepts = []
    #Negotiation(deadline,parties,updaterate)
    #print(testb)
    #print(testc)
    for i in range(tests):
        accepts.append(Negotiation(deadline,parties,updaterate))
    #print(testa,testb,testc)
    print("Mean",np.mean(testa),np.mean(testb),np.mean(testc))
    print(testa),
    print(testb)
    print(testc)
    # fig = plt.figure()
    # #ax = fig.add_subplot(111, projection='3d')
    # # ax.plot_trisurf(np.array(testa),np.array(testb),np.array(testc), color='white', edgecolors='grey', alpha=0.5)
    # plt.scatter(testb,testc, c='red')
    # plt.show()
if __name__ == '__main__':
    main()