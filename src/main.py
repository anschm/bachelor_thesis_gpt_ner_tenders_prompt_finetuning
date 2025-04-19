import argparse
import os
from datetime import datetime

import pandas

from environment_varialbes import get_openai_api_key, get_openai_model, get_openai_role, get_results_dir, \
    get_test_data_dir
from open_ai_client import OpenAiClient
from src.prompt_builder import PromptBuilder
from src.prompt_strategy import PromptStrategy


def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Sets up the argument parser for parsing command-line arguments.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(prog='Tender Prompt Evaluation', description='This program evaluates the different prompts to detect entities within public tenders')
    parser.add_argument('-ps', '--prompt-strategy', type=PromptStrategy, choices=list(PromptStrategy), help='Prompt strategy to use', required=True)
    parser.add_argument('-i', '--index', type=int, help='Define a specific index of the test data to prompt')
    return parser


def get_args():
    """
    Retrieves the parsed command-line arguments.

    Returns:
        Namespace: The namespace with parsed arguments.
    """
    return setup_arg_parser().parse_args()


def get_examples(prompt_strategy: PromptStrategy):
    """
    Retrieves examples based on the provided prompt strategy.

    Args:
        prompt_strategy (PromptStrategy): The strategy to use for fetching examples.

    Returns:
        list: A list of examples corresponding to the specified strategy.
    """
    examples = []

    examples_dir = os.path.join(test_data_dir, 'tender-examples', str(prompt_strategy))
    if not os.path.exists(examples_dir):
        return examples

    examples_files = os.listdir(examples_dir)
    for example_file in examples_files:
        example = open(os.path.join(examples_dir, str(example_file)), 'r').read()
        examples.append(example)
    return examples


def save_results_into_excel(result_dir: str, tender_test_results: list):
    """
    Saves the test results into an Excel file.

    Args:
        result_dir (str): The directory where the Excel file should be saved.
        tender_test_results (list): The list of test results to be saved.
    """
    columns = ['Index', 'Title', 'Needed Time', 'Total Tokens', 'Completion Tokens', 'Prompt Tokens', 'Length of HTML', 'Result']
    dataframe = pandas.DataFrame(tender_test_results, columns=columns)
    dataframe.to_excel(os.path.join(result_dir, 'tender-test-results.xlsx'), index=False)


def save_prompt(result_dir: str, index: str, prompt: str):
    """
    Saves the generated prompt to a text file.

    Args:
        result_dir (str): The directory where the prompt should be saved.
        index (str): The index of the test data for which the prompt was generated.
        prompt (str): The prompt text to be saved.
    """
    with open(os.path.join(result_dir, index + '.txt'), 'w') as prompt_file:
        prompt_file.write(prompt)


def save_html_result(result_dir: str, index: str, html_result: str):
    """
    Saves the HTML result to a file.

    Args:
        result_dir (str): The directory where the HTML result should be saved.
        index (str): The index of the test data for which the result was generated.
        html_result (str): The HTML content of the result to be saved.
    """
    with open(os.path.join(result_dir, str(index) + ".html"), 'w') as result_tender_html:
        result_tender_html.write(html_result)


if __name__ == '__main__':
    """
    Main entry point for the script. Parses command-line arguments, sets up 
    directories, initializes the OpenAI client, and processes the test data 
    using the specified prompt strategy.
    """

    # Get the current timestamp for unique identification of the run
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # Parse command-line arguments
    args = get_args()
    prompt_strategy = args.prompt_strategy
    test_data_index = args.index

    # Set up directories for results
    results_dir = get_results_dir()
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Retrieve necessary environment variables
    test_data_dir = get_test_data_dir()
    openai_api_key = get_openai_api_key()
    openai_model = get_openai_model()
    openai_role = get_openai_role()

    # Create a unique directory for the current run
    run_id = f'{timestamp}-{prompt_strategy}'
    result_dir = log_dir = os.path.join(results_dir, run_id)
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # Initialize the OpenAI client
    openai_client = OpenAiClient(model=openai_model, role=openai_role, api_key=openai_api_key)

    # Load test data from an Excel file
    tender_test_data = os.path.join(test_data_dir, "tender-test-data.xlsx")
    dataframe = pandas.read_excel(tender_test_data)
    tender_test_results = []

    # Iterate over each row in the test data
    for row in dataframe.iterrows():
        data = row[1]
        index = data['Index']

        # If a specific index is provided, skip others
        if test_data_index is not None and test_data_index != index:
            continue

        # Load HTML content of the tender document
        tender_html = open(os.path.join(test_data_dir, 'tender-websites', str(index) + ".html"), 'r').read()
        tender_html_len = len(tender_html)

        # Retrieve examples based on the prompt strategy
        examples = get_examples(prompt_strategy)

        # Build the prompt
        prompt_builder = PromptBuilder()
        prompt = prompt_builder.build(prompt_strategy, str(tender_html), examples)

        # Save the generated prompt for reference
        save_prompt(result_dir, str(index), prompt)

        # Send the prompt to the OpenAI API and get the response
        response = openai_client.complete(prompt)

        # Save the HTML result from the API response
        save_html_result(result_dir, str(index), response.html_result)

        # Collect the results for further analysis
        tender_test_results.append(
            [index, data['Title'], response.duration, response.total_tokens, response.completion_tokens, response.prompt_tokens, tender_html_len, response.html_result is not None])

    # Save all results into an Excel file
    save_results_into_excel(result_dir, tender_test_results)
