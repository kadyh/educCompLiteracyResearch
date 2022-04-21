# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 23:15:27 2022

@author: kdhsu24
"""
#%% Import
import pandas as pd
import numpy as np
from configparser import ConfigParser
import csv
import sys
import matplotlib.pyplot as plt
sys.path.append(r'C:\Users\kadyh\Documents\GitHub\analysisAndHandlers')
from handlers import handlers
from analysisFunc import analysisFunc
#%% Initialize
def main():
    pathCompLit=r'C:\Users\kadyh\Downloads\EDUC C122 Independent Research Project I Hsu - computerLiteracyData.csv'
    pathWS=r'C:\Users\kadyh\Downloads\EDUC C122 Independent Research Project I Hsu - worksheetData.csv'
    pathCODAP=r'C:\Users\kadyh\Downloads\EDUC C122 Independent Research Project I Hsu - codapActivityData.csv'
    handle=handlers()   
    anFunc=analysisFunc()
    #%% Actions
    # Load files into DFs
    dfCompLit=handle.pullReadCSV(pathCompLit)
    dfWS=handle.pullReadCSV(pathWS)
    dfCODAP=handle.pullReadCSV(pathCODAP)
    # Select important columns
    dfCompLit=dfCompLit.iloc[:,1:12]
    dfWS=dfWS.iloc[:,:9]
    dfCODAP=dfCODAP.iloc[:,:9]
    # Code computer literacy based off of survey results and make new column w the new code
    dfCompLit=anFunc.codeCompLitSurvey(dfCompLit)
    # Bucket scores, create new column
    # Merge horizontally, if empty then NA
    combinedDFwNA=handle.tripleJoinByNewKey(dfWS,dfCompLit,dfCODAP,'name','CompLit','CODAP')
    combinedDFwNA=combinedDFwNA.rename(columns={"scoreCompLit":"scoreWS"})
    # Create a new DF that drops rows with any NA
    combinedDFnoNA=combinedDFwNA.dropna()
    # paired T tests 
     
   
    # Graph: Scatter plot of computer literacy vs codap scores 
    scatterCompLitvCODAP=plt.figure(1)
    plt.scatter(combinedDFnoNA['literacyScore'],combinedDFnoNA['scoreCODAP'])
    plt.xlabel('Computer Literacy Score')
    plt.ylabel('CODAP Scores')
    # Graph: Scatter plot of computer literacy as a color on legend with paper vs codap activity scores
    scatterPapervCODAP=plt.figure(2)
    colors = {'75thto100':'red', '50thTo75th':'orange', '25thTo50th':'green', '0To25th':'blue'}
    freqCols=combinedDFnoNA[['scoreWS','scoreCODAP','literacyScoreCat']]
    freqGrouped=freqCols.groupby(['scoreWS','scoreCODAP']).transform(len)
   
    freqGrouped=freqCols.groupby(['scoreWS','scoreCODAP']).transform(len)
    plt.scatter(combinedDFnoNA['scoreWS'],combinedDFnoNA['scoreCODAP'], c=combinedDFnoNA['literacyScoreCat'].map(colors),s=freqGrouped*10)
    plt.xlabel('WS Score')
    plt.ylabel('CODAP Scores')

    return combinedDFwNA, combinedDFnoNA
    

        

if __name__ == "__main__":
    combinedDFwNA,combinedDFnoNA=main()

