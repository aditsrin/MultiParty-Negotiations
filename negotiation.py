import random,time,sys,math,os,datetime
from parties import Party
from domain import Domain
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from Generator import utilitygen
from Meeting_prefs import meeting
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
        for i  in range(len(parties)):
            bidding_party = parties[i]
            # print("Current Bid by Party #",bidding_party.name)
            random.seed(datetime.datetime.now())
            current_bid,bid_issue = bidding_party.offerbid(rounds,bidding_party.strategy)
            # print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue)
            votesevaluater = False
            tempcheck = False
            templist = [0]*len(parties)
            for j in range(len(parties)):
                party = parties[j]
                if party!=bidding_party:
                    partyresponse,partyvalue = party.evaluate_bid_and_vote(current_bid,bid_issue,rounds,party.strategy)
                    if(partyresponse=="No"):
                        votesevaluater = False
                        templist = [0]*len(parties)
                        break
                    else:
                        votesevaluater = True
                        tempcheck = True
                        templist[j] = partyvalue
            if(votesevaluater==True):
                #print("here")
                for j in range(len(parties)):
                    if(j!=i):
                        testlist[j].append(templist[j])
                testlist[i].append(current_bid)
                # print("Negotiation Successfull Offered by Party #",bidding_party.name," in round number",rounds,testlist,bidding_party.strategy)
                # print("***********************************************************************************************************************")
                return current_bid
            else:
                continue
    # print("Sorry Deadline is over and negotiation could not be completed")
    #print(parties[1].bayesianutilitylist,parties[2].counterutilitylist)
    return  0.0
def testbench(parties,prefs):
    global testlist
    deadline = 100
    # prefs = ['pref1','pref2','pref3']
    pref_names = ['pref'+str(i+1) for i in range(len(prefs))]
    perms = list(itertools.permutations(prefs))
    perm_names = list(itertools.permutations(pref_names))
    # perms = [prefs]
    # print(len(perms))
    prefwise = []
    for curlist,names in zip(perms,perm_names):
        for j in range(len(curlist)):
            parties[j].utilityspace = curlist[j]
            # print(parties[j].utilityspace)
            parties[j].rvlist = [i for i in range(5,50,5)] 
            parties[j].rvutils = [parties[j].utilityspace[i] for i in parties[j].rvlist]
            parties[j].rvlist = [i/50 for i in parties[j].rvlist]
            parties[j].initialiselistboulware(random.choice(parties[j].rvlist))
            # print("#####",parties[j].name,parties[j].rvlist,parties[j].rvutils)
            parties[j].utilitylistrv()
            parties[j].beiliefplot()
            # parties[j].rvlist = [parties[j].utilityspace[i] for i in parties[j].rvlist]
            # print(parties[j].rvlist)
            # print("Party ",j+1,"Profile ==> ",names[j],end='   ')
        tests = 2
        accepts = []
        rates = [2,5,10,20,50]
        # rates = [2]
        # print()
        ratewise_results = []
        updatewiselist = []
        for updaterate in rates:
            testlist= [[] for j in range(len(parties))]
            temp = []
            for i in range(tests):
                accepts.append(Negotiation(deadline,parties,updaterate,i))
            # print("For updaterate == ",updaterate,end=' ')
            # print("Mean",[round(np.mean(testlist[j]),3) for j in range(len(testlist))])
            # ratewise_results.append([np.mean(testa),np.mean(testb),np.mean(testc)])
            ratewise_results.append([np.mean(testlist[j]) for j in range(len(testlist))])
            temp = copy.deepcopy(testlist)
            print(temp)
            updatewiselist.append(np.array(temp))
        prefwise.append(np.array(updatewiselist))
        ratewise_results = np.array(ratewise_results)
        # print(ratewise_results)
        Final_Means = list(np.mean(ratewise_results,axis=0))
        Final_Means = [str(round(i,3)) for i in Final_Means]
        print("Final Result",' '.join(list(Final_Means)))
    prefwise = np.array(prefwise)
    np.save('prefwise',prefwise)
    # np.savetxt("prefwise.csv",prefwise, delimiter=",")

def averagetests(parties,prefs):
    global testlist
    deadline = 100
    tests = 20
    updaterates = [2,5,10,20,50]
    # updaterates = [50]
    pref_names = ['pref'+str(i+1) for i in range(len(prefs))]
    perms = list(itertools.permutations(prefs))
    perm_names = list(itertools.permutations(pref_names))
    # perms = [prefs]
    # pref_names = [pref_names]
    updatewiselist = []
    for update in updaterates:
        print("Update Rate:",update)
        mylist = []
        ct = 0
        for i in range(tests):
            parties = initialiseparties()
            print("TEST NUMBER:",i)
            print("###################################################################################")
            testlist= [[] for j in range(len(parties))]
            for curlist,names in zip(perms,perm_names):
                for j in range(len(curlist)):
                    parties[j].utilityspace = curlist[j]
                    parties[j].rvlist = [i for i in range(5,50,5)] 
                    parties[j].rvutils = [parties[j].utilityspace[i] for i in parties[j].rvlist]
                    parties[j].rvlist = [i/50 for i in parties[j].rvlist]
                    parties[j].initialiselistboulware(random.choice(parties[j].rvlist))
                    parties[j].utilitylistrv()
                    parties[j].beiliefplot()
                    # print("Party ",j+1,"Profile ==> ",names[j],end='   ')
                # print()
                Negotiation(deadline,parties,update,i)
            print("Average result over preferences: ",[round(np.mean(testlist[j]),3) for j in range(len(testlist))]) 
            # print(testlist)
            temp =  copy.deepcopy([round(np.mean(testlist[j]),3) for j in range(len(testlist))])
            if(temp.index(max(temp))==0):
                ct+=1
        print("Wins %",ct/tests*100)
            mylist.append([round(np.mean(testlist[j]),3) for j in range(len(testlist))])
        mylist = np.array(mylist)
        updatewiselist.append(mylist)
    updatewiselist = np.array(updatewiselist)
    np.save('update_results',updatewiselist)
    # np.savetxt("updatewise.csv",updatewiselist, delimiter=",")

def initialiseparties():
    random.seed(datetime.datetime.now())
    parties = []
    deadline = 100
    number_of_parties =  3
    for partynames in range(1,number_of_parties+1):
        tempparty = Party(str(partynames),deadline)
        parties.append(tempparty)
    parties[0].strategy = 'bayesian'
    parties[1].strategy = 'counter'
    parties[2].strategy = 'lstm'
    return parties

def main():
    random.seed(datetime.datetime.now())
    print("Welcome to Negotiation Platform")
    prefs = meeting()
    # print(prefs)
    # parties[4].strategy = "optimal"
    print("Starting Negotiation Protocol")
    print("Meeting Domain")
    # testbench(parties,prefs)
    averagetests(parties,prefs)
if __name__ == '__main__':
    main()