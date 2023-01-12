# Import necessary libraries
import json
import logging
import os
from collections import deque

# import environ
import openai

# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = "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"
conversation_history_path = "files/text/open_ai_responses.jsonl"


class OpenAIConversation:
    def __init__(
        self,
        past_text,
        temperature=0,
        # temperature=0.7,
        max_tokens=100,
        top_p=1,
        # frequency_penalty=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    ):
        # Validate user input
        if not past_text:
            logging.error("No user input provided")
            return None

        # Assign parameters to class variables
        self.past_text = past_text
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.model = model
        self.prompt = f"{past_text}AI:"
        self.response = None
        self.cache = []

    def generate_reply(self):
        # Try to get response from OpenAI
        try:
            self.response = openai.Completion.create(
                model=self.model,
                prompt=self.prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
        except Exception as e:
            logging.error(f"Error getting response from OpenAI: {e}")
            return None

        # Assign response to class variable
        self.response = self.response.choices[0].text
        print("AI:", self.response)

        # Cache conversation history
        self.cache.append({"prompt": self.prompt, "response": self.response})
        # Validate conversation_history_path
        if not os.path.exists(conversation_history_path):
            logging.error(
                f"Error writing to {conversation_history_path}: File does not exist"
            )
            return None
        # Try to write to conversation_history_path
        try:
            with open(conversation_history_path, "a") as f:
                for conversation in self.cache:
                    f.write(json.dumps(conversation) + "\n")
        except Exception as e:
            logging.error(f"Error writing to {conversation_history_path}: {e}")
            return None

        # Validate response
        if not self.response:
            logging.error("No response generated")
            return None

        # Return response without the first character
        return self.response[1:] if self.response else None



'''

import os
import json
import logging
import openai
import argparse

openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    openai.api_key = "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"

conversation_history_path = "files/text/open_ai_responses.jsonl"


def main(args):
    """
    This function is responsible for getting the user input,
    responding to it, and recording the results
    """
    # Define deque structure
    q = deque([], maxlen=10)

    # Get user input
    while True:
        text = input("You: ")
        if not text:
            break
        q.append(text)
        print(reply(args, " ".join(q)))


def reply(args, text):
    """
    This function is responsible for instantiating the
    OpenAIConversation class and getting a response
    """
    # Create instance of OpenAIConversation class
    chatbot = OpenAIConversation(
        args,
        past_text=text,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        frequency_penalty=args.frequency_penalty,
        presence_penalty=args.presence_penalty,
        model=args.model,
    )

    # Try to generate a reply
    try:
        reply = chatbot.generate_reply()
    except Exception as e:
        logging.error(f"Error generating reply: {e}")
        return None

    # Return reply
    return reply


class OpenAIConversation:
    def __init__(
        self,
        args,
        past_text,
        temperature=0,
        # temperature=0.7,
        max_tokens=100,
        top_p=1,
        # frequency_penalty=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        model="text-davinci-003",
    ):
        # Validate user input
        if not past_text:
            logging.error("No user input provided")
            return None

        # Assign parameters to class variables
        self.past_text = past_text
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty
        self.model = model
        self.prompt = f"{past_text}AI:"
        self.response = None
        self.cache = []

    def generate_reply(self):
        # Try to get response from OpenAI
        try:
            self.response = openai.Completion.create(
                model=self.model,
                prompt=self.prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                frequency_penalty=self.frequency_penalty,
                presence_penalty=self.presence_penalty,
            )
        except Exception as e:
            logging.error(f"Error getting response from OpenAI: {e}")
            return None

        # Assign response to class variable
        self.response = self.response.choices[0].text
        print("AI:", self.response)

        # Cache conversation history
        self.cache.append({"prompt": self.prompt, "response": self.response})

        # If the user wants to cache the conversation history
        if args.cache:
            # Validate conversation_history_path
            if not os.path.exists(conversation_history_path):
                logging.error(
                    f"Error writing to {conversation_history_path}: File does not exist"
                )
                return None
            # Try to write to conversation_history_path
            try:
                with open(conversation_history_path, "a") as f:
                    for conversation in self.cache:
                        f.write(json.dumps(conversation) + "\n")
            except Exception as e:
                logging.error(
                    f"Error writing to {conversation_history_path}: {e}"
                )
                return None

        # Validate response
        if not self.response:
            logging.error("No response generated")
            return None

        # Return response without the first character
        return self.response[1:] if self.response else None


if __name__ == "__main__":
    # Get command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--temperature", default=0, type=float, help="Temperature"
    )
    parser.add_argument(
        "--max_tokens", default=100, type=int, help="Max tokens"
    )
    parser.add_argument("--top_p", default=1, type=float, help="Top p")
    parser.add_argument(
        "--frequency_penalty", default=0, type=float, help="Frequency penalty"
    )
    parser.add_argument(
        "--presence_penalty", default=0, type=float, help="Presence penalty"
    )
    parser.add_argument(
        "--model", default="text-davinci-003", type=str, help="Model"
    )
    parser.add_argument(
        "--cache", action="store_true", help="Cache conversation history"
    )
    args = parser.parse_args()

    # Call main()
    main(args)



## Learning Objectives

- Get a response from the OpenAI API
- Use a command line interface (CLI) to get user input
- Cache the conversation history


## Instructions

- Navigate to the [OpenAI API](https://openai.com/docs/api/#generative-apis) and click on **Sign Up**.
- Fill out the form for the API key.
- On the left-hand side of the page click **API Keys**.
- Click **Copy** to copy the API key.
- Create a file called `.env` in the root directory of the project.
- In the `.env` file, set the `OPENAI_API_KEY` environmental variable to the API key you copied.
- Run `source .env` to load the environmental variable.
- Run `pipenv install` to install the necessary dependencies.
- Run `pipenv run python chatbot.py` and chat with the AI!



## Challenge

- [ ] Consider how to specify the command line arguments in a more user-friendly way.
- [ ] Add a feature to the program that allows the user to save the conversation history.
- [ ] Add a feature where the user can select the model to use.
- [ ] Add a feature where the user can select the number of responses to generate.
- [ ] Add a feature where the user can add text to the conversation history.'''