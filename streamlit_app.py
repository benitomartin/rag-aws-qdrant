# streamlit_app.py
"""
Streamlit app to query an LLM via AWS Lambda.

This app allows users to enter a query and receive a response from an AWS Lambda
function that processes the query using a retrieval and generation method.
"""

import json
import os

import requests
import streamlit as st
from dotenv import load_dotenv

# Load environmental variables from a .env file
load_dotenv()

API_ENDPOINT = os.getenv('API_ENDPOINT')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')


# Set up the Streamlit app
st.title('Query LLM via AWS Lambda')
st.write("Enter your query below and get the response from the Lambda function.")

# Input for the query
query = st.text_input("Query:")

# Input for the collection name (optional)
collection_name = st.text_input("Qdrant Collection Name:", value=COLLECTION_NAME)

# Function to call the API Gateway
def call_lambda(query, collection_name):
    """
    Call the AWS Lambda function via the API Gateway endpoint.

    Args:
    ----
    query (str): The question to send to the Lambda function.
    collection_name (str): The name of the Qdrant collection to search in.

    Returns:
    -------
    dict: The JSON response from the Lambda function, or an error message.

    """
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "collection_name": collection_name
    }
    try:
        response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        print(f"Response status code: {response.status_code}")  # Debugging
        print(f"Response content: {response.content}")  # Debugging
        if response.content:
            return response.json()  # Attempt to parse JSON response
        else:
            return {"error": "Empty response"}
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
        st.error(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        st.error(f"JSON decode error: {json_err}")
        st.error(f"Response content: {response.content.decode()}")

# Button to submit the query
if st.button("Submit"):
    if query:
        with st.spinner('Calling Lambda function...'):
            response = call_lambda(query, collection_name)
            if response:
                st.write("Response:")
                # st.json(response)
                st.write(response['response'])
            else:
                st.error("No response received from the Lambda function.")
    else:
        st.error("Please enter a query.")
