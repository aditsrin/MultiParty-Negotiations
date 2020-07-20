import numpy as np
import matplotlib.pyplot as plt
def calculateavg():
    updates = [2,5,10,20,50]
    y = []
    for update in updates:
        data = np.load('./MeetingResults/fiveagents/Boulware/Meeting_Results_Utils_'+str(update)+'.npy')
        # data = np.load('./MeetingResults/fiveagents/Optimal/Meeting_Results_Utils_'+str(update)+'.npy')
        y.append(np.mean(data,axis = 0))
        # print(np.mean(data,axis = 0))
    y = np.array(y)
    print("Final Average for Meeting Domain-Boulware Base",np.mean(y,axis = 0))
    # print("Final Average for Meeting Domain-Optimal Base",np.mean(y,axis = 0))
def percentageaverage():
    updates = [2,5,10,20,50]
    agents = ['bayesian','counter','lstm']
    avgs = []
    for j in range(len(agents)):
        x = [i for i in range(1,6)]
        y = []
        for update in updates:
            # data = np.load('./MeetingResults/fouragents/Boulware/Meeting_Results_Utils_'+str(update)+'.npy')
            data = np.load('./MeetingResults/fouragents/Optimal/Meeting_Results_Utils_'+str(update)+'.npy')
            y.append(np.mean(((data[:,j]-data[:,3])/data[:,3])*100))
        y = np.array(y)
        avgs.append(np.mean(y))
    # print("The average percentage comparison value for meeting domain boulware base is",avgs)
    print("The average percentage comparison value for meeting domain optimal base is",avgs)

def summary_table():
    updates = [2,5,10,20,50]
    agents = ['bayesian','counter','lstm']
    a = []
    b = []
    c = []
    d = []
    for update in updates:
        # data = np.load('./MeetingResults/fiveagents/Boulware/Meeting_Results_Utils_'+str(update)+'.npy')
        data = np.load('./MeetingResults/fiveagents/Optimal/Meeting_Results_Utils_'+str(update)+'.npy')
        a.append(data[:,0])
        b.append(data[:,1])
        c.append(data[:,2])
        d.append(data[:,3])
    a = np.mean(np.array(a))
    b = np.mean(np.array(b))
    c = np.mean(np.array(c))
    d = np.mean(np.array(d))
    print(a,b,c,d)
    avgs = ((a-b)/a)*100
    # print("The summary meeting domain boulware base is",avgs)
    print("The summary meeting domain optimal base is",avgs)

def plotfunctionality():
    updates = [2,5,10,20,50]
    # agents = ['bayesian','counter','lstm','optimal']
    # agents = ['bayesian','counter','lstm','boulware']
    colors = ['r','g','b','purple']
    styles = ['solid','dotted','dashdot','dotted']
    font = {'weight' : 'bold','size'   : 13 }
    markers = ['o','^','s','d']
    agents = ['bayesian','counter','lstm']
    # colors = ['r','g','b']
    # for update in updates:
    #     data = np.load('./MeetingResults/fouragents/Boulware/Meeting_Results_Utils_'+str(update)+'.npy')
    #     # data = np.load('./MeetingResults/fouragents/Optimal/Meeting_Results_Utils_'+str(update)+'.npy')
    #     # print(data.shape)
    #     for j in range(len(agents)):
    #         plt.title('UpdateRate: '+str(update))
    #         plt.plot(data[:,j],label=agents[j],c=colors[j])
    #     plt.legend(loc=1)
    #     plt.savefig('./MeetingResults/fouragents/Boulware/Util_plot_'+str(update))
    #     # plt.savefig('./MeetingResults/fouragents/Optimal/Util_plot_'+str(update))
    #     plt.close()
    points = [(9,2),(9,5),(9,10),(9,20),(9,50)]
    for j in range(len(agents)):
        x = [i for i in range(1,6)]
        y = []
        for update in updates:
            data = np.load('./MeetingResults/fouragents/Boulware/Meeting_Results_Utils_'+str(update)+'.npy')
            # data = np.load('./MeetingResults/fouragents/Optimal/Meeting_Results_Utils_'+str(update)+'.npy')
            y.append(np.mean(((data[:,j]-data[:,3])/data[:,3])*100))
        plt.plot(x,y,c=colors[j],label=agents[j],linestyle = styles[j],linewidth=6, markersize=12,marker=markers[j])
    legend_properties = {'weight':'bold', 'size':10}
    plt.legend(prop=legend_properties,bbox_to_anchor=(1,.8), loc=1)
    plt.xticks(x,points)
    plt.yticks(fontsize=10,fontweight='bold')
    plt.xticks(fontsize=10,fontweight='bold')
    plt.xlabel("Hypothesis,UpdateRate",**font)
    plt.ylabel("Average Percentage Utility",**font)
    # plt.title("% Utility Comparison for Meeting Domain-Boulware Base")
    # plt.title("% Utility Comparison for  Meeting Domain-Optimal Base")
    plt.savefig('./MeetingResults/fouragents/Boulware/Comparison_plot.pdf',format='pdf', dpi=500)
    # plt.savefig('./MeetingResults/fouragents/Optimal/Comparison_plot.pdf',format='pdf', dpi=500)


plotfunctionality()
# calculateavg()
# percentageaverage()
# summary_table()