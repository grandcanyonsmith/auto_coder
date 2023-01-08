
# New Feature 1

Create a Python function that reads all of the text in `conversations.jsonl`. Every 20 lines, it creates a one-line summary, unless the key says `summary`. The summary should display the timestamp, starting with the first and ending with the last (e.g., `12:49-13:05`). It should replace the previous 20 lines and have a key called `type`, with the value `summary`.

For example, if the conversation starts at 12:49 and ends at 13:05, the summary should be `12:49-13:05`.

This feature will help the AI quickly get an overview of the conversation without having to read through all of the lines when analyzing past conversations.

# New Feature 2