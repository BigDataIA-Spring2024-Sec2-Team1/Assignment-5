import json
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

from pinecone import Pinecone, ServerlessSpec

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


def create_index(index_name='cfa-articles-qa'):

    # # Check whether the index with the same name already exists - if so, delete it
    # if index_name in pinecone_client.list_indexes():
    #     pinecone_client.delete_index(index_name)

    # Now do stuff
    print(pinecone_client.list_indexes().names())
    if index_name not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=index_name,
            dimension=1536,
            metric='dotproduct',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-2'
            )
        )
# Function to upsert data into Pinecone


def upsert_into_pinecone(index_name, namespace_name, data_chunks, embeddings):
    embedding_to_upsert = []
    for i, chunk in enumerate(data_chunks):
        rand_chunk_code = ''.join(random.choices(
            string.ascii_letters + string.digits, k=3))
        embedding_to_upsert.append({'id': f'doc-summ-{rand_chunk_code}',
                                   'values': embeddings.data[i].embedding, 'metadata': {'text': chunk}})
    try:
        index = pinecone_client.Index('cfa-articles-qa')
        index.upsert(vectors=list(embedding_to_upsert), namespace=namespace_name)
        # pinecone_client.index.upsert(
            # index_name=index_name, vectors=embedding_to_upsert, namespace=namespace_name)
    except Exception as e:
        print(f"Error occurred while upserting into Pinecone: {e}")


def generate_filename(topic, filetype, separator='_'):
    # Remove special characters and replace spaces with underscores
    clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
    filename = clean_topic.replace(' ', separator).lower() + f"_technical_qa.{filetype}"
    return filename


def get_qa_from_file(file_path):
    try:
        print(file_path)
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
        return json_data
    except Exception as e:
        print(f"Error occurred while reading MD file: {e}")
        return None


def generate_markdown_from_json(data):
    markdown_text = ""
    markdown_text += f"### {data['question']}\n\n"
    for option in data['options']:
        markdown_text += f"{option}\n"
    markdown_text += f"\nAnswer: {data['answer']} with justification - {data['justification']}\n\n"
    return markdown_text


# Function to generate GPT qa and upsert into Pinecone
def get_question_and_upsert(topic, set='A'):
    try:
        # Get GPT qa
        filename = generate_filename(topic, 'json', '_')
        file_path = f"json_files/{filename}"
        print(file_path)
        if os.path.exists(file_path):
            json_data = get_qa_from_file(file_path)
            # print(json_data)
            if len(json_data):
                create_index('cfa-articles-qa')
                for qa_data in json_data:
                    try:
                        markdown_text = generate_markdown_from_json(qa_data)
                        # print(markdown_text)
                        # Chunk and embed GPT qa
                        qa_chunks, embeddings = chunk_and_embed(markdown_text)
                        filename = filename.split(".")[0]
                        # Upsert embeddings into Pinecone
                       
                        upsert_into_pinecone('cfa-articles-qa',
                                             f'{filename}-set{set}', qa_chunks, embeddings)
                    except Exception as e:
                        print(f"Error processing QA data: {str(e)}")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    topics = ['Time-Series Analysis', 'Machine Learning',
              'Organizing, Visualizing, and Describing Data']
    for topic in topics:
        get_question_and_upsert(topic,'B')
        # break


if __name__ == "__main__":
    main()
