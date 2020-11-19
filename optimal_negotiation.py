import random,time,sys,math,os,datetime
from optimal_parties import Party
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
    check = [[] for i in range(4)]
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
            # print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue,bidding_party.strategy)
            votesevaluater = False
            tempcheck = False
            templist = [0 for i in range(len(parties))]
            # check[i].append(current_bid)
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
                print("Negotiation Successfull Offered by Party #",bidding_party.name," in round number",rounds)
                # print(len(parties[0].bayesianutilitylist),len(parties[1].counterutilitylist))
                return current_bid,bidding_party.name
            else:
                continue
    #     check_data = np.array(check)
    # np.save('checkdata',check_data)
    # print(check_data.shape)
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

def randomprefs():
    temp = {i:random.random() for i in range(100)}
    # ans  = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1],reverse=True)}
    # sortkeys = list(ans.keys())
    # n = len(sortkeys)
    # check = {}
    # for i in range(1,n+1):
    #     check[i] = ans[sortkeys[i-1]]
    return temp

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

def checkplots(parties):
    hyp = [.12,.75] 
    for i in range(len(hyp)):
        for j in range(3):
            party = parties[j]
            print(party.strategy)
            print("************************************************************************************************************************")
        # if(party.strategy!='optimal'):
            # print(eval('party.'+party.strategy+'utilitylist'))
            # print(party.Probabilitylist)
            data = []
            for probs in party.Probabilitylist:
                data.append(probs[i])
            # print(data)
            plt.plot(data,label=party.strategy)
        # fig = plt.figure(figsize=(10,5))
        plt.legend(loc=1)
        plt.title('Optimal Belief Plots for Hypothesis '+str(hyp[i]))
        plt.savefig('./Images/Optimal_Belief_Plot_Hyp '+str(hyp[i])+'.png')
        plt.close()

    # for party in parties:
    #     print(party.strategy)
    #     print("************************************************************************************************************************")
    #     print(party.Probabilitylist)
    #     for j in range(len(hyp)):
    #         temp = []
    #         for k in range(len(party.Probabilitylist)):
    #             temp.append(party.Probabilitylist[k][j])
    #         plt.title("For hypothesis "+str(hyp[j])+" the biliefs are for agent " + str(party.strategy))
    #         plt.plot(temp)
    #         plt.savefig('./Images/'+str(party.strategy)+'_'+str(hyp[j])+'.png')
    #         plt.close()
    # for j in range(len(hyp)):
    #     for party in parties:
    #         temp = []
    #         for k in range(len(party.Probabilitylist)):
    #             temp.append(party.Probabilitylist[k][j])
    #         plt.plot(temp,label=party.strategy)
    #     plt.legend()
    #     plt.title('Hypothesis: '+str(hyp[j]))
    #     plt.savefig('./Images/Hypothesis_  '+str(hyp[j])+'.png')
    #     plt.close()



def averagetests(prefs):
    global testlist
    deadline = 100
    tests = 1
    # updaterates = [2,5,10,20,50]
    updaterates = [2]
    pref_names = ['pref'+str(i+1) for i in range(len(prefs))]
    perms = list(itertools.permutations(prefs))
    perm_names = list(itertools.permutations(pref_names))
    perms = [prefs]
    perm_names = [pref_names]
    for update in updaterates:
        print("Update Rate:",update)
        ct = [0]*len(pref_names)
        mylist = []
        for i in range(tests):
            # parties = initialiseparties()
            # print("TEST NUMBER:",i)
            # print("###################################################################################")
            testlist= [[] for j in range(len(prefs))]
            for curlist,names in zip(perms,perm_names):
                parties = initialiseparties()
                for j in range(len(curlist)):
                    parties[j].utilityspace = curlist[j]
                    # parties[j].rvlist = [.12,.35,.51,.75]        ## 4 Hypo fire 
                    parties[j].rvlist = [.12,.75]        ## 2 Hypo fire    
                    parties[j].rvutils = closehelper(parties[j].utilityspace,parties[j].rvlist)
                    parties[j].initialiselistboulware(random.choice(parties[j].rvlist))
                    parties[j].utilitylistrv()
                    parties[j].beiliefplot()
                    # print("Party ",j+1,"Profile ==> ",names[j],end='   ')
                # print()
                val,par = Negotiation(deadline,parties,update,i)
                # print("here",val,"party",par)
            # print(testlist)
            print("Average result over preferences: ",[round(np.mean(testlist[j]),3) for j in range(len(testlist))]) 
            checkplots(parties)
            mylist.append(copy.deepcopy([round(np.mean(testlist[j]),3) for j in range(len(testlist))]))
            temp =  copy.deepcopy([round(np.mean(testlist[j]),3) for j in range(len(testlist))])
            ct[temp.index(max(temp))]+=1
        ct = np.array(ct)
        print("Wins %",ct/tests*100)
        mylist = np.array(mylist)
        # print(mylist.shape)
        # np.save('./Results/Fire_Results_Utils_'+str(update),mylist)
        # np.save('./Results/fouragents/Optimal/Fire2_Results_Utils_'+str(update),mylist)
def initialiseparties():
    random.seed(datetime.datetime.now())
    parties = []
    deadline = 100
    number_of_parties =  4
    for partynames in range(1,number_of_parties+1):
        tempparty = Party(str(partynames),deadline)
        parties.append(tempparty)
    parties[0].strategy = 'bayesian'
    parties[1].strategy = 'counter'
    parties[2].strategy = 'lstm'
    parties[3].strategy = 'optimal'
    return parties
def main():
    print("Welcome to Negotiation Platform")
    # prefs = [0,0,0,0,0]
    prefs = [0,0,0,0]
    # prefs[0] = utilitygen('KillerRobot_util1.xml')
    # prefs[1] = utilitygen('KillerRobot_util2.xml')
    # prefs[2] = utilitygen('KillerRobot_util3.xml')
    # prefs[3] = utilitygen('KillerRobot_util4.xml')
    # prefs[0] = randomprefs()
    # prefs[1] = randomprefs()
    # prefs[2] = randomprefs()
    # prefs[3] = randomprefs()
    # prefs[0] = utilitygen('./Preferences/group5-car_domain/car-Profile1.xml')
    # prefs[1] = utilitygen('./Preferences/group5-car_domain/car-Profile2.xml')
    # prefs[2] = utilitygen('./Preferences/group5-car_domain/car-Profile3.xml')
    # prefs[3] = utilitygen('./Preferences/group5-car_domain/car-Profile4.xml')

    prefs[0] = utilitygen('./Preferences/group6-tram/Tram_Profile1.xml')
    prefs[1] = utilitygen('./Preferences/group6-tram/Tram_Profile2.xml')
    prefs[2] = utilitygen('./Preferences/group6-tram/Tram_Profile3.xml')
    prefs[3] = utilitygen('./Preferences/group6-tram/Tram_Profile4.xml')
    print(len(list(prefs[0].keys())))
    print("Starting Negotiation Protocol")
    print("Fire Domain")
    # testbench(prefs)
    # print(prefs)
    averagetests(prefs)
if __name__ == '__main__':
    main()