import os
from openai import OpenAI
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
import string
import random
from dotenv import load_dotenv

load_dotenv()

pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to chunk and embed data
def chunk_and_embed(data):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_text(data)
    embeddings = openai_client.embeddings.create(
        input=chunks,
        model="text-embedding-3-small"
    )
    return chunks, embeddings


# Function to upsert data into Pinecone
def upsert_into_pinecone(namespace, data_chunks, embeddings):
    embedding_to_upsert = []
    for i, chunk in enumerate(data_chunks):
        rand_chunk_code = ''.join(random.choices(
            string.ascii_letters + string.digits, k=3))
        embedding_to_upsert.append({'id': f'doc-summ-{rand_chunk_code}',
                                   'values': embeddings.data[i].embedding, 'metadata': {'text': chunk}})
    try:
        pinecone_client.create_index(
            namespace,
            dimension=1536,
            metric='dotproduct',
            replicas=1
        )
        pinecone_client.index.upsert(
            index_name=namespace, vectors=embedding_to_upsert)
    except Exception as e:
        print(f"Error occurred while upserting into Pinecone: {e}")


def get_summary_from_md(file_path):
    try:
        with open(file_path, "r") as md_file:
            summary_content = md_file.read()
        return summary_content
    except Exception as e:
        print(f"Error occurred while reading MD file: {e}")
        return None


# Function to generate GPT summary and upsert into Pinecone
def get_summary_and_upsert(topic):
    # Get GPT summary
    file_path = f"mdfiles/{topic}_technical_summary.md"
    if os.path.exists(file_path):
        summary_content = get_summary_from_md(file_path)

        # Chunk and embed GPT summary
        summary_chunks, embeddings = chunk_and_embed(summary_content)

        # Upsert embeddings into Pinecone
        upsert_into_pinecone(
            f'doc-summary-{topic.replace(" ", "-")}', summary_chunks, embeddings)
    else:
        print(f"File '{file_path}' does not exist.")


# def main():
#     topics = ['Time-Series Analysis', 'Machine Learning',
#               'Organizing, Visualizing, and Describing Data']
#     for topic in topics:
#         get_summary_and_upsert(topic)


# if __name__ == "__main__":
#     main()
