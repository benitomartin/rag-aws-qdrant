# Dockerfile
FROM public.ecr.aws/lambda/python:3.10

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY rag_app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY .env ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Command to run the Lambda function
CMD ["lambda_function.lambda_handler"]