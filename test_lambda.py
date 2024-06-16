# # test_lambda.py
"""
Test script to invoke the AWS Lambda function.

This script sends a test payload to the AWS Lambda function and prints the response.
"""
import json
import os

import boto3
from dotenv import load_dotenv

# Load environmental variables from a .env file
load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')
LAMBDA_FUNCTION_NAME = os.getenv('LAMBDA_FUNCTION_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Initialize a session using Amazon Lambda
client = boto3.client('lambda', region_name=AWS_REGION)

# Create a payload
payload = {
    "query": "Positional Encoding",
    "collection_name": COLLECTION_NAME
}

# Log the payload for debugging
print("Payload:", json.dumps(payload, indent=4))

# Invoke the Lambda function
response = client.invoke(
    FunctionName=LAMBDA_FUNCTION_NAME,
    InvocationType='RequestResponse',
    Payload=json.dumps(payload)
)

# Print the response
response_payload = json.loads(response['Payload'].read())
print(json.dumps(response_payload, indent=4))
