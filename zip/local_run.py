#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester
Tool to locally run the metrics (covid metric, nevada state metric)
See arguments below in main or use `python local_run.py -h` to see argument structure
Example run: python local_run.py -x /Users/jack/Documents/covid-data/covidData.xlsx -m meter
"""
import argparse
import pandas as pd
import io
import calculate

def main():
    # ask user for excel file with data and which method/calculator to run  
    parser = argparse.ArgumentParser(description='Run the risk meter code locally (no need to use aws packages')
    parser.add_argument('-x','--excel',help='Path to the input excel (COVID data) table, e.g., /Users/jack/Desktop/covidData.xlsx', type=str)
    parser.add_argument('-m','--method', type=str, default="meter", help='Provide the calculator you want to use (meter for the covid meter, state for NV state calculator), default: covid meter calculations')
    args = parser.parse_args()

    df = pd.read_excel(args.excel, sheet_name='data')

    # run the covid meter calculations
    if args.method == "meter":
        sum_list, threat_color, total_score = calculate.metric_calcs(df, True)
        print("List of metric scores: ")
        print(sum_list)
        print("Overall (total) score: ")
        print(total_score)
        print("Overall color: ")
        print(threat_color)
        return sum_list, threat_color.lower(), total_score
    # run the nevada state metric calculator
    elif args.method == "state":
        num_tests_metric, cases_hundothou_metric, test_pos_metric = calculate.nv_state_calculator(df)
        return num_tests_metric, cases_hundothou_metric, test_pos_metric
    else:
        print("ERROR: invalid method provided")

if __name__ == '__main__':
    main()
