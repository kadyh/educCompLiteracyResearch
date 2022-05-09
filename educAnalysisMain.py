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
    
    #%% Code Comp Lit survey
    # Code computer literacy based off of survey results and make new column w the new code
    dfCompLit=anFunc.codeCompLitSurvey(dfCompLit)
    # Bucket scores, create new column
    # Merge horizontally, if empty then NA
    
    #%% Count unique combos of completion
    
    
    #%% Combining the 3 DFs
    combinedDFwNA=handle.tripleJoinByNewKey(dfWS,dfCompLit,dfCODAP,'name','CompLit','CODAP')
    combinedDFwNA=combinedDFwNA.rename(columns={"scoreCompLit":"scoreWS"})
    # Create a new DF that drops rows with any NA
    combinedDFnoNA=combinedDFwNA.dropna()
    
    #%% Analysis between 3 DFs for perf scores
    #perf score dfs
    perfWS=dfWS[dfWS['score']==100]
    perfCODAP=dfCODAP[dfCODAP['score']==100]
    
    #merge codap scores w/ perf WS scores
    perfWSwCODAP=handle.tripleJoinByNewKey(perfWS,dfCompLit,dfCODAP,'name','CompLit','CODAP')
    perfWSwCODAP=perfWSwCODAP.rename(columns={"scoreCompLit":"scoreWS"})
    # Create a new DF that drops rows with any NA
    perfWSwCODAPnoNA=perfWSwCODAP.dropna()
    
    #merge perf codap scores w/ WS scores
    perfCODAPwWS=handle.tripleJoinByNewKey(dfWS, dfCompLit, perfCODAP, 'name', 'CompLit', 'CODAP')
    perfCODAPwWS=perfCODAPwWS.rename(columns={"scoreComplit":"scoreWS"})
    perfCODAPwWSnoNA=perfCODAPwWS.dropna()
    
    #perf all
    perfAll=handle.tripleJoinByNewKey(perfWS, dfCompLit, perfCODAP, 'name', 'CompLit', 'CODAP')
    perfAll=perfAll.rename(columns={"scoreComplit":"scoreWS"})
    perfAllnoNA=perfAll.dropna()
    
    #%% not perf 
    combinedDFnoNAnotPerf=combinedDFnoNA[~combinedDFnoNA.index.isin(perfAllnoNA.index.tolist())]
    
    #%% T tests 
    #pull the CODAP 0 
    zeroCODAPlist=combinedDFnoNA[combinedDFnoNA['scoreCODAP']==0].iloc[:,10]
    #pull CODAP 100
    perfCODAPlist=combinedDFnoNA[combinedDFnoNA['scoreCODAP']==100].iloc[:,10]
    #ttest
    ttestHours=scipy.stats.ttest_ind(zeroCODAPlist,perfCODAPlist)
    
    #pull both perf
    bothPerflist=perfAllnoNA.iloc[:,10].tolist()
    #pull non perf
    nonPerfList=combinedDFnoNAnotPerf.iloc[:,10].tolist()
    #t test perf vs non perf hours of comp usage
    ttestPerfvNonPerf=scipy.stats.ttest_ind(bothPerflist,nonPerfList)
   #%% Visuals
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

    #%%reindex
    anon1,anon2,anon3=handle.anonKeysSplit(combinedDFwNA,dfWS,dfCODAP,dfCompLit)
    
    
    #%% Histograms for T-Test

    histogramFirstTTest=plt.figure(3)
    plt.hist([zeroCODAPlist,perfCODAPlist],label=['Score of 0','Score of 100'])
    plt.legend()
    plt.xlabel('Hours Spent on Computer')
    plt.ylabel('Frequency')
    
    histogramFirstTTest=plt.figure(4)
    plt.hist([bothPerflist,nonPerfList],label=['Scored 100 on Both','Did Not Score 100 on Both'])
    plt.legend()
    plt.xlabel('Hours Spent on Computer')
    plt.ylabel('Frequency')
    
    from scipy.stats import t
    tDist=plt.figure(5)
    mean, var, skew, kurt = t.stats(zeroCODAPlist, moments='mvsk')
    x = np.linspace(t.ppf(0.01, zeroCODAPlist),
                t.ppf(0.99, zeroCODAPlist), 100)
    a=plt.plot(x, t.pdf(x, zeroCODAPlist),
                'r-', lw=1, alpha=0.1, label='T PDF for Score of 0')  
    rv = t(zeroCODAPlist)
    #plt.plot(x, rv.pdf(x), 'k-', lw=.5, label='frozen pdf')     
    mean, var, skew, kurt = t.stats(perfCODAPlist, moments='mvsk')
    x = np.linspace(t.ppf(0.01, perfCODAPlist),
                t.ppf(0.99, perfCODAPlist), 100)
    b=plt.plot(x, t.pdf(x, perfCODAPlist),
                'b-', lw=1, alpha=0.1, label='T PDF for Score of 100')  
    rv = t(perfCODAPlist)
    plt.axvline(x=0.41,color='k')
    plt.xlabel('Test Statistic')
    plt.ylabel('Probability')
    plt.legend(['T PDF for Score of 0','T PDF for Score of 100'])
    
    tDist=plt.figure(6)
    mean, var, skew, kurt = t.stats(bothPerflist, moments='mvsk')
    x = np.linspace(t.ppf(0.01, bothPerflist),
                t.ppf(0.99, bothPerflist), 100)
    a=plt.plot(x, t.pdf(x, bothPerflist),
                'r-', lw=1, alpha=0.1, label='T PDF for Perfect Scores on Both')  
    rv = t(bothPerflist)
    #plt.plot(x, rv.pdf(x), 'k-', lw=.5, label='frozen pdf')     
    mean, var, skew, kurt = t.stats(nonPerfList, moments='mvsk')
    x = np.linspace(t.ppf(0.01, nonPerfList),
                t.ppf(0.99, nonPerfList), 100)
    b=plt.plot(x, t.pdf(x, nonPerfList),
                'b-', lw=1, alpha=0.1, label='T PDF for Not Perfect Scores on Both')  
    rv = t(nonPerfList)
    plt.axvline(x=0.53,color='k')
    plt.xlabel('Test Statistic')
    plt.ylabel('Probability')
    plt.legend(['T PDF for Perfect Scores on Both','T PDF for Not Perfect Scores on Both'])
    #plt.plot(x, rv.pdf(x), 'k-', lw=.5, label='frozen pdf')     
                      
    return combinedDFwNA, combinedDFnoNA,dfCODAP,dfWS,dfCompLit,perfWSwCODAPnoNA,perfCODAPwWSnoNA,perfAllnoNA,combinedDFnoNAnotPerf,ttestHours,ttestPerfvNonPerf,anon1,anon2,anon3
    

    #%% reindex
    

if __name__ == "__main__":
    combinedDFwNA,combinedDFnoNA,dfCODAP,dfWS,dfCompLit,perfWSwCODAPnoNA,perfCODAPwWSnoNA,perfAllnoNA,combinedDFnoNAnotPerf,ttestHours,ttestPerfvNonPerf,anon1,anon2,anon3=main()

