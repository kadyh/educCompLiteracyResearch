# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 00:29:35 2022

@author: kdhsu24
"""
import pandas as pd
import numpy as np
from configparser import ConfigParser
import csv
import sys
sys.path.insert(0, '/Users/kadyh/Documents/GitHub/analysisAndHandlers/handlers.py')
from handlers import handlers

class analysisFunc:
    def __init__(self):
        # empty initialize
        a=1
        
    def codeCompLitSurvey(self,df):
        # the more hours spent on a device, the higher the computer litereacy,
        # however, time spent on a computer is more heavily weighted
        literacyScore=df['How many hours do you spend on a computer per day on average?']*2+df['How many hours do you spend on a tablet per day on average?']+df['How many hours do you spend on a smartphone per day on average?']
        df['literacyScore']=literacyScore
        df['literacyScoreCat']='0'
        for i in np.arange(len(df)):
            # 25th percentile or below
            if df['literacyScore'][i] <= np.percentile(df['literacyScore'],25):
                df['literacyScoreCat'][i]='0To25th'
            # 25th to 50th
            elif df['literacyScore'][i] > np.percentile(df['literacyScore'],25) and df['literacyScore'][i] <= np.percentile(df['literacyScore'],50):
                df['literacyScoreCat'][i]='25thTo50th'
            # 50th to 75th
            elif df['literacyScore'][i] > np.percentile(df['literacyScore'],50) and df['literacyScore'][i] <= np.percentile(df['literacyScore'],75):
                df['literacyScoreCat'][i]='50thTo75th'
            #75th and above
            elif df['literacyScore'][i] > np.percentile(df['literacyScore'],75): 
                df['literacyScoreCat'][i]='75thto100'
        return df