"""
    Lambda functions for automatically updating graphics on covid-alert.org
    Written by Jack Hester in conjunction with the City of Reno's Covid Response Committee
    Contact: colab@jackhester.com
"""

import json
import boto3
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import datetime as dt
import threatMeter
import io

# moves correct graphic to s3 bucket grabbed by the website

def thresholdRangerThreat(perc,rL):
    if perc <= rL[0]:
        score = "GREEN"
    elif perc > rL[0] and perc <= rL[1]:
        score = "YELLOW"
    elif perc > rL[1] and perc <= rL[2]:
        score = "ORANGE"
    elif perc > rL[2]:
        score = "RED"
    return score

"""
    Get correct color output to try against the 
    Param df, the dataframe of the excel file sheet
    Return threat, the threat color as a string
"""
def get_color(df):
    placeholderScore = threatMeter.ScoreCalculator(df,"dailyCases",7,[1,9,25],None,None,4.8) # PLACEHOLDER ONLY
    testPositivityScore = threatMeter.ScoreCalculator(df,"TestPositivity",7,[5,10,20])
    dailyNewCaseScore = threatMeter.ScoreCalculator(df,"dailyCases",7,[1,9,25],None,None,4.8)
    hospitalizationScore = threatMeter.ScoreCalculator(df,"Total_COVID",7,[-5,5,25],None,14,1)
    icuUsageScore = threatMeter.ScoreCalculator(df,"COVID_ICU",7,[-5,5,25],None,14,1)
    hosptitalCapacityScore = threatMeter.ScoreCalculator(df, "Staffed_Beds", 7, [70,80,85], "Inpatient",None,1)
    icuCapacityScore = threatMeter.ScoreCalculator(df,"ICU_Beds",7,[70,80,85],"ICU_Beds_Occ",None,1)

    indScoreList=[placeholderScore.getScore(),testPositivityScore.getScore(),dailyNewCaseScore.getScore(),hospitalizationScore.getScore(),icuUsageScore.getScore(),hosptitalCapacityScore.getScore(),icuCapacityScore.getScore()]

    grandScore = sum(indScoreList)
    rl = [0,3,8]
    threat = thresholdRangerThreat(grandScore,rl) # get the actual threat color
    print("The resulting threat level was: " + threat)

    return threat

"""
    Param colorStr the correct metric color, used to get 
"""
def update_graphic(colorStr):
    s3_resource = boto3.resource("s3")
    image_to_copy = "covid-alert-graphics/" + colorStr.lower() + ".png"
    #remove the old color image
    s3_resource.Object("covid-alert-graphics", "current_code/current.png").delete()
    #copy the correct image to s3 url that is fetched
    s3_resource.Object("covid-alert-graphics", "current_code/current.png").copy_from(CopySource=image_to_copy)
    s3_resource.ObjectAcl('covid-alert-graphics','current_code/current.png').put(ACL='public-read')


def lambda_handler(event, context):
    try:
        s3_client = boto3.client("s3")
        file_obj = event["Records"][0]
        file_name = str(file_obj["s3"]["object"]["key"])
        fileObj = s3_client.get_object(Bucket = "covid-alert-table-upload", Key=file_name)
        file_content = fileObj["Body"].read()#.decode("utf-8")
        b = io.BytesIO(file_content) # read the excel file from aws format to python-friendly format
        df = pd.read_excel(b, sheet_name='data')

        color = get_color(df)
        update_graphic(color)
        update_timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(update_timestamp)

        return {
            'statusCode': 200,
            'body': file_name + " succesfully loaded and processed by AWS Lambda\n The color code was: " + color + "\n This calculation was completed at " + update_timestamp
        }
    except Exception as e:
        print(str(e))
        return{
            'statusCode': 500,
            'body': "There was an internal error while attempting to update the code. Please check the log or contact colab[at]jackhester[dot]com."
        }