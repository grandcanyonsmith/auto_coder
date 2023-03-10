# Import necessary libraries
import json
import logging
import os
from collections import deque

# import environ
import openai

# openai.api_key = os.environ.get("OPENAI_API_KEY")

conversation_history_path = "files/text/open_ai_responses.jsonl"


class OpenAIConversation:
    def __init__(
        self,
        past_text,
        temperature=0,
        # temperature=0.7,
        max_tokens=5,
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


# # Import necessary libraries
# import json
# import logging
# import os
# from collections import deque
# import multiprocessing
# import numpy as np

# import openai

# # Declare variables
# conversation_history_path = "files/text/open_ai_responses.jsonl"

# # Check if OpenAI API key is provided
# if not openai.api_key:
#     logging.error("No OpenAI API key provided")
#     exit(1)


# class OpenAIConversation:
#     def __init__(
#         self,
#         past_text,
#         temperature=0.7,
#         max_tokens=80,
#         top_p=1,
#         frequency_penalty=0.5,
#         presence_penalty=0.5,
#         model="text-davinci-003",
#     ):
#         # Validate user input
#         if not past_text:
#             logging.error("No user input provided")
#             return None

#         # Assign parameters to class variables
#         self.past_text = past_text
#         self.temperature = temperature
#         self.max_tokens = max_tokens
#         self.top_p = top_p
#         self.frequency_penalty = frequency_penalty
#         self.presence_penalty = presence_penalty
#         self.model = model
#         self.prompt = f"{past_text}AI:"
#         self.response = None
#         self.cache = {}

#     def generate_reply(self):
#         # Try to get response from OpenAI
#         try:
#             self.response = openai.Completion.create(
#                 model=self.model,
#                 prompt=self.prompt,
#                 temperature=self.temperature,
#                 max_tokens=self.max_tokens,
#                 top_p=self.top_p,
#                 frequency_penalty=self.frequency_penalty,
#                 presence_penalty=self.presence_penalty,
#             )
#         except Exception as e:
#             logging.error(f"Error getting response from OpenAI: {e}")
#             return None

#         # Assign response to class variable
#         self.response = self.response.choices[0].text
#         print("AI:", self.response)

#         # Cache conversation history
#         self.cache[self.prompt] = self.response
#         # Validate conversation_history_path
#         if not os.path.exists(conversation_history_path):
#             logging.error(
#                 f"Error writing to {conversation_history_path}: File does not exist"
#             )
#             return None
#         # Try to write to conversation_history_path
#         try:
#             # Create a memory buffer
#             memory_buffer = deque()
#             # Create a process to write to the memory buffer
#             process = multiprocessing.Process(target=self.write_to_buffer, args=(memory_buffer,))
#             # Start the process
#             process.start()
#             # Wait for the process to finish
#             process.join()
#             # Write the contents of the memory buffer to the file
#             np.savetxt(conversation_history_path, list(memory_buffer), fmt="%s")
#         except Exception as e:
#             logging.error(f"Error writing to {conversation_history_path}: {e}")
#             return None

#         # Validate response
#         if not self.response:
#             logging.error("No response generated")
#             return None

#         # Return response without the first character
#         return self.response[1:] if self.response else None

#     def write_to_buffer(self, memory_buffer):
#         # Write the conversation history to the memory buffer
#         memory_buffer.extend(list(self.cache.items()))
