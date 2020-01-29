from parties import Party
import numpy as np
def mydata():
    myparty = Party("lstm",100)
    tests = 1000
    rounds = 100
    updaterates = [2,5,10,20,50]
    for update in updaterates:
        data  = []
        for i in range(tests):
            rounddata = []
            flag = False
            for j in range(1,rounds+1):
                if(j%update==0 or j==1):
                    flag = True
                rounddata.append(myparty.checkupdate(flag,j,update))
            rounddata = np.array(rounddata)
            data.append(rounddata)
        data = np.array(data)
        filename = "LSTM/Meeting_Data_100_9hyp/Inputs/meeting_"+str(update)+".npy"
        np.save(filename,data)
mydata()
            
