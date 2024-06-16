#!/bin/bash

# Exit immediately if a command exits with a non-zero status
# set -e

# Load environment variables from .env file
set -o allexport
source .env
set -o allexport

# Check if the ECR repository exists, create it if it does not
REPO_EXISTS=$(aws ecr describe-repositories --repository-names ${REPOSITORY_NAME} --region ${AWS_REGION} 2>&1)

if [[ $REPO_EXISTS == *"RepositoryNotFoundException"* ]]; then
    echo "Repository ${REPOSITORY_NAME} does not exist. Creating..."
    aws ecr create-repository --repository-name ${REPOSITORY_NAME} --region ${AWS_REGION}
else
    echo "Repository ${REPOSITORY_NAME} already exists."
fi

# Build Docker image
echo "Building Docker image ${IMAGE_NAME}..."
docker build -t ${IMAGE_NAME} .

# Authenticate Docker to your Amazon ECR registry
echo "Authenticating Docker to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Tag the Docker image
echo "Tagging Docker image..."
docker tag ${IMAGE_NAME}:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest

# Push the Docker image to Amazon ECR
echo "Pushing Docker image to ECR..."
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest

# Check if the Lambda function exists, create it if it does not
FUNCTION_EXISTS=$(aws lambda get-function --function-name ${LAMBDA_FUNCTION_NAME} --region ${AWS_REGION} 2>&1)

if [[ $FUNCTION_EXISTS == *"ResourceNotFoundException"* ]]; then
    echo "Lambda function ${LAMBDA_FUNCTION_NAME} does not exist. Creating..."
    aws lambda create-function \
        --function-name ${LAMBDA_FUNCTION_NAME} \
        --package-type Image \
        --code ImageUri=${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest \
        --role ${LAMBDA_ROLE_ARN} \
        --region ${AWS_REGION}
else
    echo "Lambda function ${LAMBDA_FUNCTION_NAME} already exists. Updating..."
    aws lambda update-function-code --function-name ${LAMBDA_FUNCTION_NAME} --image-uri ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}:latest
fi

echo "Deployment complete."
