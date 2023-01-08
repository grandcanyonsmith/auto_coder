############################################################################################################# New
# import json
# import datetime
# import time
# import json
# import re

# import transformers
# from nltk import pos_tag
# from nltk.corpus import stopwords, wordnet
# from nltk.stem import PorterStemmer, WordNetLemmatizer
# from nltk.tokenize import word_tokenize
# from transformers import pipeline
# import nltk
# nltk.download('averaged_perceptron_tagger')
# start = time.time()


# def load_conversation(file_name):
#     """
#     Reads the contents of a file and returns them as a list.
#     """
#     with open(file_name, "r") as file:
#         conversation = file.readlines()
#         file.close()
#     return conversation


# def get_start_and_end_timestamps(conversation):
#     """
#     Extracts the start and end times of a conversation as a tuple.
#     """
#     conversation = [json.loads(line) for line in conversation]
#     start, end = None, None

#     start = min(line["timestamp"] for line in conversation if line["type"] != "summary")
#     end = max(line["timestamp"] for line in conversation if line["type"] != "summary")

#     return start, end


# def format_timestamp(timestamp):
#     """
#     Converts a Unix timestamp to a human-readable format.
#     """
#     return datetime.datetime.fromtimestamp(timestamp).strftime("%I:%M%p")


# def create_timestamped_summary(start, end, message_count):
#     """
#     Creates a summary line given the start and end times and the number of messages.
#     """
#     return {
#         "type": "summary",
#         "start": start,
#         "end": end,
#         "message_count": message_count,
#     }


# def replace_messages_with_timestamped_summary(conversation, summary_line):
#     """
#     Replaces the previous 20 lines with the new summary.
#     """
#     return [summary_line if i < 20 else line for i, line in enumerate(conversation)]


# def create_timestamped_summaries(conversation, message_count):
#     """
#     Creates a one-line summary every `message_count` lines, with a key of `type` and value of `summary`.
#     """
#     message_count = len(conversation) // message_count
#     return [
#         create_timestamped_summary(
#             conversation[i]["timestamp"],
#             conversation[i + message_count - 1]["timestamp"],
#             message_count,
#         )
#         for i, line in enumerate(conversation)
#         if i % message_count == 0
#     ]


# def replace_messages_with_timestamped_summaries(conversation, summary_lines):
#     """
#     Replaces the lines in the conversation with the provided summary lines.
#     """
#     summary_dict = {line["timestamp"]: line for line in summary_lines}
#     return [
#         summary_dict[line["timestamp"]] if line["type"] == "summary" else line
#         for line in conversation
#     ]


# def extract_last_messages(conversation, message_count):
#     """
#     Extracts the last `message_count` messages from `conversation` as a list.
#     """
#     return [json.loads(message_json) for message_json in conversation[-message_count:]]


# def generate_message_text(last_messages):
#     """
#     Generates a message text string from a list of messages.
#     """
#     message_text = ""
#     message_values = [message_json["message"] for message_json in last_messages]
#     return " ".join(message_values)


# def get_last_messages(conversation_file, message_count):
#     """
#     Reads the last `message_count` messages from a file and returns them as a string.
#     """
#     conversation = load_conversation(conversation_file)
#     last_messages = extract_last_messages(conversation, message_count)
#     return generate_message_text(last_messages)


# def create_summary_with_last_messages(text):
#     """
#     Creates a summary
#     returns a one-line summary
#     """
#     return main(text)


# def format_summary_json(start, end, new_summary):
#     return {
#         "timestamp": {"start": start, "end": end},
#         "type": "summary",
#         "text": new_summary,
#     }


# def replace_text_with_summary(new_summary):
#     """
#     takes that formatted json summary and replaces the last x amount of lines that it st summarized with it. then it writes it to the converson.jsonl file
#     """
#     conversation = load_conversation(conversation_file_name)
#     start, end = get_start_and_end_timestamps(conversation)
#     formatted_summary = format_summary_json(start, end, new_summary)
#     # conversation = load_conversation(conversation_file_name)
#     print(formatted_summary)
#     return formatted_summary


# def replace_last_lines_with_summary(conversation_file, summary):
#     # Read in the conversation from the file
#     with open(conversation_file, "r") as file:
#         conversation = file.readlines()
#         file.close()

#     # Erase the last 20 lines of the conversation
#     conversation = conversation[:-20]

#     # Add the new summary to the end of the conversation
#     conversation.append(json.dumps(summary))

#     # Write the updated conversation to the file
#     with open(conversation_file, "w") as file:
#         file.writelines(conversation)
#         file.close()


# def summarize_text(text):
#     # pass text to Transformer's Summarization object
#     summarizer = pipeline("summarization")
#     # use Part-of-Speech tagging
#     pos_tagged_text = pos_tag(word_tokenize(text))
#     # use lemmatization
#     lemmatized_words = [
#         WordNetLemmatizer().lemmatize(word, get_wordnet_pos(tag))
#         for word, tag in pos_tagged_text
#     ]
#     lemmatized_text = " ".join(lemmatized_words)
#     # use stemming
#     stemmed_words = [PorterStemmer().stem(word) for word in lemmatized_words]
#     stemmed_text = " ".join(stemmed_words)

#     return summarizer(stemmed_text, max_length=100, min_length=30, do_sample=False)[0][
#         "summary_text"
#     ]


# def get_wordnet_pos(treebank_tag):
#     if treebank_tag.startswith("J"):
#         return wordnet.ADJ
#     elif treebank_tag.startswith("V"):
#         return wordnet.VERB
#     elif treebank_tag.startswith("N"):
#         return wordnet.NOUN
#     elif treebank_tag.startswith("R"):
#         return wordnet.ADV
#     else:
#         return wordnet.NOUN


# def clean_text(text):
#     text = " ".join(text.split())
#     return re.sub("[^A-Za-z0-9 ]+", "", text)


# def read_text_file(filename):
#     with open(filename, "r") as f:
#         text = f.read()
#     return text


# # remove stop words
# def remove_stop_words(text):
#     stop_words = set(stopwords.words("english"))
#     word_tokens = word_tokenize(text)
#     return " ".join([word for word in word_tokens if word not in stop_words])


# def stem_text(text):
#     stemmer = PorterStemmer()
#     return " ".join([stemmer.stem(word) for word in text.split()])


# def main(text):
#     text = clean_text(text)
#     text = remove_stop_words(text)
#     text = stem_text(text)

#     text = summarize_text(text)
#     print(text)
#     return text


# conversation_file_name = "conversation.jsonl"  # Declare a variable to store the file

# message_count_limit = 20  # Declare a variable to store the loop limit
# text = get_last_messages(conversation_file_name, message_count_limit)
# new_summary = create_summary_with_last_messages(text)
# r = replace_text_with_summary(new_summary)
# replace_last_lines_with_summary(conversation_file_name, r)
# end = time.time()
# print(end - start)

import json
import datetime
import time
import re
import functools

import transformers
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from transformers import pipeline
# import nltk

# nltk.download('averaged_perceptron_tagger')

# @functools.lru_cache()
def load_conversation(file_name):
    """
    Reads the contents of a file and returns them as a list.
    """
    with open(file_name, "r") as file:
        conversation = [json.loads(line) for line in file]
    return conversation


# @functools.lru_cache()
def get_start_and_end_timestamps(conversation):
    """
    Extracts the start and end times of a conversation as a tuple.
    """
    start, end = None, None

    start = min(line["timestamp"] for line in conversation if line["type"] != "summary")
    end = max(line["timestamp"] for line in conversation if line["type"] != "summary")

    return start, end


def format_timestamp(timestamp):
    """
    Converts a Unix timestamp to a human-readable format.
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime("%I:%M%p")

def create_timestamped_summary(start, end, message_count):
    """
    Creates a summary line given the start and end times and the number of messages.
    """
    return {
        "type": "summary",
        "start": start,
        "end": end,
        "message_count": message_count,
    }

def replace_messages_with_timestamped_summary(conversation, summary_line):
    """
    Replaces the previous 20 lines with the new summary.
    """
    return [summary_line if i < 20 else line for i, line in enumerate(conversation)]

def create_timestamped_summaries(conversation, message_count):
    """
    Creates a one-line summary every `message_count` lines, with a key of `type` and value of `summary`.
    """
    message_count = len(conversation) // message_count
    return [
        create_timestamped_summary(
            conversation[i]["timestamp"],
            conversation[i + message_count - 1]["timestamp"],
            message_count,
        )
        for i, line in enumerate(conversation)
        if i % message_count == 0
    ]


def replace_messages_with_timestamped_summary(conversation, summary_line):
    """
    Replaces the previous 20 lines with the new summary.
    """
    return [summary_line if i < 20 else line for i, line in enumerate(conversation)]


def create_timestamped_summaries(conversation, message_count):
    """
    Creates a one-line summary every `message_count` lines, with a key of `type` and value of `summary`.
    """
    message_count = len(conversation) // message_count
    return [
        create_timestamped_summary(
            conversation[i]["timestamp"],
            conversation[i + message_count - 1]["timestamp"],
            message_count,
        )
        for i, line in enumerate(conversation)
        if i % message_count == 0
    ]


def replace_messages_with_timestamped_summaries(conversation, summary_lines):
    """
    Replaces the lines in the conversation with the provided summary lines.
    """
    summary_dict = {line["timestamp"]: line for line in summary_lines}
    return [
        summary_dict[line["timestamp"]] if line["type"] == "summary" else line
        for line in conversation
    ]

def extract_last_messages(conversation, message_count):
    """
    Extracts the last `message_count` messages from `conversation` as a list.
    """
    return [json.loads(message_json) for message_json in conversation[-message_count:]]

def generate_message_text(last_messages):
    """
    Generates a message text string from a list of messages.
    """
    message_text = ""
    message_values = [message_json["message"] for message_json in last_messages]
    return " ".join(message_values)

def get_last_messages(conversation_file, message_count):
    """
    Reads the last `message_count` messages from a file and returns them as a string.
    """
    conversation = load_conversation(conversation_file)
    last_messages = extract_last_messages(conversation, message_count)
    return generate_message_text(last_messages)

def summarize_conversation(conversation_file, message_count=20):
    """
    Summarizes a conversation by replacing every `message_count` messages with a summary line.
    """
    conversation = load_conversation(conversation_file)
    start, end = get_start_and_end_timestamps(conversation)
    summary_lines = create_timestamped_summaries(conversation, message_count)
    return replace_messages_with_timestamped_summaries(conversation, summary_lines)

def main():
    conversation_file = "conversation.jsonl"
    message_count = 20
    summarized_conversation = summarize_conversation(conversation_file, message_count)
    last_messages = get_last_messages(conversation_file, message_count)
    model = pipeline("text-summarization")
    summary = model(last_messages, max_length=100, min_length=30)
    summary_text = summary[0]["summary_text"]
    summary_line = {
        "type": "summary",
        "timestamp": time.time(),
        "message": summary_text,
    }
    summarized_conversation = replace_messages_with_timestamped_summary(summarized_conversation, summary_line)
    with open(conversation_file, "w") as file:
        for line in summarized_conversation:
            file.write(json.dumps(line))
            file.write("\n")


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Time taken: {end - start} seconds")
