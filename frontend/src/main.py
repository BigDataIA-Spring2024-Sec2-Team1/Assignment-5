import json
import streamlit as st
import warnings
from utility import *
from os import path
from streamlit.logger import get_logger

warnings.filterwarnings("ignore")

logger = get_logger(__name__)


# Define navigation pane
st.sidebar.title("Navigation")


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
    if summary:
        st.write(f"{selected_topic} summary:")
        st.write(summary)
    else:
        st.write("Error fetching summary data.")


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
        markdown_text = display_question(question)
        st.markdown(markdown_text)


# Page 3 definition
def Answer_by_qa_vector():
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
        markdown_text = display_question(question)
        st.markdown(markdown_text)

        # Add a button to get answer by RAG methodology
        if st.button("Get Answer by RAG methodology"):
            try:
                question_entry = [
                    entry for entry in qa_data if entry["question"] == selected_question][0]
                data_dict = json.dumps(question_entry)
                answer = fetch_answer_by_gpt_with_pc_qa_context(
                    data_dict, selected_topic)
                st.write("Answer by RAG methodology:")
                if answer:
                    st.markdown(answer)
                else:
                    st.write("Error")
            except Exception as e:
                logger.error(
                    f"Error getting answer by RAG methodology: {str(e)}")


# Page 4 definition
def Answer_by_summary_vectors():
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
        markdown_text = display_question(question)
        st.markdown(markdown_text)

    # Add a button to get answer by RAG methodology
    if st.button("Get Answer by RAG methodology"):
        try:
            question_entry = [
                entry for entry in qa_data if entry["question"] == selected_question][0]
            data_dict = json.dumps(question_entry)
            answer = fetch_answer_by_gpt_with_pc_summary_context(
                data_dict, selected_topic)
            st.write("Answer by RAG methodology:")
            if answer:
                st.markdown(answer)
            else:
                st.write("Error")
        except Exception as e:
            logger.error(f"Error getting answer by RAG methodology: {str(e)}")


def home_page():
    pages = {
        "Knowledge summary": knowledge_summary,
        "Knowledge base Q/A": Knowledge_base_QA,
        "Find answer by vector database": Answer_by_qa_vector,
        "Find answer by knowledge summary": Answer_by_summary_vectors
    }
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    if selected_page:
        pages[selected_page]()


if __name__ == "__main__":
    home_page()
