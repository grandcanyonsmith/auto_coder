import argparse
import json
import logging
import re
import unittest
from typing import List

import requests
from nltk import pos_tag, wordnet
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO)

def handle_exception(func):
    """Decorator to handle exceptions in a function"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            print(f"Error: {e}")
            # Notify user of error via email
            error_notification(e)

    return wrapper


def error_notification(error_message: str):
    """Sends an email notification when an error occurs in the program"""
    # Set up email parameters
    data = {
        "from": "error-notification@example.com",
        "to": "admin@example.com",
        "subject": "Error notification",
        "text": error_message
    }
    # Make the API call
    response = requests.post(
        "https://api.example.com/send-email",
        data=json.dumps(data),
        headers={"Content-type": "application/json"}
    )
    # Log the response
    logging.info(response.text)


def preprocess_text(text: str) -> str:
    """Preprocesses a string by removing stop words, stemming, and lemmatizing."""
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    filtered_words = [word for word in word_tokens if word not in stop_words]
    text = " ".join(filtered_words)
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in text.split()]
    text = " ".join(stemmed_words)
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in text.split()]
    return " ".join(lemmatized_words)


def create_dict_list(text: str) -> List[dict]:
    """Creates a list of dictionaries from a string."""
    text_list = text.split("\n")
    return [
        {
            "text": item,
            "pos": pos_tag([item])[0][1],
            "synonyms": get_synonyms(item)
        }
        for item in text_list if item.strip()
    ]

def get_synonyms(word):
    synonyms = [] 
    for syn in wordnet.synsets(word): 
        for l in syn.lemmas(): 
            synonyms.append(l.name()) 
    return list(set(synonyms))

@handle_exception
def convert_to_json(filename: str) -> str:
    """Converts a text file to a JSON string."""
    # Read data from file
    try:
        with open(filename, "r") as file:
            text = file.read()
    except Exception as e:
        logging.error(f"Error reading file: {e}")
    # Preprocess data
    text = re.sub("[^A-Za-z0-9 ]+", "", text)
    text = preprocess_text(text)
    text_list = create_dict_list(text)
    tagged_text = pos_tag(text_list[0]["text"].split())
    json_text = json.dumps(text_list)
    # Write data to file
    try:
        with open("files/output.json", "w") as outfile:
            json.dump(text_list, outfile)
    except Exception as e:
        logging.error(f"Error writing file: {e}")
    # Print data to console
    for item in text_list:
        if isinstance(item, dict):
            print(item["text"], end=" ")
    return json_text


def validate_input(filename: str) -> str:
    """Validates the input filename"""
    if not filename:
        raise ValueError("No filename provided")
    if not filename.endswith(".py"):
        raise ValueError("Invalid file format")
    return filename

def user_interface():
    """Displays a user interface for input"""
    # Initialize variables
    valid_input = False
    filename = ""
    # Keep looping until valid input is given
    while not valid_input:
        filename = input("Please enter the filename: ")
        try:
            validate_input(filename)
            valid_input = True
        except Exception as e:
            logging.error(e)
            print("Invalid filename. Please try again.")
    # Process file
    convert_to_json(filename)
    print("File processed successfully!")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Convert text file to JSON")
    parser.add_argument("filename", help="The file to convert")
    args = parser.parse_args()

    # Validate input
    try:
        validate_input(args.filename)
    except Exception as e:
        logging.error(e)
        # Display user interface for input
        user_interface()


class TestConvertToJson(unittest.TestCase):
    def test_convert_to_json(self):
        filename = "files/sample.txt"
        convert_to_json(filename)
        with open("files/output.json") as json_file:
            data = json.load(json_file)
        self.assertEqual(data[0]["text"], "hello world")
        self.assertGreater(len(data[0]["synonyms"]), 0)

    def test_validate_input(self):
        filename = "files/sample.txt"
        self.assertEqual(validate_input(filename), filename)

    def test_validate_input_error(self):
        filename = "files/sample.pdf"
        with self.assertRaises(ValueError):
            validate_input(filename)

    def test_preprocess_text(self):
        text = "Hello, world!"
        self.assertEqual(preprocess_text(text), "hello world")

    def test_create_dict_list(self):
        text = "Hello\nWorld"
        self.assertEqual(create_dict_list(text)[0]["text"], "Hello")
        self.assertGreater(len(create_dict_list(text)[0]["synonyms"]), 0)


if __name__ == "__main__":
    unittest.main()