
import json
import logging
import re
import unittest
from typing import List

from nltk import pos_tag, wordnet
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


def handle_exception(func):
    """Decorator to handle exceptions in a function"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            print(f"Error: {e}")

    return wrapper


logging.basicConfig(filename="files/log.txt", level=logging.ERROR)


@handle_exception
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


@handle_exception
def create_dict_list(text: str) -> List[dict]:
    """Creates a list of dictionaries from a string."""
    text_list = text.split("\n")
    return [{"text": item, "pos": pos_tag([item])[0][1]} for item in text_list if item.strip()]


@handle_exception
def convert_to_json(filename: str) -> str:
    """Converts a text file to a JSON string."""
    with open(filename, "r") as file:
        text = file.read()
    text = re.sub("[^A-Za-z0-9 ]+", "", text)
    text = preprocess_text(text)
    text_list = create_dict_list(text)
    tagged_text = pos_tag(text_list[0]["text"].split())
    json_text = json.dumps(text_list)
    with open("files/output.json", "w") as outfile:
        json.dump(text_list, outfile)
    for item in text_list:
        if isinstance(item, dict):
            print(item["text"], end=" ")
    return json_text


def validate_input(filename: str) -> str:
    """Validates the input filename"""
    if not filename:
        raise ValueError("No filename provided")
    if not filename.endswith(".txt"):
        raise ValueError("Invalid file format")
    return filename


if __name__ == "__main__":
    try:
        filename = input("Enter file name: ")
        validate_input(filename)
    except Exception as e:
        logging.error(e)


class TestConvertToJson(unittest.TestCase):
    def test_convert_to_json(self):
        filename = "files/sample.txt"
        convert_to_json(filename)
        with open("files/output.json") as json_file:
            data = json.load(json_file)
        self.assertEqual(data[0]["text"], "hello world")

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
        self.assertEqual(create_dict_list(text), [{"text": "Hello"}, {"text": "World"}])


if __name__ == "__main__":
    unittest.main()
