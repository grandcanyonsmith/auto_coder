
import json
import datetime

def convert_timestamp(timestamp):
    """
    This function converts a Unix timestamp to a human-readable format.
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime('%I:%M%p')

def summarize_conversation(file):
    """
    This function reads all of the text in `conversation.jsonl` and creates a one-line summary every 20 lines, unless the key says `summary`. The summary displays the timestamp, starting with the first and ending with the last (e.g., `12:49-13:05`). It replaces the previous 20 lines and has a key called `type`, with the value `summary`.
    """
    with open(file, 'r') as f:
        conversation = f.readlines()
        
    summary = ""
    start_time = ""
    end_time = ""
    count = 0
    for line in conversation:
        try:
            line = json.loads(line)
        except Exception:
            continue
        if line["type"] == "summary":
            continue
        if count == 0:
            start_time = convert_timestamp(line["timestamp"])
        end_time = convert_timestamp(line["timestamp"])
        count += 1
        if count == 20:
            timestamp = start_time + "-" + end_time
            line["type"] = "summary"
            line["message"] = "summary here"
            line["timestamp"] = timestamp
            # create a new function that replaces the 20 lines with the new summary
            replace_lines_with_summary(conversation, line)
            count = 0
            print(line)
    return summary

def replace_lines_with_summary(conversation, line):
    """
    This function replaces the previous 20 lines with the new summary.
    """
    for i in range(20):
        conversation[i] = line

print(summarize_conversation('conversation.jsonl'))
