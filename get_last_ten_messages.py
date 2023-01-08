import json

# Declare a variable to store the file name
file_name = "conversation.jsonl"

# Declare a variable to store the loop limit
message_limit = 20


def get_last_ten_messages(file):
    """
    This function reads the last 10 messages from a file and prints them as a string.
    """
    # Use a try/except block to capture and handle any errors that may occur when opening the file.
    try:
        # open the file
        with open(file_name, "r") as file:
            # read the file
            file_data = file.readlines()
            # get the last 10 messages using a list comprehension
            last_ten_messages = [
                json.loads(message_json) for message_json in file_data[-message_limit:]
            ]
            # create an empty string
            message_text = ""
            # loop through the last 10 messages
            for message_json in last_ten_messages:
                # get the message key value
                message_value = message_json["message"]
                # add the message value to the string
                message_text += f"{message_value} "

            # print the string
            print(message_text)

    except Exception as e:
        print(f"An error occurred: {e}")

    # close the file
    file.close()


# call the function
get_last_ten_messages(file_name)
