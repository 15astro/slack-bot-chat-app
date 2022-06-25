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
    aggregate_function = "Maximum"
    resorce_identifier = "rds-test"
    slash_command_data=request.get_json()
    print(slash_command_data)
    if 'text' in slash_command_data:
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

       if 'minutes' in slash_command_data['text']:
           period = int(slash_command_data['text'].split()[-2])*60
       else:
           period = 300

       if 'max' in slash_command_data['text']:
           aggregate_function = 'Maximum'

       if 'min' in slash_command_data['text'].split():
           aggregate_function = 'Minimum'
         
       if 'avg' in slash_command_data['text']:
           aggregate_function = 'Average'

       if 'count' in slash_command_data['text']:
           aggregate_function = 'Count'

       if 'all' in slash_command_data['text']:
           all_responses = []
           all_metrics = ['CPUUtilization', 'FreeableMemory', 'DatabaseConnections', 'FreeStorageSpace', 'ReadLatency', 'WriteLatency', 'ReadIOPS', 'WriteIOPS', 'ReadThroughput', 'WriteThroughput', 'DiskQueueDepth']
           for metric in all_metrics:
             current_response = get_rd_stats(namespace, metric, period, aggregate_function)
             current_user_friendly_response = aggregate_function+" "+namespace+" "+metric+" for "+resorce_identifier+" is "+ str(round(current_response['MetricDataResults'][0]['Values'][0],2))
             requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": current_user_friendly_response})
           return str({ "text": None})
             #all_responses.append(current_user_friendly_response)


       rds_stats_response = get_rd_stats(namespace, metric_name, period, aggregate_function)
       print("Params passed to RDS:", namespace, metric_name, period, aggregate_function)
       print("Response returned by RDS:", rds_stats_response)
       print("Type of response by RDS:", type(rds_stats_response))
       cloudwatch_custom_response = {rds_stats_response['MetricDataResults'][0]['Label']: rds_stats_response['MetricDataResults'][0]['Values'][0]}
       cloudwatch_user_friendly_response = aggregate_function+" "+namespace+" "+metric_name+" for "+resorce_identifier+" is "+ str(round(rds_stats_response['MetricDataResults'][0]['Values'][0],2))

       requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": cloudwatch_user_friendly_response})
       return {"text":None}

    else:  
        empty_greeting_messsages = ["What's Up?, ", "Hello!, ", "Howdy?, ", "How are you doing today?, ", "How can I help?, ", "Never thought you'd come back so soon, " ]
        messsage_index=random.randint(0,len(empty_greeting_messsages)-1)
        empty_greetings = empty_greeting_messsages[messsage_index]+slash_command_data['userName'].split()[0]
        requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": empty_greetings})
        return { "text": None}


@app.route('/rds')
def fact_about_rds():
    client = boto3.client('iam')
    iam_response = client.list_users()
    print(type(iam_response))
    requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(iam_response)})
    return str(iam_response)


def get_rd_stats(namespace, metric_name, period, aggregate_function):
    print("This is what received in get_rd_stats function:", namespace, metric_name, period, aggregate_function)
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
            'Stat': aggregate_function,
            }
        }
    ],
    StartTime=(datetime.now() - timedelta(seconds=300 * 3)).timestamp(),
    EndTime=datetime.now().timestamp()
)
    #requests.post('https://api.flock.com/hooks/sendMessage/602bd051-e3cc-4fd4-8bd0-7e8a5fa9dd5d', json={ "text": str(response)})
    return response


