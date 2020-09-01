#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 23:37:46 2020

@author: jack hester and jeremy smith
"""
import boto3
import json
import pandas as pd
import io
import datetime as dt

import calculate
import plot

def update_timestamp():
    update_timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print(update_timestamp)
    # TODO: finish implementation by putting text file in current_code dir

def update_metric(df):
    threat_color, total_score = calculate.metric_calcs(df)
    # TODO: implement checking algorithm to see if there was a major drop/change in values
    # !!!!High priority!!!!
    
    s3_resource = boto3.resource("s3")
    metric_to_copy = "covid-alert-graphics/" + threat_color.lower() + "_metric.png"
    
    # remove the old metric
    s3_resource.Object("covid-alert-graphics", "current_code/current_metric.png").delete()
    # copy the correct image to s3 url that is fetched
    s3_resource.Object("covid-alert-graphics", "current_code/current_metric.png").copy_from(CopySource=metric_to_copy)
    s3_resource.ObjectAcl('covid-alert-graphics', 'current_code/current_metric.png').put(ACL='public-read')
    
    plot.plot_test(df,s3_resource)

    return threat_color.lower()


def lambda_handler(event, context):
    try:
        s3_client = boto3.client("s3")
        file_obj = event["Records"][0]
        file_name = str(file_obj["s3"]["object"]["key"])
        fileObj = s3_client.get_object(Bucket="covid-alert-table-upload", Key=file_name)
        file_content = fileObj["Body"].read()  # .decode("utf-8")
        b = io.BytesIO(file_content)  # read the excel file from aws format to python-friendly format
        df = pd.read_excel(b, sheet_name='data')

        color = update_metric(df)
        #update_timestamp()
        #calculate.nv_state_calculator(df)
        #calculate.school_dist_calculator(df)

        return {
            'statusCode': 200,
            'body': file_name + " succesfully loaded and processed by AWS Lambda\n The color code was: " + color + "\n This calculation was completed at "# + update_timestamp
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': "There was an internal error while attempting to update the code. Please check the log or contact colab[at]jackhester[dot]com."
        }  

