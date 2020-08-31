#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 20:13:31 2020

@author: jack hester and jeremy smith
"""

import numpy as np

"""
Class ThreatCalculator
Includes several methods useful for generating COVID-19 prevalence, incidence, and trend statistics
***
param df, the pandas dataframe with all of the variables to be analyzed (import of excel/csv file)
param analysis_var, a string stating the column in the data table that will be analyzed
param interval, the time interval (e.g. # of days) to perform primary analysis over
param normalizer, optionally normalize against a value (useful for doing per cap, per 100,000 calcs)
param delay, optionally delay the beginning of your analysis window by n time steps (e.g., for 14 day avg with 7 day delay)
"""
class ThreatCalculator:
    def __init__(self, df, analysis_var, interval, normalizer=False, delay=0):
        self.df = df
        self.analaysis_var = analysis_var
        self.interval = interval
        self.normalizer = normalizer
        self.delay = delay
        dataList = []
        for i, row in df.iterrows():
            val = row[analysis_var]
            dataList.append(val)
        self.data = dataList
    
    
    # when you need to grab a secondary data set besides the one provided when the class is called
    # analysis_var is the variable  (column name) to sample data from, same as class init
    # may want to deprecate eventually...
    def create_data_list(self, analysis_var):
        dataList = []
        for i, row in self.df.iterrows():
            val = row[analysis_var]
            dataList.append(val)
        return dataList
    
    
    # daysBack is how many days worth of data to get, starting with current (latest) date    
    # starts n=delay days back if delay was provided during intialization
    # provide data to use if you need to analyze a separate data set from the one in class init
    # provide different delay from overall class delay if necessary
    def select_data(self, daysBack, data=False, delay=0):
        #dataList = self.create_data_list(self.analaysis_var)
        if not delay:
            delay = self.delay
        if data:
            selection = data[len(data)-(daysBack+delay):len(data)-delay]
        else:
            selection = self.data[len(self.data)-(daysBack+delay):len(self.data)-delay]
        return selection
    
    
    # returns dates with same indices in df as the overall data, useful for plot axes
    def get_dates(self):
        dates = self.create_data_list('Date')
        selected_dates = dates[len(dates)-self.interval:]
        date_strs = [d.strftime('%Y-%m-%d') for d in selected_dates] # convert timestamp objects to strings
        return date_strs
    
    
    # check if output should be percentage and if so convert values to percentage
    def to_percentage(self, value):
        value = value * 100
        return value
     
    
    # normalize value to per-capita value (e.g. per 100,000)
    # data is list of data to be normalized
    def normalize(self, value):
        if type(value) == 'list':
            adjusted_data = [v / self.normalizer for v in value]
            return adjusted_data
        else:
            return value / self.normalizer
    
    
    # get the mean of the data provided over the interval provided (at init)
    # otherwise get mean of data provided at init over alternate interval (interval)
    def get_mean(self, interval=0):
        if not interval:
            interval = self.interval
        return np.mean(self.select_data(interval))
    
    
    # calculate a moving average
    # data is a list containing the data to calculate on
    # interval is number of days you want to calculate average(s) over
    # returns a list of the moving averages for all applicable subsets of the data
    # normalize (optionally) divide by some denominator
    def moving_avg(self, interval):
        if self.normalizer:
            d = self.normalizer(self.data)
            data = d
        else: data = self.data
        length = len(data)
        i = 0
        moving_avgs = []
        while(i+interval<=length):
            subset = data[i:i+interval]
            avg = np.mean(subset)
            moving_avgs.append(avg)
            i += 1
        return moving_avgs
    
    # calculate the slope for an ordinary least squares line, generate a quasi-intercept
    # data is the list containing data to calculate on
    # interval is the number of days to use in analysis
    # normalize (optionally) divide by some denominator
    def ols_line(self):
        if self.normalizer:
            d = self.normalize(self.data)
            data = d
        else: data = self.data
        
        selected_data = self.select_data(self.interval)
        x = np.arange(len(selected_data))
        y = np.c_[selected_data]
        X = x-x.mean()
        Y = y - y.mean()
        coeff = (X.dot(Y) / (X.dot(X)))
        quasi_intercept =  selected_data = data[len(data)-1] # return a value that was the day before as a pseudo intercept value
        return coeff[0], quasi_intercept # coeff[0] is the "slope"
    

    # get the differences for all values in two data lists or 
    # subtracts second_sample data points from first_sample data points
    # or gets the difference between the means of two samples (lists) if ofMeans
    # or gets the differences of two values
    def difference(self, first_sample, second_sample, ofMeans=False):
        if (type(first_sample) == 'list' and type(second_sample) == 'list') and len(first_sample)==len(second_sample):
            differences = []
            for i in range(0, len(first_sample)):
                differences.append(first_sample[i] - second_sample[i])
            return differences
        elif ofMeans:
            return np.mean(first_sample) - np.mean(second_sample)
        else:
            return first_sample - second_sample
    
    # difference in means of two interval over the mean of the second interval
    # (typically second interval would be longer than the first)
    # second_interval is the second interval needed for analysis, first provided at init
    def diff_avg_over_second_avg(self, second_interval):
        first_mean = self.get_mean()
        second_mean = np.mean(self.select_data(second_interval))
        diff = self.difference(first_mean, second_mean)
        return diff / second_mean
        
    # divide the mean of the primary analysis variable (provided at init)...
    # ...by the mean of the secondary analysis var provided heres
    def div_avgs(self, second_analysis_var):
        first_mean = self.get_mean()
        second_data = self.select_data( self.interval, self.create_data_list(second_analysis_var) , 0)
        second_mean = np.mean(second_data)
        return first_mean / second_mean
    
    # calculate a summary of a moving average and slope
    # return the selected data (from relevant column, in order)
    # return the list of all moving averages
    # return the latest moving average
    # return the slope from ols
    # return the quasi-intercept
    # return the dates for the data (in order)
    def generateSummary(self,mov_avg_interval=7):
        #data = self.create_data_list(self.analaysis_var)
        selection = self.select_data(self.interval)
        slope, quasi_intercept = self.ols_line()[0:2]
        moving_avgs = self.moving_avg(mov_avg_interval)
        latest_moving_avg = moving_avgs[len(moving_avgs)-1]
        #if self.isPercentage:
        #    slope, quasi_intercept, latest_moving_avg = slope * 100, quasi_intercept * 100, latest_moving_avg *100
        #    [m * 100 for m in moving_avgs]
        return selection, moving_avgs, latest_moving_avg, slope, quasi_intercept, self.get_dates()
            
            
        

    

        