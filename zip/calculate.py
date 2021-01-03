#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester, jeremy smith, and aditya nair
"""
import sys
import numpy as np
import scipy as sp
from scipy.integrate import odeint
from sindy_data import SindyData
import ThreatCalculator as threat
import calc_utils


# function to generate an approximation of the Nevada State metrics, specific to Washoe County
# see details at https://nvhealthresponse.nv.gov/
# param df, the pandas data frame containing all of the data needed
def nv_state_calculator(df):
    # test positivity
    test_pos = threat.ThreatCalculator(df, 'FactorPositivity', 14, False, 7)
    test_pos_metric = test_pos.to_percentage(test_pos.get_mean())

    #cases per 100,000
    cases_hundothou = threat.ThreatCalculator(df, 'dailyCases', 30, 4.78, 0)
    cases_hundothou_metric = cases_hundothou.normalize(cases_hundothou.get_sum())

    #number of tests adminstered
    num_tests = threat.ThreatCalculator(df, 'DailyTests', 14, 4.78, 7)
    num_tests_metric = num_tests.normalize(num_tests.get_mean())

    score = 0
    if num_tests_metric < 100:
        print("Testing criterion not met (there less than 100 per 100,000)")
        score+=1
    if cases_hundothou_metric > 200:
        print("Case rate criterion not met (there were > 200 per 100,000 cases)")
        score+=1
    if cases_hundothou_metric > 50 or test_pos_metric > 8.0:
        print("Third criterion not met (case rate was > 50 per 100,000 and/or test positivity was greater than 8%")
        score+=1
    if score >= 2:
        print("We do NOT meet the Nevada state threshold")
    else:
        print("We currently meet the Nevada state threshold")
    return num_tests_metric, cases_hundothou_metric, test_pos_metric


# function to generate metrics for truckee meadows website
# param df, the pandas data frame containing all of the data needed
# param returnForPredict true to return the metric objects to get data from for prediction
# TODO: add other params here
def metric_calcs(df, returnForPredict=False,
    test_schedule_params={'dataColumn': 'RiskAssess','avgPeriod': 14, 'cutoffs':[25,265,400]},
    test_pos_params={'dataColumn': 'FactorPositivity','avgPeriod':1, 'cutoffs':[0.03,0.07,0.12]}
    ):
    indSumList = []

    # 1. 14-day avg of COVID test scheduling
    #test_schedule = threat.ThreatCalculator(df, 'RiskAssess', 14)
    test_schedule = threat.ThreatCalculator(df, test_schedule_params['dataColumn'], test_schedule_params['avgPeriod'])
    test_schedule_clac = test_schedule.get_mean()
    indSumList.append(calc_utils.thresholdRanger(test_schedule_clac, test_schedule_params['cutoffs']))

    # 2. Previous day test positivity
    test_pos = threat.ThreatCalculator(df, test_pos_params['dataColumn'], test_pos_params['avgPeriod'])
    #test_pos = threat.ThreatCalculator(df, 'FactorPositivity', 1)
    indSumList.append(calc_utils.thresholdRanger(test_pos.select_data(1)[0], test_pos_params['cutoffs']))
    #indSumList.append(calc_utils.thresholdRanger(test_pos.get_mean(), [0.03,0.07,0.12]))
    #TODO: update when daily num available

    # 3. 7-day average of daily cases / 100,000
    case_rate = threat.ThreatCalculator(df, 'dailyCases', 7, 4.7)
    case_rate_calc = case_rate.normalize(case_rate.get_mean())
    indSumList.append(calc_utils.thresholdRanger(case_rate_calc, [1,9,25]))

    # 4a. % diffence of 7-day and 14-day average in hospitalizations due to covid...
    # ...divided by the 14-day average in hospitalizations due to covid
    # assigned 1/2 weight
    covid_hosp_rate = threat.ThreatCalculator(df, 'Total_COVID', 7)
    covid_hosp_calc = covid_hosp_rate.to_percentage(covid_hosp_rate.diff_avg_over_second_avg(14))
    #print(covid_hosp_calc)
    indSumList.append(0.5 * calc_utils.thresholdRanger(covid_hosp_calc, [-5,5,20]))

    # 4b. % diffence of 7-day and 14-day average in icu use due to covid...
    # ...divided by the 14-day average in icu use due to covid
    # assigned 1/2 weight
    covid_icu_use = threat.ThreatCalculator(df, 'COVID_ICU', 7)
    covid_icu_calc = covid_icu_use.to_percentage(covid_icu_use.diff_avg_over_second_avg(14))
    indSumList.append(0.5 * calc_utils.thresholdRanger(covid_icu_calc, [-5,5,20]))


    # 5a. % utilization of overall hospital beds, avg over 7 days
    # assigned 1/2 weight
    hosp_use = threat.ThreatCalculator(df, 'Inpatient', 7)
    hosp_use_calc = hosp_use.to_percentage(hosp_use.div_avgs('Staffed_Beds'))
    indSumList.append(0.5 * calc_utils.thresholdRanger(hosp_use_calc, [70,80,90]))


    # 5b. % utilization of overall icu beds, avg over 7 days
    # assigned 1/2 weight
    icu_use = threat.ThreatCalculator(df, 'ICU_Beds_Occ', 7)
    icu_use_calc = icu_use.to_percentage(icu_use.div_avgs('ICU_Beds'))
    indSumList.append(0.5 * calc_utils.thresholdRanger(icu_use_calc, [70,80,90]))

    grandScore = sum(indSumList)
    overall_cutoffs = [1,3,5,7,9,11,13]   # current breaks for threat score
    overall_threat = calc_utils.thresholdRangerThreat(grandScore,overall_cutoffs)
    #print("Threat color: "+overall_threat)

    if returnForPredict:
        return test_schedule, test_pos, case_rate, covid_hosp_rate, covid_icu_use, hosp_use, icu_use
    else:
        return indSumList, overall_threat, grandScore

def generate_predictions(df):
    # Predictive meter
    test_schedule, test_pos, case_rate, covid_hosp_rate, covid_icu_use, hosp_use, icu_use = metric_calcs(df, True)
    indSumList_preds, overall_thread_preds, grandScore_preds = [],[],[]

    # compile data to matrix
    x_data = np.array((test_schedule.data, test_pos.data, case_rate.data, covid_hosp_rate.data, covid_icu_use.data, hosp_use.data, icu_use.data))
    # differentiate data
    dx_data = calc_utils.differentiate(x_data, 1)
    # Datasets (number of days * number of variables)
    x = np.transpose(x_data)
    dx = np.transpose(dx_data)
    # Create regression object
    sindy_covid = SindyData(x[10:,:],dx[10:,:],2,calc_utils.polyLib)
    # Create polynomial basis functions
    Theta = sindy_covid.library(sindy_covid.X,sindy_covid.poly_order)
    # Regression coefficients
    sigma0 = np.linalg.lstsq(Theta,sindy_covid.dX,rcond=None)[0]
    # Simulate future data based on last day data (6-day prediction)
    x_pred = sindy_covid.simulate(sigma0,x[-1,:],list(range(0, 6)))
    #print(x_pred)
    #print(x_pred[5:,0])
    #print(x_pred[5:,0])

    for i in range(0,5):
        indSumList_pred = []
        # Predictive indicator variables
        test_schedule_pred = test_schedule
        test_schedule_pred.data = x_pred[i:,0]
        test_schedule_calc_pred = test_schedule.get_mean()
        indSumList_pred.append(calc_utils.thresholdRanger(test_schedule_pred.ols_line()[0], [25,265,400]))
        
        
        test_pos_pred = test_pos
        test_schedule_pred.data = x_pred[i:,1]
        indSumList_pred.append(calc_utils.thresholdRanger(test_pos_pred.select_data(1)[0], [0.03,0.07,0.12]))


        case_rate_pred = case_rate
        case_rate_pred.data = x_pred[i:,2]
        case_rate_calc_pred = case_rate_pred.normalize(case_rate_pred.get_mean())
        indSumList_pred.append(calc_utils.thresholdRanger(case_rate_calc_pred, [1,9,25]))

        covid_hosp_rate_pred = covid_hosp_rate
        covid_hosp_rate_pred.data = x_pred[i:,3]
        covid_hosp_calc_pred = covid_hosp_rate_pred.to_percentage(covid_hosp_rate_pred.diff_avg_over_second_avg(14))
        indSumList_pred.append(0.5 * calc_utils.thresholdRanger(covid_hosp_calc_pred, [-5,5,20]))

        covid_icu_use_pred = covid_icu_use
        covid_icu_use_pred.data = x_pred[i:,4]
        covid_icu_calc_pred = covid_icu_use_pred.to_percentage(covid_icu_use_pred.diff_avg_over_second_avg(14))
        indSumList_pred.append(0.5 * calc_utils.thresholdRanger(covid_icu_calc_pred, [-5,5,20]))


        hosp_use_pred = hosp_use
        hosp_use_pred.data = x_pred[i:,5]
        hosp_use_calc_pred = hosp_use.to_percentage(hosp_use_pred.div_avgs('Staffed_Beds'))
        indSumList_pred.append(0.5 * calc_utils.thresholdRanger(hosp_use_calc_pred, [70,80,90]))


        icu_use_pred = icu_use
        icu_use_pred.data = x_pred[i:,6]
        icu_use_calc_pred = icu_use_pred.to_percentage(icu_use_pred.div_avgs('ICU_Beds'))
        indSumList_pred.append(0.5 * calc_utils.thresholdRanger(icu_use_calc_pred, [70,80,90]))
        
        overall_cutoffs = [1,3,5,7,9,11,13]   # current breaks for threat score
        grandScore_pred = sum(indSumList_pred)
        overall_threat_pred = calc_utils.thresholdRangerThreat(grandScore_pred,overall_cutoffs)
        indSumList_preds.append(indSumList_pred)
        overall_thread_preds.append(overall_threat_pred)
        grandScore_preds.append(grandScore_pred)
        
    #return indSumList_pred, overall_threat_pred, grandScore_pred
    return indSumList_preds, overall_thread_preds, grandScore_preds