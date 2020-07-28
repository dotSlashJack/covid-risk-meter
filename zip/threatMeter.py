"""
    Script to calculate a risk gauge setting for COVID in Washoe County
    Written by Jeremy Smith and Jack Hester in conjunction with the City of Reno's Covid Response Committee
    Contact: jsmith@tmrpa.org
"""

import pandas as pd
import numpy as np

"""
    Supporting functions
"""

def thresholdRanger(perc,rL):
    if perc <= rL[0]:
        score = 0
    elif perc > rL[0] and perc <= rL[1]:
        score = 1
    elif perc > rL[1] and perc <= rL[2]:
        score = 2
    elif perc > rL[2]:
        score = 3
    return score

"""
    slices a series to return the specified number of days worth
    of data as a numpy array.  For instance values for the last week, 
    2 weeks, or month to analyze trends/slope over specified time period
"""
def getTimeSlice(arr, period):
    leng = len(arr)
    slice = leng - period
    newArr = arr[slice:]
    return newArr

"""
    slices a series to return the specified number of days worth
    of data as a numpy array.  Commences on the penultimate value
    to calc a previous period's average
"""
def getTimeSlicePre(arr, period):
    leng = len(arr)
    slice = leng - period
    newArr = arr[slice-1:]
    # remove last value
    leng2 = len(newArr)
    newArr = newArr[:leng2]
    return newArr


"""
    ScoreCalculator
    param df the pandas data frame containing metrics
    param metric the column name to get/use from the data frame (aka field name)
    param period the time period (in days) you want to analyze data over
    param rL the cutoffs for each category
    param metric2 (optionally) include a second metric to use in calculations, assumes same data frame for both
    period2 (optionally) include a second period in calculations
    param divBy (optionally) divide the mean by a number, useful for per capita calculation
"""
class ScoreCalculator:
    def __init__(self, df, metric, period, rL, metric2=None, period2=None, divBy=None):
        self.df = df
        self.metric = metric
        self.period = period
        self.rL = rL
        self.metric2 = metric2
        self.period2 = period2
        #self.differenceOrQuotient = differenceOrQuotient
        self.divBy = divBy or 1

    """ pulls a column from the excel sheet and turns it into a numpy array """
    def createDataList(self, fieldName):
        dList = []
        pd_df = self.df
        for index, row in pd_df.iterrows():
            val = row[fieldName]
            dList.append(val)
            arr = np.array(dList)
        return arr

    # calculate the score for each metric
    # return score, the score
    def getScore(self):
        if self.period2!=None:          # right now used to handle hospitalization and ICU bed usage
            series = self.createDataList(self.metric)
            avg = np.mean(series)
    
            slc = getTimeSlice(series, self.period)
            slcAvg = np.mean(slc)
            slc2 = getTimeSlice(series, self.period2)
            slc2Avg = np.mean(slc2)
            diff = slcAvg - slc2Avg
            perc = (diff/slc2Avg)*100
            
            score = thresholdRanger(perc,self.rL)
            score = score/2

        elif self.metric2!=None:        # right now used to handle hospital and ICU capacity
            series = self.createDataList(self.metric)
            series2 = self.createDataList(self.metric2)
    
            slc = getTimeSlice(series, self.period)
            slcAvg = np.mean(slc)
            slc2 = getTimeSlice(series2, self.period)
            slcAvg2 = np.mean(slc2)
            use = slcAvg2*100/(slcAvg)  # TODO: update this crude, case-specific multiplication by 100 implementation

            score = thresholdRanger(use,self.rL)
            score = score/2

        else:                           # handles all other metrics
            series = self.createDataList(self.metric)
            avg = np.mean(series)

            slc = getTimeSlice(series, self.period)
            slcAvg = np.mean(slc)

            val = slcAvg/self.divBy     # val is cases or test positivity
            score = thresholdRanger(val,self.rL)

        return score
