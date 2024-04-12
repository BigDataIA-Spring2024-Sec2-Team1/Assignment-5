import os
import time
import json
from src.main import get_answer_by_gpt_with_pc_qa_context
from src.utility import Answer

output_file = os.path.join('results', 'results.json')


def process_questions_from_setA_and_save_results():
    # Define the directory containing the JSON files for setA
    setA_dir = "gpt/src/json_files/"

    # Get the list of JSON files in the setA directory
    json_files = [f for f in os.listdir(
        setA_dir) if f.endswith('.json') and 'setA' in f]

    # Create a list to store the results
    results = []

    # Iterate over each JSON file
    for json_file in json_files:
        # Extract topic name from the filename
        topic_name = json_file.split('_')[0]
        file_path = os.path.join(setA_dir, json_file)

        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        results_topic = []
        topic_dir = os.path.join('results', topic_name)
        os.makedirs('results', exist_ok=True)
        os.makedirs(topic_dir, exist_ok=True)

        # Iterate over each question in the JSON file
        for question_dict in data:
            # Call the get_answer_by_gpt_with_pc_qa_context function for each question
            req_data = {'question': question_dict, 'topic': topic_name}
            result = get_answer_by_gpt_with_pc_qa_context(
                req_data, answer_in_markdown_text=False)

            if result['answer']:
                answer_instance: Answer = result['answer']
                answer = answer_instance.Answer

                # Compare the answer with the expected answer from the question dictionary
                expected_answer = question_dict['answer'].replace(
                    'Option', '').strip()
                is_correct = answer == expected_answer

                # Append the result, question dictionary, and comparison to the results list
                results_topic.append({
                    'question': question_dict,
                    'topic': topic_name,
                    'result': answer_instance.dict(),
                    'expected_answer': expected_answer,
                    'generated_answer': answer,
                    'is_correct': is_correct
                })

                time.sleep(0.5)
                output_file = f'results_{topic_name}.json'
                save_results(results_topic, topic_dir, output_file)

        results.extend(results_topic)

    save_results(results, 'results', output_file)


def save_results(results, dir_name='results', output_file='results.json'):
    # Save the results to a JSON file
    output_file = os.path.join(dir_name, 'results.json')

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_file}")


def count_correct_answers(filename=output_file):
    # Read data from JSON file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Count the number of correct answers using list comprehension
    correct_answers = sum(question["is_correct"] for question in data)
    total_questions = len(data)
    wrong_answers = total_questions - correct_answers

    print("Total questions:", total_questions)
    print("Correct answers:", correct_answers)
    print("Wrong answers:", wrong_answers)


count_correct_answers(output_file)
# Call the function to process questions from setA and save results
# process_questions_from_setA_and_save_results()
