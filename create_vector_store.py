# create_vector_store.py
"""
Script to download a PDF paper from ArXiv, process it, and upsert metadata into Qdrant.

Usage:
    python create_vector_store.py --paper_number 1706.03762
"""

import argparse
import os
from uuid import uuid4

import requests
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.models import Distance, PointStruct, VectorParams

# Load environmental variables from a .env file
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
QDRANT_URL = os.getenv('QDRANT_URL')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def download_pdf_paper_from_arxiv(paper_number):
    """
    Download a PDF paper from ArXiv given its paper number.

    Args:
    ----
    paper_number (str): The ArXiv paper number.

    Returns:
    -------
    str: The paper number.

    """
    url = f"https://arxiv.org/pdf/{paper_number}.pdf"
    res = requests.get(url)
    pdf_path = f"{paper_number}.pdf"
    with open(pdf_path, 'wb') as f:
        f.write(res.content)
    return pdf_path

def create_collection_if_not_exists(client, collection_name):
    """
    Create a Qdrant collection if it does not already exist.

    Args:
    ----
    client (QdrantClient): The Qdrant client instance.
    collection_name (str): The name of the collection.

    """
    try:
        collections = client.get_collections()
        if collection_name not in [col.name for col in collections.collections]:
            client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    "content": VectorParams(size=1536, distance=Distance.COSINE)
                }
            )
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")
    except ResponseHandlingException as e:
        print(f"Error checking or creating collection: {e}")

def chunked_metadata(data, client, collection_name):
    """
    Process and upsert chunked metadata into Qdrant.

    Args:
    ----
    data (list): The list of document chunks.
    client (QdrantClient): The Qdrant client instance.
    collection_name (str): The name of the collection.

    """
    chunked_metadata = []

    for item in data:
        content = item.page_content

        id = str(uuid4())
        source = item.metadata["source"]
        page = item.metadata["page"]

        content_vector = embedding.embed_documents([content])[0]
        vector_dict = {"content": content_vector}

        payload = {
           "page_content": content,
           "metadata": {
                        "id": id,
                        "page_content": content,
                        "source": source,
                        "page": page,
                        }
            }

        metadata = PointStruct(id=id, vector=vector_dict, payload=payload)
        chunked_metadata.append(metadata)

    if chunked_metadata:
        client.upsert(
            collection_name=collection_name,
            wait=True,
            points=chunked_metadata
        )

    print(f"{len(chunked_metadata)} Chunked metadata upserted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an ArXiv paper and upsert metadata into Qdrant.")
    parser.add_argument("--paper_number", required=True, help="The ArXiv paper number (e.g., 1706.03762)")
    args = parser.parse_args()

    paper_number = args.paper_number

    # Download and process the paper
    pdf_path = download_pdf_paper_from_arxiv(paper_number)

    # Load documents
    loader = PyPDFLoader(pdf_path)

    # Embed and store documents in Qdrant
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Initialize Qdrant client
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # Create collection if it does not exist
    create_collection_if_not_exists(client, COLLECTION_NAME)

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    document = loader.load_and_split(text_splitter)

    # Upsert documents in vector store
    chunked_metadata(document[:40], client, COLLECTION_NAME)
