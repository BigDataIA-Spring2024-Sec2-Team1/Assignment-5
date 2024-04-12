from typing import List
import json
import streamlit as st
import requests
import warnings

warnings.filterwarnings("ignore")

# Function to fetch summary data for a given topic


def fetch_summary_data(topic):
    response = requests.get(f"http://backend:8000/get_summary_data/{topic}")
    print(response)
    return response.json().get("data", "")

# Function to fetch QA data for a given topic and set


def fetch_qa_data(topic, set_id):
    response = requests.get(
        f"http://backend:8000/get_qa_data/{topic}/{set_id}")
    return json.loads(response.json().get("data", "[]"))


def fetch_answer_by_gpt_with_pc_summary_context(jsondump):
    print(jsondump)
    data=json.loads(jsondump)
    url = f"http://backend:8000/get_answer_by_gpt_with_pc_summary_context"
    try:
        response = requests.post(url, json=data)
    #     if response.status_code == 200:
    #         st.success("Data sent successfully!")
    #     else:
    #         st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
    return response.json().get("markdown_text", {})


# Function to display markdown for a question
def display_question(question):
    markdown_text = f"### {question['question']}\n\n"
    markdown_text += "Options:\n\n"
    for i, option in enumerate(question['options'], start=1):
        markdown_text += f"{chr(64 + i)}) {option}\n"
    markdown_text += f"\n**Answer:** {question['answer']}\n\n"
    markdown_text += f"Justification: {question['justification']}"
    st.markdown(markdown_text)


# Define navigation pane
st.sidebar.title("Navigation")


def home_page():
    pages = {
        "Knowledge summary": knowledge_summary,
        "Knowledge base Q/A": Knowledge_base_QA,
        "Find answer by vector database": Answer_by_vector,
    }
    # "Find answer by knowledge summary": Answer_by_summary
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    if selected_page:
        pages[selected_page]()

# Page 1 definition


def knowledge_summary():
    st.title("Knowledge Summary")
    st.write("Select the topic")
    selected_topic = st.selectbox("Select topic", [
        "Time-Series Analysis",
        "Machine Learning",
        "Organizing, Visualizing, and Describing Data"
    ])
    summary = fetch_summary_data(selected_topic)
    st.write(f"{selected_topic} summary:")
    st.write(summary)

# Page 2 definition


def Knowledge_base_QA():
    st.title("Knowledge base Q/A")
    st.write("Select the topic")
    selected_topic = st.selectbox("Select topic", [
        "Time-Series Analysis",
        "Machine Learning",
        "Organizing, Visualizing, and Describing Data"
    ])
    selected_set = st.selectbox("Select Set", ["A", "B"])
    qa_data = fetch_qa_data(selected_topic, selected_set)
    questions = [entry["question"] for entry in qa_data]
    selected_question = st.selectbox("Select a question", questions)
    question = next(
        (entry for entry in qa_data if entry["question"] == selected_question), None)
    if question:
        display_question(question)


# Page 3 definition
def Answer_by_vector():
    st.title("Find answer by vector database")
    st.write("Select the topic")
    selected_topic = st.selectbox("Select topic", [
        "Time-Series Analysis",
        "Machine Learning",
        "Organizing, Visualizing, and Describing Data"
    ])
    selected_set = st.selectbox("Select Set", ["A", "B"])
    qa_data = fetch_qa_data(selected_topic, selected_set)
    questions = [entry["question"] for entry in qa_data]
    selected_question = st.selectbox("Select a question", questions)
    question = next(
        (entry for entry in qa_data if entry["question"] == selected_question), None)

    if question:
        display_question(question)

        # Add a button to get answer by RAG methodology
        if st.button("Get Answer by RAG methodology"):
            
            # Logic to get answer by RAG methodology
            st.write("Answer by RAG methodology:")
            # You can add the logic to get the answer by RAG methodology here

# Page 4 definition


def Answer_by_summary():
    st.title("Find answer by knowledge summary")
    st.write("Select the topic")
    selected_topic = st.selectbox("Select topic", [
        "Time-Series Analysis",
        "Machine Learning",
        "Organizing, Visualizing, and Describing Data"
    ])
    selected_set = st.selectbox("Select Set", ["A", "B"])
    qa_data = fetch_qa_data(selected_topic, selected_set)
    questions = [entry["question"] for entry in qa_data]
    selected_question = st.selectbox("Select a question", questions)
    question = next(
        (entry for entry in qa_data if entry["question"] == selected_question), None)

    if question:
        display_question(question)

    # Add a button to get answer by RAG methodology
    if st.button("Get Answer by RAG methodology"):
        question_entry=[entry for entry in qa_data if entry["question"] == selected_question][0]
        print(question_entry)
        # json_data = f"""{question_entry}""" 
        data_dict = json.dumps(question_entry)
        answer = fetch_answer_by_gpt_with_pc_summary_context(data_dict)
        st.write("Answer by RAG methodology:")
        st.write(answer)
        # display_question()
        # Logic to get answer by RAG methodology
        # You can add the logic to get the answer by RAG methodology here


home_page()
