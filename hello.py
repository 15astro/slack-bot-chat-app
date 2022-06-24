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


