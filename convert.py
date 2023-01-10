import json
import re
from nltk import pos_tag, wordnet
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    """Preprocesses a string by removing stop words, stemming, and lemmatizing."""
    stop_words = set(stopwords.words("english"))
    word_tokens = word_tokenize(text)
    text = " ".join([word for word in word_tokens if word not in stop_words])
    stemmer = PorterStemmer()
    text = " ".join([stemmer.stem(word) for word in text.split()])
    lemmatizer = WordNetLemmatizer()
    return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

def create_dict_list(text):
    """Creates a list of dictionaries from a string."""
    text_list = text.split("\n")
    return [{"text": item} for item in text_list if item != ""]

def convert_to_json(filename):
    """Converts a text file to a JSON string."""
    with open(filename, "r") as file:
        text = file.read()
    text = re.sub("[^A-Za-z0-9 ]+", "", text)
    text = preprocess_text(text)
    text_list = create_dict_list(text)
    print(text_list)
    tagged_text = pos_tag(text_list[0]["text"].split())
    json_text = json.dump(text_list, open("output.json", "w"))
    for item in text_list:
        if not isinstance(item, dict):
            print(item["text"], end=" ")
    return json_text

if __name__ == "__main__":
    import time
    start = time.time()
    convert_to_json(input("Enter file name: "))
    end = time.time()
    print(f"Time taken: {end - start} seconds")