import random,time,sys,math,os,datetime
from parties import Party
from domain import Domain

def Negotiation(deadline,parties):
    number_of_parties = len(parties)
    iterator = 0
    for rounds in range(deadline):
        time.sleep(1)
        # if(iterator==number_of_parties):
        #     iterator = 0
        #     bidding_party = parties[iterator]
        # else:
        #     bidding_party = parties[iterator]
        #     iterator +=1
        for bidding_party in parties:
            print("Current Bid by Party #",bidding_party.name)
            current_bid,bid_issue = bidding_party.offerbid(rounds)
            print("The current bid utility being offered is: ",current_bid," and the current issue is ",bid_issue)
            votesevaluater = False
            for party in parties:
                if party!=bidding_party:
                    partyresponse = party.evaluate_bid_and_vote(current_bid,bid_issue,rounds)
                    if(partyresponse=="No"):
                        votesevaluater = False
                        break
                    else:
                        votesevaluater = True
            if(votesevaluater==True):
                print("Negotiation Successfull Offered by Party #",bidding_party.name)
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
    for partynames in range(1,number_of_parties+1):
        tempparty = Party(str(partynames),deadline)
        tempparty.setutilityspace(issues_list)
        parties.append(tempparty)
    #deadline = int(input("Enter the deadline : "))
    time.sleep(3)
    print("Starting Negotiation Protocol")
    Negotiation(deadline,parties)
if __name__ == '__main__':
    main()