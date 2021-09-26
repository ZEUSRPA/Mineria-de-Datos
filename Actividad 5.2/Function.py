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
        if(testPercent==0 or testPercent==100):
            self.test_data=self.data
            self.train_data=self.data
        else:
            testAmount = len(self.data)*testPercent//100
            self.data=self.data.sample(frac=1)
            self.test_data = self.data[:testAmount]
            self.train_data = self.data[testAmount:]
    
    #Chimi's function
    def zeroR(self,clase = 'Clase'):
        #Encontramos el valor mas repetido
        valor = self.train_data[clase].mode().iloc[0]
        #Cuenta las veces que el nombre se repite
        radio = self.test_data[self.test_data.eq(valor).any(1)].count().max()
        #Numero de veces que aparece
        clases = self.test_data.groupby([clase]).size().max()
         #Numero total de registros
        total_registros = self.test_data.count().max()
        #Porcentaje aciertos a partir del promedio
        aciertos = (clases/total_registros)*100 
        #Porcentaje de erroes 
        errores = 100 - aciertos

        return aciertos
        #pass
        

    #Marijo's function
    def oneR(self,n):
        pass
    
    def evaluation(self,params):
        self.one_evaluation=[]
        self.zero_evaluation=[]
        zeroA=0
        oneA=0
        ok=False
        if params['Class'] in self.data:
            ok=True
            for i in range(0,params["repeatTimes"]):
                self.split_data(params["testPercent"])
                aux = self.zeroR(params['Class'])
                zeroA+=aux
                self.zero_evaluation.append(aux)
        zeroA=zeroA/params["repeatTimes"]
        ans = {"OK":ok,"zeroR":self.zero_evaluation,"oneR":self.one_evaluation,"zeroA":zeroA,"oneA":oneA}
        return ans
            