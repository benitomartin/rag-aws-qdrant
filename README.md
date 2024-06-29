# RAG AWS API QDRANT 🚀

<p align="center">
  <img width="976" alt="aws" src="https://github.com/benitomartin/mlops-aws-insurance/assets/116911431/4bfeb7ce-b151-4042-8cf6-c83299a2765a">
</p>

This repository contains a full Q&A pipeline using LangChain framework, Qdrant as vector database and AWS Lambda Function and API Gateway. The data used are research papers that can be loaded into the vector database, and the AWS Lambda Function processes the request using the retrieval and generation logic. Therefore it can use any other research paper from Arxiv.

This [Medium article](https://medium.com/@bmartinc80/building-a-serverless-application-with-aws-lambda-and-qdrant-for-semantic-search-ddb7646d4c2f) contains the complete instructions for the project set up.

The main steps taken to build the RAG pipeline can be summarize as follows:

* **Data Ingestion**: load data from https://arxiv.org

* **Indexing**: RecursiveCharacterTextSplitter for indexing in chunks

* **Vector Store**: Qdrant inserting metadata

* **QA Chain Retrieval**: RetrievalQA

* **AWS Lambda and API**: Process the request

* **Streamlit**: UI
  
Feel free to ⭐ and clone this repo 😉

## Tech Stack

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenAI](https://img.shields.io/badge/OpenAI-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![Anaconda](https://img.shields.io/badge/Anaconda-%2344A833.svg?style=for-the-badge&logo=anaconda&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Project Structure

The project has been structured with the following files:

- `Dockerfile:` Dockerfile
- `.env_sample`: sample environmental variables
- `.gitattributes`: gitattributes
- `Makefile`: install requirements, formating, linting, and clean up
- `pyproject.toml`: linting and formatting using ruff
- `requirements.txt:` project requirements
- `create_vector_store.py:` script to create the collection in Qdrant
- `rag_app.py:` RAG Logic
- `lambda_function.py:` lambda function
- `test_lambda.py:` script to test the lambda function
- `build_and_deploy.sh:` script to create and push the Docker image and deploy it as an AWS Lambda function


## Project Set Up

The Python version used for this project is Python 3.10. You can follow along the medium article.

1. Clone the repo (or download it as a zip file):

   ```bash
   git clone https://github.com/benitomartin/rag-aws-qdrant.git
   ```

2. Create the virtual environment named `main-env` using Conda with Python version 3.10:

   ```bash
   conda create -n main-env python=3.10
   conda activate main-env
   ```
   
3. Execute the `Makefile` script and install the project dependencies included in the requirements.txt:

    ```bash
    pip install -r requirements.txt

    or
 
    make install
    ```

4. Creat **AWS Account**, credentials, and proper policies with full access to ECR and Lambda for the project to function correctly. Make sure to configure the appropriate credentials to interact with AWS services.

5. Make sure the `.env` file is complete and run the `build_and_deploy.sh script`  

   ```bash
   chmod +x build_and_deploy.sh
   ./build_and_deploy.sh
   ```

6. If you get timeout and/or memory error you can increase them:
   ```bash
    aws lambda update-function-configuration \
    --function-name rag-llm-lambda \
    --timeout 300 \
    --memory-size 1024
   ```

7. Create an API Endpoint as per medium article description

8. Run the streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Streamlit UI

<p align="center">
    <img src="https://github.com/benitomartin/mlops-aws-insurance/assets/116911431/3bd3c707-4967-43d2-ba83-2a1a19196e47">
    </p>
