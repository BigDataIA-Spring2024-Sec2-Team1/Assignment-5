import streamlit as st
import requests
import warnings

warnings.filterwarnings("ignore")

st.sidebar.title("Navigation")
# Define navigation pane


def home_page():
    if st.sidebar.button("Knowledge summary"):
        st.session_state.page = "Knowledge_summary"
    if st.sidebar.button("Knowledge base Q/A"):
        st.session_state.page = "Knowledge_base_QA"
    if st.sidebar.button("Find answer by vector database"):
        st.session_state.page = "Answer_by_vector"
    if st.sidebar.button("Find answer by knowledge summary"):
        st.session_state.page = "Answer_by_summary"

    if "page" in st.session_state:
        if st.session_state.page == "Knowledge_summary":
            knowledge_summary()
        elif st.session_state.page == "Knowledge_base_QA":
            Knowledge_base_QA()
        elif st.session_state.page == "Answer_by_vector":
            Answer_by_vector()  # Corrected function name
        elif st.session_state.page == "Answer_by_summary":
            Answer_by_summary()  # Corrected function name

# Page 1 definition --------------------------------------------


def knowledge_summary():
    st.title("Knowledge Summary")
    st.write("Select the topic")

    selected_topic = st.selectbox("Select topic", [
                                  "Time-Series Analysis", "Machine Learning", "Organizing, Visualizing, and Describing Data"])
    if selected_topic == "Time-Series Analysis":
        st.write("Time-Series Analysis summary will be displayed here")
    elif selected_topic == "Machine Learning":
        st.write("Machine Learning summary will be displayed here")
    elif selected_topic == "Organizing, Visualizing, and Describing Data":
        st.write(
            "Organizing, Visualizing, and Describing Data summary will be displayed here")

# Page 2 definition --------------------------------------------


def Knowledge_base_QA():
    st.title("Knowledge base Q/A")
    st.write("Select the topic")
    knowledge_QA_topic = st.selectbox("Select topic", [
                                      "Time-Series Analysis", "Machine Learning", "Organizing, Visualizing, and Describing Data"])
    if knowledge_QA_topic == "Time-Series Analysis":
        time_series_topic()
    elif knowledge_QA_topic == "Machine Learning":
        machine_learning_topic()
    elif knowledge_QA_topic == "Organizing, Visualizing, and Describing Data":
        organizing_data_topic()

# All topics


def time_series_topic():
    st.title("Time-Series Analysis")
    st.write("Select a set you would like to explore")

    selected_set = st.selectbox("Select Set", ["Set A", "Set B"])
    if selected_set == "Set A":
        time_series_set_a()
    elif selected_set == "Set B":
        time_series_set_b()


def machine_learning_topic():
    st.title("Machine Learning")
    st.write("Select a set you would like to explore")

    selected_set = st.selectbox("Select Set", ["Set A", "Set B"])
    if selected_set == "Set A":
        machine_learning_set_a()
    elif selected_set == "Set B":
        machine_learning_set_b()


def organizing_data_topic():
    st.title("Organizing, Visualizing, and Describing Data")
    st.write("Select a set you would like to explore")

    selected_set = st.selectbox("Select Set", ["Set A", "Set B"])
    if selected_set == "Set A":
        organizing_data_set_a()
    elif selected_set == "Set B":
        organizing_data_set_b()

# Sets for all topics


def time_series_set_a():
    st.title("Time-Series Analysis - Set A")
    st.write("Questions of set A")
    # Make a GET request to your FastAPI endpoint
    response = requests.get("http://localhost:8000/data")
    # Extract the JSON data from the response
    data = response.json()
    # Extract the list of data from the JSON response
    data_list = data.get("data_list", [])
    # Create a dropdown list in Streamlit
    selected_option = st.selectbox("Select an option", data_list)
    # Display the selected option
    st.write("Answer of:", selected_option)


def time_series_set_b():
    st.title("Time-Series Analysis - Set B")
    st.write("Questions of set B")
    questions_set_b = ["Question 4", "Question 5", "Question 6"]
    selected_question_b = st.selectbox(
        "Select Question from Set B", questions_set_b)
    st.session_state.selected_question = selected_question_b
    display_answer(selected_question_b)


def machine_learning_set_a():
    st.title("Machine Learning - Set A")
    st.write("Questions of set A")
    questions_set_a = ["Question 1", "Question 2", "Question 3"]
    selected_question_a = st.selectbox(
        "Select Question from Set A", questions_set_a)
    st.session_state.selected_question = selected_question_a
    display_answer(selected_question_a)


def machine_learning_set_b():
    st.title("Machine Learning - Set B")
    st.write("Questions of set B")
    questions_set_b = ["Question 4", "Question 5", "Question 6"]
    selected_question_b = st.selectbox(
        "Select Question from Set B", questions_set_b)
    st.session_state.selected_question = selected_question_b
    display_answer(selected_question_b)


def organizing_data_set_a():
    st.title("Organizing, Visualizing, and Describing Data - Set A")
    st.write("Questions of set A")
    questions_set_a = ["Question 1", "Question 2", "Question 3"]
    selected_question_a = st.selectbox(
        "Select Question from Set A", questions_set_a)
    st.session_state.selected_question = selected_question_a
    display_answer(selected_question_a)


def organizing_data_set_b():
    st.title("Organizing, Visualizing, and Describing Data - Set B")
    st.write("Questions of set B")
    questions_set_b = ["Question 4", "Question 5", "Question 6"]
    selected_question_b = st.selectbox(
        "Select Question from Set B", questions_set_b)
    st.session_state.selected_question = selected_question_b
    display_answer(selected_question_b)


def display_answer(selected_question):
    # Here you can add logic to fetch and display the answer related to the selected question
    if selected_question == "Question 4":
        st.write("Answer to Question 4")
    elif selected_question == "Question 5":
        st.write("Answer to Question 5")
    elif selected_question == "Question 6":
        st.write("Answer to Question 6")
    else:
        st.write("No answer found for the selected question")

# Page 3 definition --------------------------------------------


def Answer_by_vector():
    st.title("Find answer by vector database")
    st.write("Select the topic")
    knowledge_QA_topic = st.selectbox("Select topic", [
                                      "Time-Series Analysis", "Machine Learning", "Organizing, Visualizing, and Describing Data"])
    if knowledge_QA_topic == "Time-Series Analysis":
        time_series_topic()
    elif knowledge_QA_topic == "Machine Learning":
        machine_learning_topic()
    elif knowledge_QA_topic == "Organizing, Visualizing, and Describing Data":
        organizing_data_topic()

# Page 4 definition --------------------------------------------


def Answer_by_summary():
    st.title("Find answer by knowledge summary")
    st.write("Select the topic")
    knowledge_QA_topic = st.selectbox("Select topic", [
                                      "Time-Series Analysis", "Machine Learning", "Organizing, Visualizing, and Describing Data"])
    if knowledge_QA_topic == "Time-Series Analysis":
        time_series_topic()
    elif knowledge_QA_topic == "Machine Learning":
        machine_learning_topic()
    elif knowledge_QA_topic == "Organizing, Visualizing, and Describing Data":
        organizing_data_topic()


home_page()
