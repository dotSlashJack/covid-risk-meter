"""
    Lambda functions for automatically updating graphics on covid-alert.org
    Written by Jack Hester and Jeremy Smith in conjungtion with the City of Reno's Covid Response Committee
    Contact: colab@jackhester.com or jsmith@tmrpa.org
"""
import json
import boto3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# moves correct graphic to s3 bucket grabbed by the website
# colorStr is the color to display
# TODO: update this to a better graphic, maybe add more than 3 codes
def update_graphic(colorStr):
    s3_resource = boto3.resource("s3")
    image_to_copy = colorStr+".png"
    #remove the old color image
    s3_resource.Object("current-color", "current_code/current.png").delete()
    #copy the correct image to s3 url that is fetched
    s3_resource.Object("current-color", "current_code/current.png").copy_from(CopySource="current-color/yellow.png")
    s3_resource.ObjectAcl('current-color','current_code/current.png').put(ACL='public-read')
    return "color: "+image_to_copy


def lambda_handler(event, context):
    s3_client = boto3.client("s3")
    file_obj = event["Records"][0]
    file_name = str(file_obj["s3"]["object"]["key"])
    fileObj = s3_client.get_object(Bucket = "warning-code-graphic", Key=file_name)
    file_content = fileObj["Body"].read().decode("utf-8")
    update_graphic("yellow")

    return {
        'statusCode': 200,
        'body': file_name+" succesfully loaded and processed by AWS Lambda"
    }