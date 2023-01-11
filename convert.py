
import json
import re

from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

FILE_NAME = input("Enter file name: ")

def clean_text(text):
    """Removes all non-alphanumeric characters from the text."""
    text = " ".join(text.split())
    return re.sub("[^A-Za-z0-9 ]+", "", text)


def read_text_file(filename):
    """Reads the contents of a text file."""
    with open(filename, "r") as f:
        text = f.read()
    return text


def lemmatize_text(text):
    """Lemmatizes the text."""
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])


def remove_stop_words(text):
    """Removes stop words from the text."""
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    return " ".join([word for word in word_tokens if word not in stop_words])


def stem_text(text):
    """Stems the text."""
    stemmer = PorterStemmer()
    return " ".join([stemmer.stem(word) for word in text.split()])


def create_dict_list(text):
    """Creates a list of dictionaries from the text."""
    text_list = text.split("\n")
    return [{"text": item} for item in text_list if item != ""]


def convert_to_json(filename):
    """Converts the text file to a JSON object."""
    text = read_text_file(filename)
    text = clean_text(text)
    text = remove_stop_words(text)
    text = stem_text(text)
    text = lemmatize_text(text)
    text_list = create_dict_list(text)
    json_text = json.dumps(text_list)
    # print(json_text)
    for item in text_list:
        print(item["text"], end=" ")
    return json_text


if __name__ == "__main__":
    convert_to_json(FILE_NAME)
