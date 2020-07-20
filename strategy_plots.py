import math
import matplotlib.pyplot as plt
def optimalbidder(rv,Deadline):
    ut = []
    ut.append(.25+.25*rv)
    for i in range(1,Deadline):
        ut.append(.25*math.pow(ut[i-1]+1,2))
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
    Deadline = 102
    utils = []
    for i in rv:
        utils.append(optimalbidder(i,Deadline))
        # utils.append(boulwareUtilities(i,Deadline))

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
    print(rvlist)
    print(ops)
    print("*********************TEST*******************************")
    print(test)
    plt.figure('AverageUtilities Tims')
    # plt.title('Optimal Bidder Utilities',fontsize=20, fontweight='bold')
    plt.title('Boulware Utilities',fontsize=14, fontweight='bold')
    font = {'weight' : 'bold','size'   : 13 }
    legend_properties = {'weight':'bold', 'size':10}
    # coefs = poly.polyfit(x, AverageUtilities_Tims, Tims_index)
    # ffit = poly.polyval(x,coefs)
    x = [i for i in range(Deadline)]
    x_2 = [i for i in range(1,Deadline+1)]
    Res,=plt.plot(x_2,rvlist, marker='o',linestyle='', color='r', linewidth=2, markersize=8)
    Tim,=plt.plot(x,ops, linestyle='-', color='k', linewidth=1.5)
    # Timfit,=plt.plot(x,ffit, linestyle='--', color='g', linewidth=2.5)
    plt.yticks(fontsize=14,fontweight='bold')
    plt.xticks(fontsize=14,fontweight='bold')
    # plt.legend([Res,Tim,Timfit],["Reservation Utilities","Optimal Bidder Utilities","Fitted Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    plt.legend([Res,Tim],["Reservation Utilities","Optimal Bidder Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    # plt.legend([Res,Tim],["Reservation Utilities","Boulware Utilities"],loc=6,ncol=1, handlelength=4,prop=legend_properties)
    plt.xlabel('Rounds',fontsize=14, fontweight='bold')
    plt.ylabel('Utilities',fontsize=14, fontweight='bold')
    plt.savefig('optimal_plot.pdf',format='pdf', dpi=1000)
    # plt.savefig('boulware_plot.pdf',format='pdf', dpi=1000)
    # plt.show()
        

#0 , 0.9 , 0.1 , 0.1 , 0.9 , 0.9,