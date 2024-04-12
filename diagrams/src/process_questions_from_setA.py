import os
import json
from ....backend.src.main import get_answer_by_gpt_with_pc_qa_context


def process_questions_from_setA_and_save_results():
    # Define the directory containing the JSON files for setA
    setA_dir = "json_files/"

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
        print(file_path)
        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Iterate over each question in the JSON file
        for question_dict in data:
            # Call the get_answer_by_gpt_with_pc_qa_context function for each question
            req_data = {'question': question_dict, 'topic': topic_name}
            result = get_answer_by_gpt_with_pc_qa_context(req_data)
            # Compare the answer with the expected answer from the question dictionary
            expected_answer = question_dict['answer']
            is_correct = result == expected_answer

            # Append the result, question dictionary, and comparison to the results list
            results.append({
                'question': question_dict,
                'topic': topic_name,
                'result': result,
                'expected_answer': expected_answer,
                'is_correct': is_correct
            })
            break

    # Save the results to a JSON file
    output_file = 'results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_file}")


# Call the function to process questions from setA and save results
process_questions_from_setA_and_save_results()
