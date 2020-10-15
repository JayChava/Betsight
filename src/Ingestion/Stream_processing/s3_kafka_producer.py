''' File to pull streaming data to kafka instance and starting producer for topic'''
import boto3
import pandas as pd
import json
from kafka import KafkaProducer
import sys
import time
import csv


# low-level functional API
client = boto3.client('s3') 
# high-level object-oriented API
resource = boto3.resource('s3') 

# reading in file from s3
my_bucket = resource.Bucket('betsight') 
obj = client.get_object(Bucket='betsight', Key='data/file.csv')
data = pd.read_csv(obj['Body'])

# storing data locally
data.to_csv('CD.csv')

# initializing producer
producer = KafkaProducer(bootstrap_servers = ['localhost:9092'])

# writing json data to topic
with open('CD.csv') as file:
        reader = csv.DictReader(file, delimiter=",")
        for row in reader:
               producer.send('gameweek', json.dumps(row).encode('utf-8'))
               producer.flush()