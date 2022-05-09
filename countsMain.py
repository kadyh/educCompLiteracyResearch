# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:29:32 2022

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
import scipy.stats
#%% Initialize
def main():
    pathCompLit=r'C:\Users\kadyh\Downloads\EDUC C122 Independent Research Project I Hsu - computerLiteracyData.csv'
    pathWS=r'C:\Users\kadyh\Downloads\EDUC C122 Independent Research Project I Hsu - worksheetData.csv'
    pathCODAP=r'C:\Users\kadyh\Downloads\EDUC C122 Independent Research Project I Hsu - codapActivityData.csv'
    handle=handlers()   
    anFunc=analysisFunc()
    #%% Set Up
    # Load files into DFs
    dfCompLit=handle.pullReadCSV(pathCompLit)
    dfWS=handle.pullReadCSV(pathWS)
    dfCODAP=handle.pullReadCSV(pathCODAP)
    # Select important columns
    dfCompLit=dfCompLit.iloc[:,1:12]
    dfWS=dfWS.iloc[:,:9]
    dfCODAP=dfCODAP.iloc[:,:9]

    
    #%% Count unique combos of completion
    CODAP_WS=handle.doubleJoinByNewKey(dfWS, dfCODAP, 'name','CODAP').dropna()
    swapCODAPWS=handle.doubleJoinByNewKey(dfCODAP, dfWS, 'name','CODAP').dropna()
    CODAP_CLS=handle.doubleJoinByNewKey(dfCODAP, dfCompLit, 'name','CompLit').dropna()
    swapCODAPCLS=handle.doubleJoinByNewKey(dfCompLit, dfCODAP, 'name','CompLit').dropna()
    WS_CLS=handle.doubleJoinByNewKey(dfWS, dfCompLit, 'name','CompLit').dropna()
    swapWSCLS=handle.doubleJoinByNewKey(dfCompLit, dfWS, 'name','CompLit').dropna()
    
    
    return CODAP_WS,CODAP_CLS,WS_CLS,swapCODAPWS,swapCODAPCLS,swapWSCLS

        
if __name__ == "__main__":
    CODAP_WS,CODAP_CLS,WS_CLS,swapCODAPWS,swapCODAPCLS,swapWSCLS=main()

