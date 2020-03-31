import math
def boulwareUtilities (rv,Deadline):
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

def optimalbidder(rv,Deadline):
    ut = []
    ut.append(.5+.5*rv)
    for i in range(1,Deadline+1):
        ut.append(.5+.5*math.pow(ut[i-1],2))
    return ut
ut = boulwareUtilities(0,100)
ut2 = optimalbidder(0,100)
print(ut)
print(ut2)
