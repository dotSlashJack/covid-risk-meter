#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 15:57:50 2020

@author: jack
"""

import ThreatCalculator as threat
import Plotter as plotter

# selection, moving_avgs, latest_moving_avg, slope, quasi_intercept, self.get_dates()
def plot_test(df):
    case_rate = threat.ThreatCalculator(df, 'dailyCases', 7)
    case_rate_output = case_rate.generateSummary(7)
    case_rate_plotter = plotter.Plotter(case_rate_output[0],["Case rate per 100,000","Date","Cases"])
    
    case_rate_plotter.bar_plot(case_rate_output[5])
    case_rate_plotter.add_mov_avg(3)
    case_rate_plotter.show_plot()
    
    case_rate_plotter.scatter_plot()
    case_rate_plotter.add_trend_line(case_rate_output[3],case_rate_output[4])
    case_rate_plotter.show_plot()
    case_rate_plotter.save_plot(saveName='testplot', aws=True, bucket_name='covid-alert-graphics')
    #data, labels=['title','x_title','y_title']
