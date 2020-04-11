import random,time,sys,math,os,datetime
from parties_fire import Party
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from Generator import utilitygen
import itertools
import copy

def Negotiation(deadline,parties,updaterate,test_count):
    # print(updaterate)
    global testlist
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
        for i in range(len(parties)):
            bidding_party = parties[i]
            # print("Current Bid by Party #",bidding_party.name)
            random.seed(datetime.datetime.now())
            current_bid,bid_issue = bidding_party.offerbid(rounds,bidding_party.strategy)
            # print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue)
            votesevaluater = False
            tempcheck = False
            templist = [0 for i in range(len(parties))]
            for j in range(len(parties)):
                party = parties[j]
                if party!=bidding_party:
                    partyresponse,partyvalue = party.evaluate_bid_and_vote(current_bid,bid_issue,rounds,party.strategy)
                    if(partyresponse=="No"):
                        votesevaluater = False
                        # templist = [0]*len(parties)
                        templist = [0 for i in range(len(parties))]
                        break
                    else:
                        votesevaluater = True
                        tempcheck = True
                        templist[j] = partyvalue
            if(votesevaluater==True):
                for j in range(len(parties)):
                    if(j!=i):
                        testlist[j].append(templist[j])
                testlist[i].append(current_bid)
                # print("Negotiation Successfull Offered by Party #",bidding_party.name," in round number",rounds,templist)
                # print(len(parties[0].bayesianutilitylist),len(parties[1].counterutilitylist))

                return current_bid,bidding_party.name
            else:
                continue
    # print("Sorry Deadline is over and negotiation could not be completed")
    #print(parties[1].bayesianutilitylist,parties[2].counterutilitylist)
    return  0.0,None
def closehelper(space,rvs):
    mylist = []
    for j in rvs:
        close = 2
        for i in space:
            temp = min(close,abs(space[i]-j))
            if(temp<close):
                close = temp
                util = space[i]
        mylist.append(util)
    return mylist
def testbench(prefs):
    global testlist
    deadline = 100
    pref_names = ['pref'+str(i+1) for i in range(len(prefs))]
    perms = list(itertools.permutations(prefs))
    perm_names = list(itertools.permutations(pref_names))
    # perms = [prefs]
    # print(len(perms))
    for curlist,names in zip(perms,perm_names):
        for j in range(len(curlist)):
            parties[j].utilityspace = curlist[j]
            # print(parties[j].utilityspace)
            parties[j].rvlist = [.12,.35,.51,.75]        ## 4 Hypo fire    
            # parties[j].rvlist = [.12,.75]              #@@@@ 2 Hypo Fire
            parties[j].rvutils = closehelper(parties[j].utilityspace,parties[j].rvlist)
            # parties[j].rvlist = [i/50 for i in parties[j].rvlist]
            parties[j].initialiselistboulware(random.choice(parties[j].rvlist))
            parties[j].utilitylistrv()
            parties[j].beiliefplot()
            # parties[j].rvlist = [parties[j].utilityspace[i] for i in parties[j].rvlist]
            # print("######",parties[j].name,parties[j].rvlist,parties[j].rvutils)
            print("Party ",j+1,"Profile ==> ",names[j],end='   ')
        tests = 4
        accepts = []
        rates = [2,5,10,20,50]
        # rates = [2]
        print()
        ratewise_results = []
        for updaterate in rates:
            testlist= [[] for j in range(len(parties))]
            for i in range(tests):
                parties = initialiseparties()
                accepts.append(Negotiation(deadline,parties,updaterate,i))
            # print("For updaterate == ",updaterate,end=' ')
            # print("Mean",round(np.mean(testa),3),round(np.mean(testb),3),round(np.mean(testc),3))
            ratewise_results.append([np.mean(testlist[j]) for j in range(len(testlist))])
        ratewise_results = np.array(ratewise_results)
        Final_Means = list(np.mean(ratewise_results,axis=0))
        Final_Means = [str(round(i,3)) for i in Final_Means]
        print("Final Result",' '.join(list(Final_Means)))

def averagetests(prefs):
    global testlist
    deadline = 100
    tests = 20
    updaterates = [2,5,10,20,50]
    # updaterates = [2]
    pref_names = ['pref'+str(i+1) for i in range(len(prefs))]
    perms = list(itertools.permutations(prefs))
    perm_names = list(itertools.permutations(pref_names))
    # perms = [prefs]
    # perm_names = [pref_names]
    for update in updaterates:
        print("Update Rate:",update)
        ct = 0
        for i in range(tests):
            parties = initialiseparties()
            print("TEST NUMBER:",i)
            print("###################################################################################")
            testlist= [[] for j in range(len(parties))]
            for curlist,names in zip(perms,perm_names):
                for j in range(len(curlist)):
                    parties[j].utilityspace = curlist[j]
                    parties[j].rvlist = [.12,.35,.51,.75]        ## 4 Hypo fire    
                    parties[j].rvutils = closehelper(parties[j].utilityspace,parties[j].rvlist)
                    parties[j].initialiselistboulware(random.choice(parties[j].rvlist))
                    parties[j].utilitylistrv()
                    parties[j].beiliefplot()
                    # print("Party ",j+1,"Profile ==> ",names[j],end='   ')
                val,par = Negotiation(deadline,parties,update,i)
                # print("here",val,"party",par)
            # print(testlist)
            print("Average result over preferences: ",[round(np.mean(testlist[j]),3) for j in range(len(testlist))]) 
            temp =  copy.deepcopy([round(np.mean(testlist[j]),3) for j in range(len(testlist))])
            if(temp.index(max(temp))==0):
                ct+=1
        print("Wins %",ct/tests*100)
def initialiseparties():
    random.seed(datetime.datetime.now())
    parties = []
    deadline = 100
    number_of_parties =  3
    for partynames in range(1,number_of_parties+1):
        tempparty = Party(str(partynames),deadline)
        parties.append(tempparty)
    return parties
def main():
    print("Welcome to Negotiation Platform")
    # prefs = [0,0,0,0,0]
    prefs = [0,0,0]
    # prefs[0] = utilitygen('KillerRobot_util1.xml')
    # prefs[1] = utilitygen('KillerRobot_util2.xml')
    # prefs[2] = utilitygen('KillerRobot_util3.xml')
    prefs[0] = utilitygen('Supermarket-A-prof1.xml')
    prefs[1] = utilitygen('Supermarket-A-prof2.xml')
    prefs[2] = utilitygen('Supermarket-B-prof1.xml')
    # prefs[3] = utilitygen('Supermarket-B-prof2.xml')
    # prefs[4] = utilitygen('Supermarket-C-prof1.xml')
    # parties[4].strategy = "optimal"
    # prefs[0] = {i:random.random() for i in range(100)}
    # prefs[1] = {i:random.random() for i in range(100)}
    # prefs[2] = {i:random.random() for i in range(100)}
    # print(prefs)
    print("Starting Negotiation Protocol")
    print("Fire Domain")
    # testbench(prefs)
    averagetests(prefs)
if __name__ == '__main__':
    main()