#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nevada DHHS data table collection

Created on Sat Jul 18 16:08:14 2020

@author: jack
"""

from tabula import read_pdf
import datetime as dt
import subprocess
import calendar
import time


today = dt.date.today()
execute_applescript = ['osascript', '/Users/jack/covid-alert/misc/Washoe_DHHS.scpt']
# calls external script that downloads ms power bi website as pdf
# gets data from https://app.powerbigov.us/view?r=eyJrIjoiMjA2ZThiOWUtM2FlNS00MGY5LWFmYjUtNmQwNTQ3Nzg5N2I2IiwidCI6ImU0YTM0MGU2LWI4OWUtNGU2OC04ZWFhLTE1NDRkMjcwMzk4MCJ9&pageName=ReportSection2ef293f74a403d042100
process = subprocess.Popen(execute_applescript,
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout, stderr)

time.sleep(2) # extra buffer just in case

# convert the pdf to a table
input_pdf = "/Users/jack/Downloads/Washoe_Daily_DHHS_"+str(calendar.month_name[today.month])+"_"+str(today.day)+"_"+str(today.year)+".pdf"
#print(input_pdf)
df = read_pdf(input_pdf, pages="1")

# read throgh the table, extract Washoe-only data, put in a dictionary
washoe_data = {'County':"Washoe"}
column_names = ['Population','Tests','People Tested','Cumulative Positivity Rate','Total Cases','Case Rate per 100,000','Deaths','Death Rate per 100,000']
for index, row in df[0].iterrows():
    if row[0].lower()=="washoe":
        i = 1
        while i < len(row):
            washoe_data.update({column_names[i-1] : str(row[i])})
            i+=1
    elif row[1].lower()=="washoe":
        i = 2
        while i < len(row):
            washoe_data.update({column_names[i-2] : str(row[i])})
            i+=1

print(washoe_data)
