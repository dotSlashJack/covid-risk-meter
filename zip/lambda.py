#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jack hester
"""
import boto3
import json
import pandas as pd
import io
from datetime import datetime
from pytz import timezone
import pytz

import calculate
import plot

def update_timestamp(s3_resource):
    timestamp = datetime.now(tz=pytz.utc)
    pacific_timestamp = timestamp.astimezone(timezone('US/Pacific'))
    minute = pacific_timestamp.strftime("%M")
    hour = pacific_timestamp.hour
    apm = "" # is it am or pm?
    if hour == 12:
        apm = ' PM'
    elif hour-12 > 0:
        hour = hour%12
        apm = ' PM'
    elif hour == 0:
        hour = 12
        apm = ' AM'
    update_time_friendly = "Last updated on "+pacific_timestamp.strftime("%m/%d/%Y")+" at "+str(hour)+":"+minute+apm
    
    filename = 'latest-timestamp.txt'
    bucket_name = "covid-alert-graphics"
    object = s3_resource.Object(bucket_name, filename)
    object.put(Body=update_time_friendly,ACL='public-read')
    
    print(update_time_friendly)
    return update_time_friendly


def update_metric(df):

    sum_list, threat_color, total_score = calculate.metric_calcs(df)

    print(sum_list)
    print(threat_color)
    print(total_score)
    # TODO: implement checking algorithm to see if there was a major drop/change in values
    # !!!!High priority!!!!

    s3_resource = boto3.resource("s3")
    metric_to_copy = "covid-alert-graphics/" + threat_color.lower() + "_metric.png"

    # remove the old metric
    s3_resource.Object("covid-alert-graphics", "current_code/current_metric.png").delete()
    # copy the correct image to s3 url that is fetched
    s3_resource.Object("covid-alert-graphics", "current_code/current_metric.png").copy_from(CopySource=metric_to_copy)
    s3_resource.ObjectAcl('covid-alert-graphics', 'current_code/current_metric.png').put(ACL='public-read')

    #plot.plot_test(df,s3_resource)

    timestamp = update_timestamp(s3_resource)

    return threat_color.lower(), timestamp


def lambda_handler(event, context):
    try:
        s3_client = boto3.client("s3")
        file_obj = event["Records"][0]
        file_name = str(file_obj["s3"]["object"]["key"])
        fileObj = s3_client.get_object(Bucket="covid-alert-table-upload", Key=file_name)
        file_content = fileObj["Body"].read()  # .decode("utf-8")
        b = io.BytesIO(file_content)  # read the excel file from aws format to python-friendly format
        df = pd.read_excel(b, sheet_name='data')

        color, timestamp = update_metric(df)
        #calculate.nv_state_calculator(df)
        #calculate.school_dist_calculator(df)

        return {
            'statusCode': 200,
            'body': file_name + " succesfully loaded and processed by AWS Lambda\n The color code was: " + color + "\n This calculation was completed at " + timestamp
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': "There was an internal error while attempting to update the code. Please check the log or contact colab[at]jackhester[dot]com."
        }
