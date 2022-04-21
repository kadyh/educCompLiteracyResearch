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
sys.path.insert(0, '/Users/kadyh/Documents/GitHub/analysisAndHandlers/handlers.py')
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
    # Merge horizontally, if empty then NA
    
    # Save that as a DF
    
    # Create a new DF that drops rows with any NA
    
    # paired T tests 
     
    # Bucket scores, create new column
    
    # Graph: Scatter plot of computer literacy as a color on legend with paper vs codap activity scores
    
    # Graph: Scatter plot of computer literacy vs codap scores 
    
    # Graph: Distribution (histogram) of student performance on paper activity
    
    return dfCompLit,dfWS,dfCODAP
    

        

if __name__ == "__main__":
    dfCompLit,dfWS,dfCODAP=main()

