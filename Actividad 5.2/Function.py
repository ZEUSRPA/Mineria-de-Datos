import pandas as pd
import numpy as np

class Function:
    def __init__(self) -> None:
        self.data=[]
        self.train_data=[]
        self.test_data=[]
        self.one_evaluation=0
        self.zero_evaluation=0
        

    def loadData(self,file):
        try:
            self.data=pd.read_csv(file)
            return 1
        except:
            return -1


    def split_data(self,data):
        pass
    
    #Chimi's function
    def zeroR(self,n):
        pass

    #Marijo's function
    def oneR(self,n):
        pass

    def evaluation(self):
        pass