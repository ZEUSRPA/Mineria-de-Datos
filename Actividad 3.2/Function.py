from tkinter.constants import NUMERIC
from numpy.core.numeric import Inf
import pandas as pd
import numpy as np
import math
from pandas.api.types import is_numeric_dtype
from pandas.api.types import is_bool_dtype
from pandas.core.algorithms import mode
import math
#Clase que contiene las funciones para ejecutar la evaluacion con el algoritmo  KNN
class Function:
    #Constructor de la clase
    def __init__(self) -> None:
        """Constructor de la clase Function
        Parametros:Ninguno
        """
        self.data=[]
    #Funcion para cargar los datos desde un archivo csv
    def loadData(self,file):
        """Cargar archivo csv
        Parametros:
        file:string
            ruta del archivo a cargar
        """
        try:
            self.data=pd.read_csv(file)
            
            return 1
        except:
            return -1
    
    def preprocessing(self,target):
        self.categorical=[]
        self.numerical=[]

        for x in self.data.columns.tolist():
            if(dict(self.data.dtypes)[x]==np.object):
                self.categorical.append(x)
            else:
                self.numerical.append(x)
        # for x in self.data.columns.tolist():
        #     if(x!=target):
        #         if(self.data.at[0,x].lower()=="numérico" or self.data.at[0,x].lower()=="numerico"):
        #             self.numerical.append(x)
        #         else:
        #             self.categorical.append(x)
        #     else:
        #         if(self.data.at[0,x].lower()=="numérico" or self.data.at[0,x].lower()=="numerico"):
        #             self.targetType="numerical"
        #         else:
        #             self.targetType="categorical"
        # self.data=self.data.drop(self.data.index[[0]])
        # if(self.targetType=="numerical"):
        #     self.data[target]=self.data[target].astype(float)

        
        for x in self.categorical:
            self.data[x]=self.data[x].astype(object)
        for x in self.numerical:
            self.data[x]=self.data[x].astype(float)

        #Normalizar
        for x in self.numerical:
            maximo=self.data[x].loc[self.data[x].idxmax()]
            minimo=self.data[x].loc[self.data[x].idxmin()]
            
            for index,row in self.data.iterrows():
                self.data.at[index,x]=(row[x]-minimo)/(maximo-minimo)
       
    def crossTable(self,atrib,atrib2):
        contingency=pd.crosstab(self.data[atrib],self.data[atrib2])
        return contingency
    
    def crosstableCsv(self,atrib,atrib2):
        contingency=pd.crosstab(self.data[atrib],self.data[atrib2])
        return contingency
    
    def returnSum(self,contingency):
        auxcol=contingency.sum(axis=0) 
        auxrow=contingency.sum(axis=1)
        total=contingency.values.sum()
        return auxcol,auxrow,total
    
    def chiCuad(self,contingency):
        arr=contingency.to_numpy()
        auxcol,auxrow,total=self.returnSum(contingency)
        arr = arr.astype('float64')
        for x in range(len(arr)):
            for y in range(len(arr[x])):
                auxk=auxcol[y]*auxrow[x]/total
                arr[x][y]=auxk
        #print(arr)
        return arr
    
    def chiCuadrada(self,atr1,atr2):
        matrix=self.data
        contingency=self.crossTable(atr1,atr2)
        values=contingency.to_numpy()
        #print(contingency)
        arr2=values
        arr=self.chiCuad(contingency)
        sumi=0
        for x in range(len(arr2)):
            for y in range(len(arr2[x])):
                #print(arr[x][y])
                sumi+=((values[x][y]-arr[x][y])*(values[x][y]-arr[x][y]))/arr[x][y]
        
        return sumi,contingency
    
    def tschuprow(self,atr1,atr2):
        sumi,crosstable=self.chiCuadrada(atr1,atr2)
        #print(crosstable)
        arr=crosstable.to_numpy()
        arr = arr.astype('float64')
        total=crosstable.values.sum()
        c=len(arr)
        r=len(arr[0])
        p= sumi/(total*math.sqrt((c-1)*(r-1)))
        #print(sumi)
        return math.sqrt(p)

    #Funcion para ejecutar el algoritmo KNN
    def evaluation(self,params):
        """Ejecutar evaluacion con el algoritmo
        Parametros:
        params:dictionary
            file:string
                Indica el nombre del archivo
        """
        self.loadData(params['file'])
        self.preprocessing("-------")
        response=""
        #self.knn_evaluation=[]
        answers=[]
        
        for i in range(len(self.categorical)):
            for j in range(i+1,len(self.categorical)):
                response=""
                response+=self.categorical[i]+" -> "+self.categorical[j] + " = "
                response+=str(self.tschuprow(self.categorical[i],self.categorical[j]))+'\n'
                answers.append(response)
        ans = {"answers":answers}
        return ans


# a=Function()
# csv='play_db.csv'
# atr1='Windy'
# atr2='Play'
# chi=a.chiCuadruada(csv,atr1,atr2)
# print(chi)
# print(a.tschuprow(chi,a.crosstableCsv(csv,atr1,atr2)))
