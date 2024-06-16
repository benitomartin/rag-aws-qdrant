# rag_app.py
"""
Module for retrieval and generation of responses using Qdrant and GPT-3.5-turbo.

This module provides the function to retrieve context from Qdrant and generate
an answer using GPT-3.5-turbo based on the retrieved context.
"""
import os

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

# Load environmental variables from a .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

# Initialize Qdrant client
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# Embed and store documents in Qdrant
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

def rag_retrieve_and_generate(query, collection_name):
    """
    Retrieve context from Qdrant and generate an answer using GPT-3.5-turbo.

    Args:
    ----
    query (str): The question to retrieve context for.
    collection_name (str): The name of the Qdrant collection to search in.

    Returns:
    -------
    str: The generated answer based on retrieved context.

    """
    # Initialize vector store
    vectorstore = Qdrant(client=client,
                        collection_name=collection_name,
                        embeddings=embedding,
                        vector_name="content")

    # Define the prompt template
    template = """

    You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \


    Question: {question}
    Context: {context}

    Answer:

    """

    # Initialize retriever
    retriever = vectorstore.as_retriever()

    # Create prompt using the template
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize the LLM (GPT-3.5-turbo)
    llm35 = ChatOpenAI(temperature=0.0,
                    model="gpt-3.5-turbo",
                    max_tokens=512)


    # Create a retrieval QA chain
    qa_d35 = RetrievalQA.from_chain_type(
                                        llm=llm35,
                                        chain_type="stuff",
                                        chain_type_kwargs = {"prompt": prompt},
                                        retriever=retriever)

    # Invoke the chain with the query to get the result
    result = qa_d35.invoke({"query": query})["result"]
    return result

if __name__ == "__main__":
    # Example usage
    collection_name = COLLECTION_NAME
    query = "What is the attention mechanism?"
    print(f"Response: {rag_retrieve_and_generate(query, collection_name)}")
