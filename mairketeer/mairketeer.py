import openai
import os
import json
import logging
from typing import List

# Set OpenAI api key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def strip_numbers_from_list(text_list: List[str]) -> List[str]:
    """Strip numbers from the beginning of each line in a list of text

    Arguments:
        text_list {list} -- List of text to be stripped

    Returns:
        list -- Stripped lines 
    """
    stripped_lines = []
    for line in text_list:
        if not line.startswith(' ') and line:
            stripped_lines.append(line.lstrip("1234567890."))

    return stripped_lines


def add_numbers_in_front_of_list(text_list: List[str]) -> List[str]:
    """Add numbers in front of each line in a list of text

    Arguments:
        text_list {list} -- List of text to be numbered

    Returns:
        list -- Numbered lines 
    """
    numbered_lines = []
    for i, line in enumerate(text_list):
        if not line.startswith(' ') and line:
            numbered_lines.append(f'{i+1}. {line}')

    return numbered_lines


def create_value_proposition_for_email_sequence(ctas: List[str]) -> List[str]:
    """Create value propositions for a sequence of calls to action

    Arguments:
        ctas {list} -- List of calls to action

    Returns:
        list -- List of value propositions
    """
    value_propositions = []
    for cta in ctas:
        prompt = f"Call to action:\n\"\"\"\n{cta}\n\"\"\"\n\nValue proposition for the email:\n\"\"\"\n"
        
        # Use OpenAI to create value proposition
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0
            )
        except Exception as e:
            logging.exception("Failed to create value proposition")
            raise Exception("Failed to create value proposition")
        
        value_propositions.append(response["choices"][0]["text"])
    return value_propositions


def convert_list_to_jsonl_format(text_list: List[str]) -> List[dict]:
    """Convert list of text to jsonl format

    Arguments:
        text_list {list} -- List of text

    Returns:
        list -- List of jsonl dicts
    """
    jsonl_list = []
    for item in text_list:
        jsonl_dict = {'step_sequence': item}
        jsonl_list.append(jsonl_dict)
    return jsonl_list


def create_steps_for_email_sequence(background_information: str, desired_outcome: str, number_of_emails: int) -> str:
    """Create email sequence steps

    Arguments:
        background_information {str} -- Background information
        desired_outcome {str} -- Desired outcome
        number_of_emails {int} -- Number of emails

    Returns:
        str -- Email sequence steps
    """
    prompt = f"Background information:\n\"\"\"\n{background_information}\n\"\"\"\n\nDesired Outcome:\n\"\"\"\n{desired_outcome}\n\"\"\"\n\nNumber of emails in the email sequence:\n\"\"\"\n{number_of_emails}\n\"\"\"\n\nSteps in email sequence\n\"\"\"\n"
    
    # Use OpenAI to create steps
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0
        )
    except Exception as e:
        logging.exception("Failed to create steps")
        raise Exception("Failed to create steps")
    
    return response["choices"][0]["text"]


def create_ctas_for_email_sequence(subject_lines: List[str]) -> List[str]:
    """Create call to action for each subject line in email sequence

    Arguments:
        subject_lines {list} -- List of subject lines

    Returns:
        list -- List of calls to action
    """
    ctas = []
    for subject_line in subject_lines:
        prompt = f"Subject line:\n\"\"\"\n{subject_line}\n\"\"\"\n\nCall to action for the email:\n\"\"\"\n"
        
        # Use OpenAI to create call to action
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0.2,
                presence_penalty=0
            )
        except Exception as e:
            logging.exception("Failed to create call to action")
            raise Exception("Failed to create call to action")
        
        ctas.append(response["choices"][0]["text"])
    return ctas

def get_number_of_emails_from_user() -> int:
    """Ask user for the number of emails in the sequence

    Raises:
        Exception: If the number of emails is not a number

    Returns:
        int -- Number of emails
    """
    while True:
        try:
            number_of_emails = int(input("Please enter the number of emails in your sequence: "))
            break
        except Exception as e:
            logging.exception("Invalid input")
            print("Invalid input. Please enter a valid number of emails.")
    
    return number_of_emails


def get_background_information_for_sequence() -> str:
    """Ask user for background information of the email sequence

    Returns:
        str -- Background information
    """
    try:
        with open('files/background_information.txt', 'r') as file:
            background_information = file.read().replace('\n', '')
    except Exception as e:
        logging.exception("Failed to get background information")
        raise Exception("Failed to get background information")
    
    return background_information