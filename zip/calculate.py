#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester and jeremy smith
"""
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
# param printList true to print the list of each score's value, false to not print
def metric_calcs(df, returnSumList=False):
    indSumList = []

    # 1. 14-day avg of COVID test scheduling
    test_schedule = threat.ThreatCalculator(df, 'RiskAssess', 14)
    test_schedule_clac = test_schedule.get_mean()
    indSumList.append(calc_utils.thresholdRanger(test_schedule_clac, [25,265,400]))

    # 2. Previous day test positivity
    test_pos = threat.ThreatCalculator(df, 'FactorPositivity', 1)
    #test_pos = threat.ThreatCalculator(df, 'FactorPositivity', 7)
    indSumList.append(calc_utils.thresholdRanger(test_pos.select_data(1)[0], [0.03,0.07,0.12]))
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

    if returnSumList:
        return indSumList, overall_threat, grandScore
    else:
        return overall_threat, grandScore
