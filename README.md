# rag-aws-qdrant
python create_vector_store.py --paper_number 1706.03762

aws lambda update-function-configuration \
  --function-name rag-llm-lambda \
  --timeout 300 \
  --memory-size 1024


aws lambda get-function-configuration --function-name llm-lambda-raga


chmod +x build_and_deploy.sh

./build_and_deploy.sh



# Step 1: Create an API Gateway
Navigate to the API Gateway Console:

Go to the AWS Management Console.
Open the API Gateway service.
Create a New REST API:

Click on "Create API".
Select "REST API" and then click "Build".
Choose "New API".
Provide a name for your API (e.g., LLMAPI).
Click "Create API".
Create a Resource:

Click on "Actions" and select "Create Resource".
Provide a Resource Name (e.g., query) and Resource Path (e.g., /query).
Click "Create Resource".
Create a Method:

Select the newly created resource (/query).
Click on "Actions" and select "Create Method".
Choose "POST" from the dropdown and click the checkmark.
Set up Integration with Lambda:

In the "Setup" page, select "Lambda Function".
Check the box for "Use Lambda Proxy integration".
In the "Lambda Function" field, enter the name of your Lambda function (e.g., llm-lambda).
Click "Save".
You will be prompted to grant API Gateway permission to invoke your Lambda function. Click "OK".
Deploy the API:

Click on "Actions" and select "Deploy API".
Create a new deployment stage (e.g., dev).
Click "Deploy".
Get the Endpoint URL:

After deployment, you will be provided with an Invoke URL (e.g., https://<api-id>.execute-api.<region>.amazonaws.com/dev).


curl -X POST  https://0cmkbkknb6.execute-api.eu-central-1.amazonaws.com/dev/query   -H "Content-Type: application/json"   -d '{"query": "What is the capital of France?", "collection_name": "arxiv-collection"}'

curl -X POST  https://0cmkbkknb6.execute-api.eu-central-1.amazonaws.com/dev/query   -H "Content-Type: application/json"   -d '{"query": "positional encoder", "collection_name": "arxiv-collection"}'