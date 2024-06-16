# lambda_function.py
"""
AWS Lambda handler module.

This module contains the lambda_handler function that processes incoming events
and generates responses using a retrieval and generation method.
"""

import json
import os

from dotenv import load_dotenv

from rag_app import rag_retrieve_and_generate

# Load environmental variables from a .env file
load_dotenv()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def lambda_handler(event, context):
    """
    AWS Lambda handler function to process incoming events and generate responses.

    Args:
    ----
    event (dict): The event payload from AWS Lambda, which includes the HTTP request details.
    context (LambdaContext): The runtime information provided by AWS Lambda, including function name, memory limit, and request ID.

    Returns:
    -------
    dict: The HTTP response containing the status code and response body.

    Raises:
    ------
    json.JSONDecodeError: If there is an error decoding the JSON payload.
    Exception: For any other exceptions that occur during processing.

    """
    # Log the incoming event for debugging
    print("Received event:", json.dumps(event))

    try:
        # Parse the body if it exists
        if 'body' in event:
            body = json.loads(event['body'])
            print(f"Parsed body: {body}")
            query = body.get('query', '')
            collection_name = body.get('collection_name', COLLECTION_NAME)
        else:
            # Handle direct invocation with query parameters
            query = event.get('query', '')
            collection_name = event.get('collection_name', COLLECTION_NAME)

        print(f"Query: {query}, Collection Name: {collection_name}")

        if not query:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Query parameter is missing'})
            }

        # Generate the response using the RAG (Retrieve and Generate) method
        response = rag_retrieve_and_generate(query, collection_name)
        print(f"Response: {response}")

        return {
            'statusCode': 200,
            'body': json.dumps({'response': response})
        }
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON format', 'details': str(e)})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)})
        }
