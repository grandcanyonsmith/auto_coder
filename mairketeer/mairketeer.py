import os
import json
import logging
from typing import List

import openai # Add comment for OpenAI module

# Set OpenAI api key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Replace hardcoded value with environment variable
openai.api_key = OPENAI_API_KEY # Replace hardcoded value with environment variable

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Add logging configuration

def strip_numbers_from_list(text_list: List[str]) -> List[str]:
    """Strip numbers from the beginning of each line in a list of text."""
    return [line.lstrip("1234567890.") for line in text_list if not line.startswith(' ') and line]

def add_numbers_in_front_of_list(text_list: List[str]) -> List[str]:
    """Add numbers in front of each line in a list of text."""
    print("textlist",text_list)
    return [f'{i+1}. {line}' for i, line in enumerate(text_list) if not line.startswith(' ') and line]

def create_value_proposition_for_email_sequence(ctas: List[str]) -> List[str]:
    """Create value propositions for a sequence of calls to action."""
    value_propositions = []

    for cta in ctas:
        prompt = f"Please provide a value proposition for the following call to action:\n\"\"\"\n{cta}\n\"\"\"\n"
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
            logging.exception("Failed to create value proposition") # Add logging
            raise Exception(
                "Failed to create value proposition. Please check the OpenAI API key and try again."
            ) from e

        value_propositions.append(response["choices"][0]["text"])

    return value_propositions

def convert_list_to_jsonl_format(text_list: List[str]) -> List[dict]:
    """Convert list of text to jsonl format."""
    return [{'step_sequence': item} for item in text_list]

def create_steps_for_email_sequence(background_information: str, desired_outcome: str, number_of_emails: int) -> str:
    """Create email sequence steps."""
    prompt = f"Please create a detailed email sequence based on the following information:\n\nBackground information:\n\"\"\"\n{background_information}\n\"\"\"\n\nDesired Outcome:\n\"\"\"\n{desired_outcome}\n\"\"\"\n\nNumber of emails in the email sequence:\n\"\"\"\n{number_of_emails}\n\"\"\"\n"
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
        logging.exception("Failed to create steps") # Add logging
        raise Exception(
            "Failed to create steps. Please check the OpenAI API key and try again."
        ) from e

    return response["choices"][0]["text"]

def create_ctas_for_email_sequence(subject_lines: List[str]) -> List[str]:
    """Create call to action for each subject line in email sequence."""
    ctas = []

    for subject_line in subject_lines:
        prompt = f"Please provide a call to action for the following subject line:\n\"\"\"\n{subject_line}\n\"\"\"\n"
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
            logging.exception("Failed to create call to action") # Add logging
            raise Exception(
                "Failed to create call to action. Please check the OpenAI API key and try again."
            ) from e

        ctas.append(response["choices"][0]["text"])

    return ctas

def get_number_of_emails_from_user() -> int:
    """Ask user for the number of emails in the sequence."""
    while True:
        try:
            number_of_emails = int(
                input("Please enter the number of emails in your sequence: "))
            break
        except Exception as e:
            logging.exception("Invalid input") # Add logging
            print("Invalid input. Please enter a valid number as the number of emails in the sequence.") # Add error handling

    return number_of_emails

def get_background_information_for_sequence() -> str:
    """Ask user for background information of the email sequence."""
    try:
        with open('files/background_information.txt', 'r') as file:
            background_information = file.read().replace('\n', '')
    except Exception as e:
        logging.exception("Failed to get background information") # Add logging
        raise Exception("Failed to get background information. Please check the file path and try again.") # Add error handling

    return background_information