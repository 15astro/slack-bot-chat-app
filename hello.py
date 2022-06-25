from flask import Flask
import random
import requests
import json
from flask import request

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

@app.route("/entrypoint" ,methods=['POST'])
def slash_entrypoint():
    namespace = 'AWS/RDS'
    metric_name = 'DatabaseConnections'
    slash_command_data=request.get_json()
    print(slash_command_data)
    if 'text' in slash_command_data:
       # text_command = slash_command_data['text']
       # text_splits = text_command.split()
       # for split in text_splits:
       #   print(split)
       if 'rds' in slash_command_data['text']:
           namespace = 'AWS/RDS'

       if 'cpu' in slash_command_data['text']:
           metric_name = 'CPUUtilization'

       if 'memory' in slash_command_data['text']:
           metric_name = 'FreeableMemory'

       if 'connections' in slash_command_data['text']:
           metric_name = 'DatabaseConnections'

       if 'space' in slash_command_data['text']:
           metric_name = 'FreeStorageSpace'

       if 'read latency' in slash_command_data['text']:
           metric_name = 'ReadLatency'

       if 'write latency' in slash_command_data['text']:
           metric_name = 'WriteLatency'
        
       if 'read iops' in slash_command_data['text']:
           metric_name = 'ReadIOPS'

       if 'write iops' in slash_command_data['text']:
           metric_name = 'WriteIOPS'

       if 'read throughput' in slash_command_data['text']:
           metric_name = 'ReadThroughput'

       if 'write throughput' in slash_command_data['text']:
           metric_name = 'WriteThroughput'    

       if 'disk queue' in slash_command_data['text']:
           metric_name = 'DiskQueueDepth'  

       if 'mins' in slash_command_data['text'] or 'minutes' in slash_command_data['text']:
           period = int(slash_command_data['text'].split()[-2])*60
       else:
           period = 300

       rds_stats_response = get_rd_stats(namespace, metric_name, period)
       requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(rds_stats_response)})
       return {"text":rds_stats_response}

    else:   
        empty_greetings = "What's Up, "+slash_command_data['userName'].split()[0]
        return str({ "text": empty_greetings})


@app.route('/rds')
def fact_about_rds():
    client = boto3.client('iam')
    iam_response = client.list_users()
    print(type(iam_response))
    requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(iam_response)})
    return str(iam_response)


def get_rd_stats(namespace, metric_name, period):
    cloudwatch = boto3.client('cloudwatch')
    response = cloudwatch.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'cloudwatch_metrics',
            'MetricStat': {
            'Metric': {
                'Namespace': namespace,
                'MetricName': metric_name,
                'Dimensions': [
                        {
                            "Name": "DBInstanceIdentifier",
                          "Value": "rds-test"
                        }]
            },
            'Period': period,
            'Stat': 'Maximum',
            }
        }
    ],
    StartTime=(datetime.now() - timedelta(seconds=300 * 3)).timestamp(),
    EndTime=datetime.now().timestamp()
)
    #requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(response)})
    return str(response)


