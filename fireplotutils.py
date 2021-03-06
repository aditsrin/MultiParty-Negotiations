import numpy as np
import matplotlib.pyplot as plt

def calculateavg():
    updates = [2,5,10,20,50]
    y = []
    for update in updates:
        data = np.load('./Results/fiveagents/Boulware/Fire4_Results_Utils_'+str(update)+'.npy')
        # data = np.load('./Results/fiveagents/Optimal/Fire2_Results_Utils_'+str(update)+'.npy')
        y.append(np.mean(data,axis = 0))
        # print(np.mean(data,axis = 0))
    y = np.array(y)
    print("Final Average for Fire Domain(4 HYP)-Boulware Base",np.mean(y,axis = 0))
    # print("Final Average for Fire Domain(2 HYP)-Optimal Base",np.mean(y,axis = 0))
def percentageaverage():
    updates = [2,5,10,20,50]
    agents = ['bayesian','counter','lstm']
    avgs = []
    for j in range(len(agents)):
        x = [i for i in range(1,11)]
        y = []
        for update in updates:
            data = np.load('./Results/fouragents/Boulware/Fire2_Results_Utils_'+str(update)+'.npy')
            # data = np.load('./Results/fouragents/Optimal/Fire2_Results_Utils_'+str(update)+'.npy')
            y.append(np.mean(((data[:,j]-data[:,3])/data[:,3])*100))
        for update in updates:
            data = np.load('./Results/fouragents/Boulware/Fire4_Results_Utils_'+str(update)+'.npy')
            # data = np.load('./Results/fouragents/Optimal/Fire4_Results_Utils_'+str(update)+'.npy')
            y.append(np.mean(((data[:,j]-data[:,3])/data[:,3])*100))
        y = np.array(y)
        avgs.append(np.mean(y))
    print("The average for fire domain with boulware base is",avgs)
    # print("The average for fire domain with optimal base is",avgs)
def summary_table():
    updates = [2,5,10,20,50]
    agents = ['bayesian','counter','lstm']
    a = []
    b = []
    c = []
    d = []
    for update in updates:
        # data = np.load('./Results/fiveagents/Boulware/Fire2_Results_Utils_'+str(update)+'.npy')
        data = np.load('./Results/fiveagents/Optimal/Fire2_Results_Utils_'+str(update)+'.npy')
        a.append(data[:,0])
        b.append(data[:,1])
        c.append(data[:,2])
        d.append(data[:,3])
    for update in updates:
        # data = np.load('./Results/fiveagents/Boulware/Fire4_Results_Utils_'+str(update)+'.npy')
        data = np.load('./Results/fiveagents/Optimal/Fire4_Results_Utils_'+str(update)+'.npy')
        a.append(data[:,0])
        b.append(data[:,1])
        c.append(data[:,2])
        d.append(data[:,3])

    a = np.mean(np.array(a))
    b = np.mean(np.array(b))
    c = np.mean(np.array(c))
    d = np.mean(np.array(d))
    print(a,b,c,d)
    avgs = ((a-c)/a)*100
    # print("The summary for boulware base is",avgs)
    print("The summary for optimal base is",avgs)

def predplots():
    agents = ['BLRA','COUNTER','LSTM']
    colors = ['r','g','b']
    styles = ['solid','dotted','dashed']
    markers = ['o','^','s']
    font = {'weight' : 'bold','size'   : 13 }
    points = [(2,2),(2,5),(2,10),(2,20),(2,50),(4,2),(4,5),(4,10),(4,20),(4,50)]
    avgs = [[0.16765498, 0.19050088, 0.19295727],[0.15674722, 0.17759151, 0.18926029],[0.14929814, 0.15338959, 0.19787798],[0.12962711, 0.13917208, 0.19746076],[0.10904703, 0.12053593, 0.1061228 ],[0.17341154, 0.18929071, 0.19347113], [0.17315517, 0.18220992, 0.1902073 ],[0.14276764, 0.15835184, 0.17231169],[0.13268595, 0.14038879, 0.19169707],[0.1172383 , 0.10894593, 0.12060645]]
    sums = []
    x = [i for i in range(1,11)]
    for j in range(3):
        y = []
        for k in avgs:
            y.append(k[j])
        plt.plot(x,y,c=colors[j],label=agents[j],linestyle = styles[j],linewidth=3, markersize=6,marker=markers[j])
        print(agents[j],np.mean(y))
    legend_properties = {'weight':'bold', 'size':10}
    plt.legend(prop=legend_properties,bbox_to_anchor=(0.3,.3), loc=1)
    plt.xticks(x,points)
    plt.yticks(fontsize=10,fontweight='bold')
    plt.xticks(fontsize=10,fontweight='bold')
    plt.xlabel("Hypothesis,UpdateRate",**font)
    plt.ylabel("Average Prediction Values",**font)
    # plt.show()
    plt.savefig('prediction_plot_fire_avg_70_30.pdf',format='pdf', dpi=500)
def plotfunctionality():
    updates = [2,5,10,20,50]
    # agents = ['BLRA','COUNTER','LSTM','BOULWARE']
    agents = ['BLRA','COUNTER','LSTM','OPTIMAL']
    # agents = ['BLRA','COUNTER','LSTM']
    colors = ['r','g','b','purple']
    styles = ['solid','dotted','dashdot','dashed']
    markers = ['o','^','s','d']
    w = [12,10,8]
    # colors = ['r','g','b']
    # agents.reverse()
    # colors.reverse()
    x = [i for i in range(1,11)]
    y = []
    points = [(2,2),(2,5),(2,10),(2,20),(2,50),(4,2),(4,5),(4,10),(4,20),(4,50)]
    font = {'weight' : 'bold','size'   : 13 }
    
    # for update in updates:
    #     # data = np.load('./Results/Fire_Results_Utils_'+str(update)+'.npy')
    #     # data = np.load('./Results/fouragents/Boulware/Fire4_Results_Utils_'+str(update)+'.npy')
    #     data = np.load('./Results/fouragents/Optimal/Fire2_Results_Utils_'+str(update)+'.npy')
    #     for j in range(len(agents)):
    #         plt.plot(data[:,j],c=colors[j],label=agents[j])
    #     plt.legend(loc=1)
    #     plt.title("Update: "+str(update))
    #     plt.savefig('./Results/fouragents/Optimal/Fire2_Utils_'+str(update)+'.png')
    #     plt.close()

    for j in range(len(agents)):
        x = [i for i in range(1,11)]
        y = []
        for update in updates:
            data = np.load('./Results/fiveagents/Boulware/Fire2_Results_Utils_'+str(update)+'.npy')
            print('hre',data.shape)
            # data = np.load('./Results/fiveagents/Optimal/Fire2_Results_Utils_'+str(update)+'.npy')
            y.append(np.mean(((data[:,j]-data[:,4])/data[:,4])*100))
        for update in updates:
            data = np.load('./Results/fiveagents/Boulware/Fire4_Results_Utils_'+str(update)+'.npy')
            # data = np.load('./Results/fiveagents/Optimal/Fire4_Results_Utils_'+str(update)+'.npy')
            y.append(np.mean(((data[:,j]-data[:,4])/data[:,4])*100))
        # plt.scatter(x,y,c=colors[j],marker=markers[j],linewidth=6, markersize=12)
        plt.plot(x,y,c=colors[j],label=agents[j],linestyle = styles[j],linewidth=3, markersize=6,marker=markers[j])
    legend_properties = {'weight':'bold', 'size':10}
    plt.legend(prop=legend_properties,bbox_to_anchor=(1,.85), loc=1)
    plt.xticks(x,points)
    plt.yticks(fontsize=10,fontweight='bold')
    plt.xticks(fontsize=10,fontweight='bold')
    # plt.title("% Utility Comparison for Fire Domain-Optimal Base")
    # plt.title("% Utility Comparison Plot for Fire Domain-Boulware Base")
    plt.xlabel("Hypothesis,UpdateRate",**font)
    plt.ylabel("Average Percentage Utility",**font)
    # plt.savefig('./Results/fiveagents/Optimal/Comparison_plot.pdf',format='pdf', dpi=500)
    plt.savefig('./Results/fiveagents/Boulware/Comparison_plot.pdf',format='pdf', dpi=500)

# plotfunctionality()
# calculateavg()
# percentageaverage()
# summary_table()
predplots()