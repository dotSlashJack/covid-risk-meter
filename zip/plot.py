#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester
"""

import io_utils

# TODO: move this to a different util file
def get_dates(df, dateCol, nTimeSteps):
    dateList = []
    for i, row in df.iterrows():
        val = row[dateCol]
        dateList.append(val)
    selected_dates = dateList[len(dateList)-nTimeSteps:]
    date_strs = [d.strftime('%Y-%m-%d') for d in selected_dates] # convert timestamp objects to strings
    return date_strs

# WARNING: THE BELOW FUNCTIONS ARE DEPRECATED AND WILL BE REMOVED IN THE NEXT VERSION
"""
# tenmporary test function for plotting
# df is the data frame containing data we want to parse and generate plots of
# s3 is the s3_resource used to sync with the s3 bucket
def plot_test(df,s3):
    case_rate = threat.ThreatCalculator(df, 'dailyCases', 7)
    case_rate_output = case_rate.generateSummary(7)
    case_rate_plotter = plotter.Plotter(case_rate_output[0],["Case rate per 100,000","Date","Cases"])

    case_rate_plotter.bar_plot(case_rate_output[5])
    case_rate_plotter.add_mov_avg(3)
    case_rate_plotter.show_plot()
    case_rate_plotter.save_plot(saveName='testplot', aws=s3, bucket_name='covid-alert-graphics')

    case_rate_plotter.scatter_plot()
    case_rate_plotter.add_trend_line(case_rate_output[3],case_rate_output[4])
    case_rate_plotter.show_plot()
    case_rate_plotter.save_plot(saveName='testplot2', aws=s3, bucket_name='covid-alert-graphics')

# plot predictions in chart.js
# param df the df containing the dates (make sure they corresponds to df for other analysis)
# param nTimeSteps the number of dates/time steps back to get
# param dataPoints a list of data points to plot (y values)
# param outputFile the location of the output graph html (graph.js file), must include  .html extension
def plot_predictions(df, nTimeSteps, dataPoints, outputFile="chartjs.html"):
    dates = get_dates(df, 'Date', nTimeSteps)
    io_utils.fill_template("template.html", outputFile, ["/*labelList*/","/*dataPontList*/"], [dates, dataPoints])
    print("Your plot was successfully written to ", outputFile)
"""
