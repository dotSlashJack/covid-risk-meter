#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester
Tool to locally run the metrics (covid metric, nevada state metric)
See arguments below in main or use `python local_run.py -h` to see argument structure
Example run: python local_run.py -x /Users/jack/Documents/covid-data/covidData.xlsx -m meter
If no agruments are provided, a GUI will open
"""
import argparse
import pandas as pd
import io
import calculate
import plot
import sys
import GUI as gui
import tkinter as tk


# run the covid meter calculations
def print_meter_output(df):
    sum_list, threat_color, total_score = calculate.metric_calcs(df)
    print("List of metric scores: ")
    print(sum_list)
    print("Overall (total) score: ")
    print(total_score)
    print("Overall color: ")
    print(threat_color)
    return sum_list, threat_color.lower(), total_score


# run the nevada state metric calculator
def print_state_output(df):
    num_tests_metric, cases_hundothou_metric, test_pos_metric = calculate.nv_state_calculator(df)
    return num_tests_metric, cases_hundothou_metric, test_pos_metric


# run predictive tool
def run_predctive_meter(df):
    indSumList_preds, overall_threat_preds, grandScore_preds = calculate.generate_predictions(df)
    print("Lists of metric scores: ")
    print(indSumList_preds)
    print("Overall (total) scores: ")
    print(grandScore_preds)
    print("Overall colors: ")
    print(overall_threat_preds)


# run selected methods/tools (from GUI)
def run_selected_tools(excel_file, run_meter, run_predictive, run_state):
    if excel_file.get()=="No excel file selected" or len(excel_file.get()) < 6:
        print("You haven't provided an excel file, so we cannot run any calculations!\nPlease select your excel file and try again.")
        return
    try:
        df = pd.read_excel(str(excel_file.get()), sheet_name="data")
    except:
        print("There was an error reading your excel file. Please make sure you have all of the necessary columns in a sheet titled \"data\"!")
        return
    if run_meter.get() == 1:
        print_meter_output(df)
    if run_predictive.get() == 1:
        run_predctive_meter(df)
    if run_state.get() == 1:
        print_state_output(df)


# build  GUI using tkinter if the user does not provide arguments via the command line
def build_gui():
    window = gui.GUI("Truckee Meadows COVID Meter GUI",dims=[500,150])
    welcome = window.add_label('Locate your excel file, select the desired routines below, then click RUN.', pack=False)[0]
    welcome.grid(row=0, column=1)

    run_meter = tk.IntVar()
    meter_check = window.add_checkbox(text="Risk Meter", var=run_meter, pack=False)
    meter_check.grid(row=2, column=0)

    run_predictive = tk.IntVar()
    predictive_check = window.add_checkbox(text="Predictive Tool", var=run_predictive, pack=False)
    predictive_check.grid(row=2, column=1)

    run_state = tk.IntVar()
    predictive_check = window.add_checkbox(text="Run Nevada Criteria Tool", var=run_state, pack=False)
    predictive_check.grid(row=2, column=2)
    
    blank_filename = "No excel file selected"
    select_lab, selected_excel =  window.add_label("No excel file selected", pack=False)
    selected_file = window.add_button("Select Excel File", lambda: window.add_file_dialogue(text_field=selected_excel), dims=False, pack=False)
    selected_file.grid(row=1, column=0)

    select_lab.grid(row=1, column=1)

    close = window.add_button("QUIT", window.close_window, dims=False, pack=False)
    close.grid(row=3, column=1)

    run = window.add_button("RUN", lambda: run_selected_tools(selected_excel, run_meter, run_predictive, run_state) , dims=False, pack=False)
    run.grid(row=3, column=0)
    window.build_gui()


def main():
    # ask user for excel file with data and which method/calculator to run  
    parser = argparse.ArgumentParser(description='Run the risk meter code locally via GUI or from the command line')
    parser.add_argument('-x','--excel',help='Path to the input excel (COVID data) table, e.g., /Users/jack/Desktop/covidData.xlsx', type=str)
    parser.add_argument('-m','--method', type=str, default="meter", help='Provide the calculator you want to use (meter for the covid meter, state for NV state calculator), default: covid meter calculations')
    
    args = parser.parse_args()
    if(len(sys.argv) < 2):# no args provided, run GUI
        build_gui()
        print(run_meter)
    
    else: # args provided, run using CLIs
        df = pd.read_excel(args.excel, sheet_name='data')
        if args.method == "meter":
            return print_meter_output(df)
        elif args.method == "state":
            return print_state_output(df)
        elif args.method == "predict":
            return run_predctive_meter(df)
        else:
            print("ERROR: invalid method provided")


if __name__ == '__main__':
    main()
