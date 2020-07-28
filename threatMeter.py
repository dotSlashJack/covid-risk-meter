# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 11:20:18 2020

@author: Jeremy Smith for Mayor Schieve's COVID Task Force
script to calculate a risk gauge setting for COVID in Washoe County

"""
# import modules
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib
import matplotlib.pyplot as plt
import string as s
import traceback
import datetime
startTime = datetime.datetime.now()


xFile = r"C:\tmrpa\COVID\riskGauge\covidData.xlsx"
df = pd.read_excel(xFile, sheet_name='data')
##xlp = xl.parse('data')
##df = pd.DataFrame(xlp)

# create data handling module
def createDataList(dFrame,fieldName):
    """ pulls a column from the excel sheet and turns it into a numpy array """
    dList = []
    for index, row in dFrame.iterrows():
        val = row[fieldName]
        dList.append(val)
        arr = np.array(dList)
    return arr

def getTimeSlice(arr, period):
    """ slices a series to return the specified number of days worth
    of data as a numpy array.  For instance values for the last week, 
    2 weeks, or month to analyze trends/slope over specified time period """
    leng = len(arr)
    slice = leng - period
    newArr = arr[slice:]
    return newArr

def getTimeSlicePre(arr, period):
    """ slices a series to return the specified number of days worth
    of data as a numpy array.  Commences on the penultimate value
    to calc a previous period's average  """
    leng = len(arr)
    slice = leng - period
    newArr = arr[slice-1:]
    # remove last value
    leng2 = len(newArr)
    newArr = newArr[:leng2]
    return newArr

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

def thresholdRangerThreat(perc,rL):
    if perc <= rL[0]:
        score = "GREEN"
    elif perc > rL[0] and perc <= rL[1]:
        score = "YELLOW"
    elif perc > rL[1] and perc <= rL[2]:
        score = "ORANGE"
    elif perc > rL[2]:
        score = "RED"
    return score


def getDateRange(arr, dFrame):
    leng = len(arr)
    leng2 = len(dFrame)
    slice = leng2 - leng
    dateSeries = dFrame['Date']
    dateSeries = dateSeries[slice:]
    return dateSeries

def convertDateRangeToLabels(dateSeries):
    """ need to take the date series and turn it into a list of strings
    for labelling (I'm sure there is a better way ...) """
    dateList = []
    dates = np.array(dateSeries)
    for date in dates:
        d = str(date)
        dd = d[:10]
        dateList.append(dd)
    return dateList
                         

# list of field names (columns) in the covidData spreadsheet
fieldList = ["Date","Cases","DailyCases","Active","Recovered","Hospitalized","Deaths",
             "dailyCases", "dailyActive","dailyReco","dailyHosp","dailyDeaths",
             "Staffed_Beds","Inpatient","Occ_Staffed","ICU_Beds","ICU_Beds_Occ",
             "Perc_Occ_ICU", "Vent_Count","Vent_Occ","Perc_Vent_Occ","Conf_COVID",
             "Susp_COVID","COVID_ICU","COVID_Vent","COVID_HFNC","COVID_24","Total_COVID",
             "TestPositivity","DailyTests","Redundant"]

try:
    # initialize a list for holding the cumulative score
    indSumList = []


    # Indicator 1:  Cases per day, increase in 7-day average
    period = 7
    period2 = 14
    rL = [-5,5,25]

    series = createDataList(df, 'Cases')
    avg = np.mean(series)
    
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    slcPre = getTimeSlice(series, period2)
    slcPreAvg = np.mean(slcPre)
    diff = slcAvg - slcPreAvg
    perc = (diff/slcPreAvg)*100
    
    score = thresholdRanger(perc,rL)
    indSumList.append(score)


    # Indicator 2:  Test Positivity, WHO percentage guidelines
    period = 7
    rL = [5,10,20]

    series = createDataList(df, 'TestPositivity')
    avg = np.mean(series)
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)

    score = thresholdRanger(slcAvg,rL)
    indSumList.append(score)


    # Indicator 3:  Daily New Cases Per 100,000 People
    period = 7
    rL = [1,9,25]

    series = createDataList(df, 'Cases')
    avg = np.mean(series)
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    cases = slcAvg/4.7
    
    score = thresholdRanger(cases,rL)
    indSumList.append(score)


    # Indicator 4:  Deaths per day
    period = 7
    period2 = 14
    rL = [-5,5,25]

    series = createDataList(df, 'Deaths')
    avg = np.mean(series)
    
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    slcPre = getTimeSlice(series, period2)
    slcPreAvg = np.mean(slcPre)
    diff = slcAvg - slcPreAvg
    perc = (diff/slcPreAvg)*100
    
    score = thresholdRanger(perc,rL)
    indSumList.append(score)


    # Indicator 5:  Hospitalizations
    period = 7
    period2 = 14
    rL = [-5,5,25]

    series = createDataList(df, 'Total_COVID')
    avg = np.mean(series)
    
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    slcPre = getTimeSlice(series, period2)
    slcPreAvg = np.mean(slcPre)
    diff = slcAvg - slcPreAvg
    perc = (diff/slcPreAvg)*100
    
    score = thresholdRanger(perc,rL)
    indSumList.append(score)


    # Indicator 6:  Hospital Capacity
    period = 7
    rL = [70,80,85]

    series = createDataList(df, 'Staffed_Beds')
    series2 = createDataList(df, 'Inpatient')
    
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    slc2 = getTimeSlice(series2, period)
    slcAvg2 = np.mean(slc2)
    use = slcAvg2*100/(slcAvg)

    score = thresholdRanger(use,rL)
    indSumList.append(score)


    # Indicator 7:  ICU Bed Use
    period = 7
    period2 = 14
    rL = [-5,5,25]

    series = createDataList(df, 'COVID_ICU')
    avg = np.mean(series)
    
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    slcPre = getTimeSlice(series, period2)
    slcPreAvg = np.mean(slcPre)
    diff = slcAvg - slcPreAvg
    perc = (diff/slcPreAvg)*100
    
    score = thresholdRanger(perc,rL)
    indSumList.append(score)


    # Indicator 8:  ICU Capacity
    period = 7
    rL = [70,80,85]

    series = createDataList(df, 'ICU_Beds')
    series2 = createDataList(df, 'ICU_Beds_Occ')
    
    slc = getTimeSlice(series, period)
    slcAvg = np.mean(slc)
    slc2 = getTimeSlice(series2, period)
    slcAvg2 = np.mean(slc2)
    use = slcAvg2*100/(slcAvg)
    
    score = thresholdRanger(use,rL)
    indSumList.append(score)

    # Put it all together

    grandScore = sum(indSumList)
    rl = [3,9,14]
    threat = thresholdRangerThreat(grandScore,rl)
    print threat


except Exception, e: 
   tb = sys.exc_info()[2]
   tbinfo = traceback.format_tb(tb)[0] 
   pymsg = tbinfo + "\n" + str(sys.exc_type)+ ": " + str(sys.exc_value) 
   #arcpy.AddError("Python Messages: " + pymsg + " GP Messages: " + arcpy.GetMessages(2))
   tb = sys.exc_info()[2]
   print "I'm sorry Dave, I can't do that"
   print "Line %i" % tb.tb_lineno
   print e.message
   #print arcpy.GetMessages()
   print "messed up!"