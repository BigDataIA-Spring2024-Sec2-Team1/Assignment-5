from typing import List
import re
import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

# Initialize OpenAI and Pinecone clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "text-embedding-3-small"
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


def get_summary_from_md(local_file_path):
    try:
        if os.path.exists(local_file_path):
            with open(local_file_path, "r") as md_file:
                summary_content = md_file.read()
            return summary_content
        else:
            return {"error": f"Summary data for topic '{topic_name}' not found."}
    except Exception as e:
        print(f"Error occurred while reading MD file: {e}")
        return None


def get_qa_from_json(topic_name, set='A'):
    try:
        qa_data = []
        file_name = generate_qa_filename(topic_name, "json", set)
        local_folder_path = f"/app/backend/json_files/"
        local_file_path = os.path.join(
            local_folder_path, os.path.basename(file_name))
        if os.path.exists(local_file_path):
            with open(local_file_path, "r") as file:
                qa_data = file.read()
            return qa_data
        else:
            return {"error": f"Summary data for topic '{topic_name}' not found."}
    except Exception as e:
        print(f"Error occurred while reading JSON file: {e}")
        return None


def get_gpt_response(q_prompt, max_tokens=500):
    try:
        response = client.completions.create(
            model="gpt-4-1106-preview",
            max_tokens=max_tokens,
            prompt=q_prompt
        )
        return response
    except Exception as e:
        print(f"Error occurred while getting GPT response: {e}")
        return None


def get_summary_from_gpt(query, topic_name='Time-Series-Analysis'):
    try:
        namespace_name = f'doc-summary-{topic_name.replace(" ", "-")}'
        q_prompt = retrieve(query, namespace_name, 'cfa-articles-summary')
        # print(q_prompt)
        summary_content = get_gpt_response(q_prompt)
        return summary_content
    except Exception as e:
        print(f"Error occurred while getting summary from GPT: {e}")
        return None


def generate_qa_filename(topic, filetype, set='A'):
    clean_topic = re.sub(r'[^a-zA-Z0-9\s]', '', topic)
    filename = clean_topic.replace(' ', '_').lower(
    ) + f"_technical_qa_set{set}.{filetype}"
    return filename


def retrieve(query, namespace_name='doc-summary-Time-Series-Analysis', index_name='cfa-articles-summary'):
    limit = 3750
    index = pinecone_client.Index(index_name)
    res = client.embeddings.create(input=query, model=MODEL)

    # retrieve from Pinecone
    xq = res.data[0].embedding

    # get relevant contexts
    match_res = index.query(
        vector=[xq], top_k=5, namespace=namespace_name, include_metadata=True)
    contexts = [
        x['metadata']['text'] for x in match_res['matches']
    ]

    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n" +
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )

    # Initialize prompt with prompt_start
    prompt = prompt_start

    # Append contexts until hitting limit
    for i, context in enumerate(contexts):
        if len(prompt) + len(context) + len(prompt_end) >= limit:
            # If adding the next context exceeds the limit, break the loop
            break
        else:
            prompt += "\n\n---\n\n" + context

    # Add prompt_end
    prompt += prompt_end

    return prompt
def convert_to_markdown(data):
    markdown_text = ""
    markdown_text += f"### {data['question']}\n\n"
    markdown_text += "Options:\n\n"
    for option in data['options']:
        markdown_text += f"- {option}\n"
    markdown_text += f"\n**Answer:** {data['answer']}\n\n"
    markdown_text += f"Justification: {data['justification']}\n\n"
    return markdown_text

def get_gpt_response(q_prompt, max_tokens=500):
  response = client.completions.create(
      model="gpt-4-1106-preview",
      max_tokens=max_tokens,
      prompt=q_prompt
    )
  return response