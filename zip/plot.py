#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester
"""

import ThreatCalculator as threat
import Plotter as plotter

# tenmporary test functio for plotting
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
