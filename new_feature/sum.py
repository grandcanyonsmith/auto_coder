import json
import datetime


def load_conversation(file_name):
    """
    Reads the contents of a file and returns them as a list.
    """
    with open(file_name, "r") as file:
        conversation = file.readlines()
        file.close()
    return conversation


def get_start_and_end_timestamps(conversation):
    """
    Extracts the start and end times of a conversation as a tuple.
    """
    conversation = [json.loads(line) for line in conversation]
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

# use convert to get sum


def create_summary_with_last_messages(text):
    """
    Creates a summary
    returns a one-line summary
    """
    # use one line summary tool

def format_summary_json(new_summary):
    """
    returns {"timestamp": {range of first to last timestamp}, "type": "{conversation_type... in this case,'summary'}", "text": "{one_line_summary_of_past_20_lines}}
    """


def replace_text_with_summary():
    """
    takes that formatted json summary and replaces the last x amount of lines that it st summarized with it. then it writes it to the converson.jsonl file
    """


conversation_file_name = "conversation.jsonl"  # Declare a variable to store the file

message_count_limit = 20  # Declare a variable to store the loop limit
text = get_last_messages(conversation_file_name, message_count_limit)
print(text)
# next steps are to stem, tokenize, lemmantize, remove stopwords, punctuation, and then summarize
