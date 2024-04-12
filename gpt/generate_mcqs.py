import csv
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_text_from_csv(file_path, title_column_name, column_name, title_value):
    texts = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row[title_column_name] == title_value:
                texts.append(row[column_name])
    return texts[0]

def get_learning_outcome_and_summary_text(title_value='Time-Series Analysis'):
    result = []
    try:
        file_path = 'refresher_readings.csv'  # Replace 'example.csv' with the path to your CSV file
        column_name = 'Learning Outcomes'  
        title_column_name = 'Title'
        lo_text = read_text_from_csv(file_path, title_column_name, column_name, title_value)
        column_name = 'Summary'  
        summary_text = read_text_from_csv(file_path, title_column_name, column_name, title_value)
        result = [lo_text, summary_text]
    except Exception as e:
        print(f"Error: {str(e)}")
    return result

def get_gpt_response(q_prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
             {"role": "system", "content": "You are a Question Answer generation Bot who generates questions and answers along with brief justifications"},
             {"role": "user", "content": q_prompt},
        ],
        max_tokens=10000,
    stream=True,
    )
    text = ""
    for chunk in response:
        # print(type(chunk.choices[0].delta))
        if chunk.choices[0].delta.content is not None:
            text = text + chunk.choices[0].delta.content
    return text


def parse_text_to_json(text):
    print("text", text)
    question_match = re.match(r'\s*(.*?)\s*(A\).*?D\).*?)\s*Answer: (Option [A-D])', text, re.DOTALL)
    if question_match:
        question, options, answer = question_match.groups()
        options = [opt.strip() for opt in options.split('\n')]
        answer = answer.strip()
    else:
        return None
    
    # Extract the justification if available
    justification_match = re.search(r'with justification - (.+)', text)
    justification = justification_match.group(1).strip() if justification_match else None
    
    # Format the options as a dictionary
    formatted_options = {opt[0]: opt[3:].strip() for opt in options}
    
    # Format the output
    output = {
        "question": question.strip(),
        "options": formatted_options,
        "answer": answer,
        "justification": justification
    }
    
    return output


def generate_mcq_json(mcqs):
    question_texts = re.split(r'\d+\.', mcqs)
    print(question_texts)
    json_data = []
    for mcq in question_texts:
        # input_string = "What is the difference between a linear trend model and a log-linear trend model?\n   A) The predicted trend value in a linear trend model is a constant amount, while in a log-linear trend model it grows at a constant rate.\n   B) The predicted trend value in a linear trend model is a constant rate, while in a log-linear trend model it grows by a constant amount.\n   C) The predicted trend value in a linear trend model is an exponential function, while in a log-linear trend model it is a linear function.\n   D) The predicted trend value in a linear trend model is a logarithmic function, while in a log-linear trend model it is a linear function.\n   Answer: Option A with justification - The summary states that a linear trend model predicts a constant amount of growth from period to period, while a log-linear trend model predicts a constant rate of growth.\n\n"
        
        parsed_mcq = parse_text_to_json(mcq)
        if parsed_mcq:
            json_data.append(parsed_mcq)
    return json.dumps(json_data, indent=4)


def generate_mcqs(lo_text, summary_text, num_questions=50):
    prompt = f"""Summary: {summary_text} and learning outcome: {lo_text}
    you are given a paragraph which has summary. \n
    You must create {num_questions} questions using it. you have to follow rules for generating question and those rules are -
        1. Each question should have only 4 options
        2. There should always be only one correct answer
        3. Do not create "All of the above", "All the above/None of the above" option
        4. Question and answer should be formatted as: 
            1. Question?
                A) Option 1
                B) Option 2
                C) Option 3
                D) Option 4
                Answer: Option x with justification
    """

    response = get_gpt_response(prompt)

    ex_res = generate_mcq_json(response)
    # print(ex_res)
    return ex_res



def formatText(text):
    data_single_line = " ".join(text.strip().splitlines())
    return ' '.join(data_single_line.split())

def get_mcqs(title_name=""):
    mcq_content = ""
    try:
        if len(title_name):
            result = get_learning_outcome_and_summary_text(title_name)
            lo_text, summary_text = result
            res = generate_mcqs(formatText(lo_text), formatText(summary_text), 10)
            # mcq_content = res.choices[0].text
            return res
    except Exception as e:
        print(f"Error: {str(e)}")
    return mcq_content

# def save_summary_to_md(mcq_content, file_path):
#     with open(file_path, "w") as md_file:
#         md_file.write(mcq_content)

def main():
    topics=['Time-Series Analysis','Machine Learning','Organizing, Visualizing, and Describing Data']
    for topic in topics:    
        mcq_content = get_mcqs(topic)
        # save_summary_to_md(mcq_content, f"md_files/{topic}_technical_summary.md")
        break
    print("Final", mcq_content)

if __name__ == "__main__":
    main()
