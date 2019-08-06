   #######################################################
    means_offers=[]
    gamma=[]
    new_gamma=[]
    new_probability=[]
    new_belief_plots=[]

    intervals = len(random_rv)

    x=[]
    for i in xrange(1,Deadline+1):
        x.append(i)

    x_belief=[]
    for i in xrange(0,Deadline+1):
        x_belief.append(i)

    for i in xrange(0,intervals):
        gamma.append(0)
        new_gamma.append(0)
        new_belief_plots.append([0])
        new_probability.append(float("{0:.4f}".format(float(1)/intervals)))
        new_belief_plots[i][0]=new_probability[i]

    total = 0

    Utilities=[]
    actual_utility=[]
    new_WeightedUtility=[]

    offers=[]
    mean1_RV=0

    for rv in random_rv:
        Utilities.append(GenerateTimUtility(rv,Deadline))     ######   ----> Tims
        # Utilities.append(boulwareUtilities(rv,Deadline))        ######   -----> Boulware

    ####################################################################