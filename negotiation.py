import random,time,sys,math,os,datetime
from parties import Party
from domain import Domain
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from Generator import utilitygen
from Meeting_prefs import meeting
import itertools
testa = []
testb = []
testc = []
tempa = 0
tempb = 0
tempc = 0
def Negotiation(deadline,parties,updaterate,test_count):
    # print(updaterate)
    number_of_parties = len(parties)
    iterator = 0
    myparty = parties[2]  
    myparty.strategy = "lstm"
    mycounterparty = parties[1]
    mycounterparty.strategy = "counter"
    mybayesian = parties[0]
    mybayesian.strategy = "bayesian" ###my agent bayesian
    for rounds in range(deadline):
        # print('Round ',rounds)
        #time.sleep(1)
        updateflag = False
        if((rounds%updaterate==0 and rounds >=1) or rounds==1):
            updateflag = True
        for party in parties:
            party.checkupdate(updateflag,rounds,updaterate)
        for party in parties:
            try:
                party.roundrvlist.append(party.rvutils[party.rvlist.index(party.rv)])
            except:
                party.roundrvlist.append(0.0)
        # print("yoboi",mybayesian.roundrvlist)
        mybayesian.mypedictedrvs(rounds)                      ##Bayesian commented
        myparty.lstminitialize(updaterate,rounds,test_count)
        mycounterparty.counterinitialize(rounds)
        #print("idhr",myparty.predictedrvs)
        for bidding_party in parties:
            # print("Current Bid by Party #",bidding_party.name)
            random.seed(datetime.datetime.now())
            current_bid,bid_issue = bidding_party.offerbid(rounds,bidding_party.strategy)
            # print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue)
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
                # print("Negotiation Successfull Offered by Party #",bidding_party.name," in round number",rounds)
                #print(len(parties[1].bayesianutilitylist),len(parties[2].counterutilitylist))
                #print(testa,testb,tempc)

                return current_bid
            else:
                continue
    # print("Sorry Deadline is over and negotiation could not be completed")
    #print(parties[1].bayesianutilitylist,parties[2].counterutilitylist)
    return  0.0
def testbench(parties,pref1,pref2,pref3):
    deadline = 100
    prefs = ['pref1','pref2','pref3']
    perms = list(itertools.permutations(prefs))
    # perms = [prefs]
    # print(len(perms))
    for curlist in perms:
        for j in range(len(curlist)):
            parties[j].utilityspace = eval(curlist[j])
            # print(parties[j].utilityspace)
            parties[j].rvlist = [i for i in range(5,50,5)] 
            parties[j].rvutils = [parties[j].utilityspace[i] for i in parties[j].rvlist]
            parties[j].rvlist = [i/50 for i in parties[j].rvlist]
            # print("#####",parties[j].name)
            parties[j].utilitylistrv()
            parties[j].beiliefplot()
            # parties[j].rvlist = [parties[j].utilityspace[i] for i in parties[j].rvlist]
            # print(parties[j].rvlist)
            print("Party ",j+1,"Profile ==> ",curlist[j],end='   ')
        tests = 100
        accepts = []
        rates = [2,5,10,20,50]
        # rates = [2]
        print()
        ratewise_results = []
        for updaterate in rates:
            for i in range(tests):
                accepts.append(Negotiation(deadline,parties,updaterate,i))
            print("For updaterate == ",updaterate,end=' ')
            print("Mean",np.mean(testa),np.mean(testb),np.mean(testc))
            # print(testa,testb,testc)
            ratewise_results.append([np.mean(testa),np.mean(testb),np.mean(testc)])
        ratewise_results = np.array(ratewise_results)
        Final_Means = list(np.mean(ratewise_results,axis=0))
        Final_Means = [str(i) for i in Final_Means]
        print("Final Result",' '.join(list(Final_Means)))

# def filereads(filelist):
#     for file in filelist:


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
    # updaterate = 4
    deadline = 100
    for partynames in range(1,number_of_parties+1):
        tempparty = Party(str(partynames),deadline)
        # tempparty.setutilityspace(issues_list)
        # tempparty.utilitylistrv()                         ###### GenerateUtility list from rvlist
        # tempparty.beiliefplot()                           ###### Belief Plot initialisation and roundprob init
        # print("check",tempparty.myutilitiesrv[3])
        parties.append(tempparty)
    # pref1 = utilitygen('KillerRobot_util1.xml')
    # pref2 = utilitygen('KillerRobot_util2.xml')
    # pref3 = utilitygen('KillerRobot_util3.xml')
    prefs = meeting()
    pref1 = prefs[0]
    pref2 = prefs[1]
    pref3 = prefs[2]
    # parties[0].utilityspace = pref1
    # parties[1].utilityspace = pref2
    # parties[2].utilityspace = pref3
    print("Starting Negotiation Protocol")
    print("Meeting Domain")
    testbench(parties,pref1,pref2,pref3)


    # Negotiation(deadline,parties,2,0)
    # print(testa),
    # print(testb)
    # print(testc)
    # fig = plt.figure()
    # #ax = fig.add_subplot(111, projection='3d')
    # # ax.plot_trisurf(np.array(testa),np.array(testb),np.array(testc), color='white', edgecolors='grey', alpha=0.5)
    # plt.scatter(testb,testc, c='red')
    # plt.show()
if __name__ == '__main__':
    main()