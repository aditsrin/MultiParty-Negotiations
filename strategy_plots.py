import math
import matplotlib.pyplot as plt
import sys
import numpy as np
def optimalbidder(rv,Deadline):
    ut = []
    ut.append(.25+.25*rv)
    for i in range(1,Deadline):
        ut.append(.25*math.pow(ut[i-1]+1,2))
    ut.reverse()
    return ut

def plots():
    data = np.load('checkdata.npy')
    # print(data[0,:])
    return data[2,:]

def onac(rv,Deadline):
    ut = []
    ut.append(rv)
    for i in range(1,Deadline):
        ut.append(math.pow((ut[i-1]+1)/2,2))
    ut.reverse()
    return ut

def boulwareUtilities (rv,Deadline):
    ut = []
    beta = 5
    beta = float(1)/beta
    for i in range(1,Deadline+1):
        minm = min(i,Deadline)
        time = float(minm)/Deadline
        curr_ut = rv + (1-rv)*(math.pow(time,beta))
        ut.append(float("{0:.4f}".format(curr_ut)))
    ut.reverse()
    return ut

if __name__ == '__main__':
    rv = [.1,.9]
    Deadline = 100
    utils = []
    for i in rv:
        # utils.append(optimalbidder(i,Deadline))
        # utils.append(boulwareUtilities(i,Deadline))
        utils.append(onac(i,Deadline))

    ops = []
    test = []
    j=1
    rvlist = []
    for i in range(1,Deadline+1):
        if(i%2==0):
            j+=1
        if(j%2==0):
            ops.append(utils[0][i-1])
            rvlist.append(rv[0])
        else:
            ops.append(utils[1][i-1])
            rvlist.append(rv[1])
        test.append(boulwareUtilities(rvlist[i-1],Deadline)[i-1])
    # ops = plots()
    print(rvlist)
    print(ops)
    print("*********************TEST*******************************")
    print(test)
    plt.figure('AverageUtilities Tims')
    # plt.title('Optimal Bidder Utilities',fontsize=20, fontweight='bold')
    # plt.title('Optimal Bidder Utilities',fontsize=14, fontweight='bold')
    plt.title('ONAC Utilities',fontsize=14, fontweight='bold')
    # plt.title('Bayesian Utilities',fontsize=14, fontweight='bold')
    font = {'weight' : 'bold','size'   : 13 }
    legend_properties = {'weight':'bold', 'size':10}
    # for m in range (1,19):
    m=5
    x = [i for i in range(Deadline)]
    x_2 = [i for i in range(1,Deadline+1)]
    coefs = np.polyfit(x,ops,m)
    print('ererere',coefs)
    ffit = np.polyval(coefs,x)
    Res,=plt.plot(x_2,rvlist, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
    Tim,=plt.plot(x,ops, linestyle='-', linewidth=1.5,color='black')
    fit, = plt.plot(x,ffit,linestyle='dashed',linewidth=1.5,color='green')
    # Timfit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=2.5)
    plt.yticks(fontsize=14,fontweight='bold')
    plt.xticks(fontsize=14,fontweight='bold')
    # plt.legend([Res,Tim,Timfit],["Reservation Utilities","Optimal Bidder Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    # plt.legend([Res,Tim],["Reservation Utilities","Optimal Bidder Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    plt.legend([Res,Tim],["Reservation Utilities","ONAC Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    # plt.legend([Res,Tim,fit],["Reservation Utilities","Optimal Bidder Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    plt.xlabel('Rounds',fontsize=14, fontweight='bold')
    plt.ylabel('Utilities',fontsize=14, fontweight='bold')
    # plt.savefig('optimal_plot.pdf',format='pdf', dpi=1000)
    # plt.savefig('optimal_plot.pdf',format='pdf', dpi=1000)
    plt.savefig('onac_plot_fit.pdf',format='pdf', dpi=1000)
    # plt.savefig('optimal_simple.pdf',format='pdf', dpi=1000)
    # plt.show()
    

#0 , 0.9 , 0.1 , 0.1 , 0.9 , 0.9,