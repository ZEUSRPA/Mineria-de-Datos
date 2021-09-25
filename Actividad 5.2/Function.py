import pandas as pd
import numpy as np

class Function:
    def __init__(self) -> None:
        self.data=[]
        self.train_data=[]
        self.test_data=[]
        self.one_evaluation=[]
        self.zero_evaluation=[]
        

    def loadData(self,file):
        try:
            self.data=pd.read_csv(file)
            return 1
        except:
            return -1

    #Split data for train and test
    def split_data(self,testPercent):
        testAmount = len(self.data)*testPercent//100
        self.data=self.data.sample(frac=1)
        self.test_data = self.data[:testAmount]
        self.train_data = self.data[testAmount:]
    
    #Chimi's function
    def zeroR(self,n):
        pass

    #Marijo's function
    def oneR(self,n):
        pass
    
    def evaluation(self,params):
        for i in range(0,params["repeatTimes"]):
            self.split_data(params["testPercent"])
            