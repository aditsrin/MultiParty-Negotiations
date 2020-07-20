import math
def check(rv,Deadline=100):
    # ut = [0]*Deadline
    # ut[0] = rv
    # for i in range(1,100,1):
    #     ut[i] = .25*((ut[i-1]+1)**2)
    # ut.reverse()
    # print(ut)
    
    ut = []
    ut.append(.25+.25*rv)
    for i in range(1,Deadline):
        val = .25*math.pow(ut[i-1]+1,2)
        ut.append(val)
        # print(val)
    ut.reverse()
    print(ut)
check(0)