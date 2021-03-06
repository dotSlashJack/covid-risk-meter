#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester
"""
import matplotlib.pyplot as plt
import numpy as np
import boto3
import io
from boto3.dynamodb.conditions import Key

"""
Class Plotter
Generate bar and scatter plots based on data lists and add trendlines using OLS and moving averages
***
param data, a list of the data points to plot
param lables, a list of axis and plot titles in the order of [title, x-axis title, y-axis title]
"""
class Plotter:
    def __init__(self, data, labels=['title','x_title','y_title']):
        self.data = data
        self.labels = labels
        #self.plot = plt.plot()

    # generate list of moving averages (same as in threatFunctions.py)
    def calc_mov_avg(self, data, interval):
        length = len(data)
        i = 0
        moving_avgs = []
        while(i+interval<=length):
            subset = data[i:i+interval]
            avg = np.mean(subset)
            moving_avgs.append(avg)
            i += 1
        return moving_avgs


    # generate a scatterplot of the data provided to this class
    def scatter_plot(self):
        x = np.linspace(1, len(self.data), len(self.data))
        plt.plot(x, self.data, 'o', color='black')
        plt.title(self.labels[0])
        plt.xlabel(self.labels[1])
        plt.ylabel(self.labels[2])

    # create a barplot wih data provided to this class, also requires labesl for each bar
    # xlabs a tuple or array of the bar labels, in order (for the x-axis)
    def bar_plot(self, xlabs=()):
        y_pos = np.arange(len(xlabs))
        plt.bar(y_pos, self.data, align='center', alpha=0.5)
        plt.title(self.labels[0])
        plt.xlabel(self.labels[1])
        plt.ylabel(self.labels[2])
        return plt

    # add moving averages line, initial points are point means until enough points to calculate proper moving average
    # interval is period over which to calculate the moving average
    def add_mov_avg(self, interval):
        length = len(self.data)
        x = np.linspace(0, length-1, length)
        if interval == length:
            print('WARNING: you have selected a period for your moving average that is the same as the number of days!')
            mov_avgs = []
            for i in range(0,interval):
                mov_avgs.append(self.data[i])
        elif interval > length:
            print("ERROR: your moving average period is longer than your analysis period")
            return None
        else:
            mov_avgs = self.calc_mov_avg(self.data,interval)
            for i in range(0,interval-1):
                mov_avgs.insert(0,self.data[(length%interval)-i]) #add in leading values before average first exists
            print("NOTE: the first "+str((length%interval)+1)+" point(s) on the moving average line are point averages not moving averages")
        plt.plot(x, mov_avgs, '-o', color='orange')


    # add linear trendline to existing plot
    # slope (flot or int) the slope of the trendline to add
    # slope (float or int) the intercept of the trendline to add
    def add_trend_line(self, slope, intercept):
        x = np.linspace(0,len(self.data),500)
        y = slope*x+intercept
        plt.plot(x, y, '-r')

    def show_plot(self):
        plt.show()

    # save the generated plot locally or to AWS s3 bucket
    # saveName string of what to save file as EXCLUDING .png, otherwise None
    # aws a boto3 resource (e.g. s3=boto3.resource('s3)) to save to AWS s3 bucket, otherwise False
    # bucket name a string of the bucket to save to if using aws, otherwise None
    def save_plot(self, saveName=None, aws=False, bucket_name=None):
        # TODO: update this for AWS lambda
        if aws:
            filename = saveName+'.png'

            img_data = io.BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)

            object = aws.Object(bucket_name, filename)
            object.put(Body=img_data,ACL='public-read')
            #s3_resource.ObjectAcl('covid-alert-graphics', 'current_code/current_metric.png',ACL='public-read')

            plt.close('all')
        else:
            plt.savefig(saveName)
            plt.close('all')
