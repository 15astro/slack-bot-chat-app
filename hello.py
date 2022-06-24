from flask import Flask
import random
import requests
import json

from datetime import datetime, timedelta
import logging
from pprint import pprint
import random
import time
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/test')
def fact_about_space():

    ran=random.randint(1,70)
    requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={"text": ran})

    return str(ran)


@app.route('/rds')
def fact_about_rds():
    client = boto3.client('iam')
    iam_response = client.list_users()
    print(type(iam_response))
    requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(iam_response)})
    return str(iam_response)

@app.route('/cpu' ,methods=['POST'])
def get_cpu_stats():
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'cpu_usage',
            'MetricStat': {
            'Metric': {
                'Namespace': 'AWS/RDS',
                'MetricName': 'CPUUtilization',
                'Dimensions': [
                        {
                            "Name": "DBInstanceIdentifier",
                          "Value": "rds-test"  
                        }]
            },
            'Period': 1800,
            'Stat': 'Maximum',
            }
        }
    ],
    StartTime=(datetime.now() - timedelta(seconds=300 * 3)).timestamp(),
    EndTime=datetime.now().timestamp()
)
    requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(response)})
    return str(response)


@app.route('/connections')
def get_connection_stats():
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'max_connection_stats',
            'MetricStat': {
            'Metric': {
                'Namespace': 'AWS/RDS',
                'MetricName': 'DatabaseConnections',
                'Dimensions': [
                        {
                            "Name": "DBInstanceIdentifier",
                          "Value": "rds-test"
                        }]
            },
            'Period': 1800,
            'Stat': 'Maximum',
            }
        }
    ],
    StartTime=(datetime.now() - timedelta(seconds=300 * 3)).timestamp(),
    EndTime=datetime.now().timestamp()
)
    requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(response)})
    return str(response)
