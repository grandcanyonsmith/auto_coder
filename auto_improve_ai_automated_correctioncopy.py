import argparse
import contextlib
import logging
import os
import random
import time

import openai

# Error Handling
try:
    openai.api_key = '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'
except Exception as e:
    openai.api_key = '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'
    logging.exception('Error: invalid OpenAI API key.')
    exit()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(name)s:%(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

# Argument Parsing
parser = argparse.ArgumentParser(description='Improve code file.')
parser.add_argument('filepath', help='path to the code file')
args = parser.parse_args()

# Read/Write File Handling
file_contents = ''
if os.path.exists(args.filepath):
    with contextlib.suppress(Exception):
        with open(args.filepath, 'r') as code_file:
            file_contents = code_file.read()
else:
    logging.error('Error: invalid file path.')
    exit()

# User Interface Utilization
class CodeImprover:
    def __init__(self, filepath, engine="text-davinci-003"):
        self.filepath = filepath
        self.file_contents = file_contents
        self.file_type = self._get_file_type()
        self.selected_suggestions = None
        self.engine = engine
    
    def _get_file_type(self):
        """Gets the file type of the code file"""
        if self.filepath.endswith(".py"):
            return "python"
        elif self.filepath.endswith(".js"):
            return "javascript"
        elif self.filepath.endswith(".java"):
            return "java"
        # add more file types as necessary
        else:
            logging.error(f"Unsupported file type: {self.filepath}")
            exit()
    
    def _get_file_content(self):
        """Gets the content of the code file"""
        try:
            with open(self.filepath, "r") as file:
                return file.read()
        except Exception as e:
            logging.exception(f"Error: {e}.")
            exit()
    
    def _get_suggestions_for_improvement(self, prompt):
        """API: Get the suggestions for code improvement from the OpenAI API"""
        try:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response.choices[0].text
        except Exception as e:
            logging.exception(f"Error: {e}.")
            exit()
    
    def _get_categories_and_actions(self):
        """Gets the possible categories for code improvement based on file type and contents"""
        instruction = f"List specific improvement categories and actions for {self.file_type} code file with contents:\n{self._get_file_content()}\nCode Refactoring, Syntax Refactoring, Algorithmic Optimization, Standardization of Code Style, Use of Optimized Library Functions, Logging of Code Performance Metrics, Automated Testing of Code"
        return self._get_suggestions_for_improvement(instruction)
    
    def _select_suggestions(self, category):
    
        """Select suggestions from the list of suggestions for the given category of code improvement"""
        suggestions = category.split(" ")
        self.selected_suggestions = self.allow_user_to_select_suggestions(suggestions)
        return self.selected_suggestions
    
    def select_suggestions(self, category):
        """Wrapper for _select_suggestions, to make it more readable"""
        return self._select_suggestions(category)
    
    def apply_improvements(self, suggestions, old_code):
        """Apply the selected suggestions to the code"""
        instruction = f"#### Implement the following suggestions in {self.file_type} code file with contents:\n\n### Old Code\n{old_code}\n\n\n### Suggestions\n{suggestions}\n\n\n### New Code"
        print("apply improvement instruction", instruction)
        start_time = time.time()
        improved_code = self._get_suggestions_for_improvement(instruction)
        end_time = time.time()
        logging.info(f'Time taken to generate improved code: {end_time - start_time} seconds')
        # Randomize the improved code
        improved_code = improved_code.replace(" ", "")
        improved_code = ''.join(random.sample(improved_code, len(improved_code)))
        with self._write_file(self.filepath, improved_code) as file:
            return improved_code
    
    def allow_user_to_select_suggestions(self, suggestions):
        """Allow the user to select which suggestions they would like to apply to the code"""
        selected_suggestions = []
        # Get user input
        user_input = input("Select the suggestions you would like to apply to the code (separated by commas): ")
        # Parse user input
        user_input_list = user_input.split(",")
        # Check if the user's input is valid
        for suggestion in suggestions:
            if suggestion in user_input_list:
                selected_suggestions.append(suggestion)
        # Return the selected suggestions
        return selected_suggestions
    
    @contextlib.contextmanager
    def _write_file(self, filepath, data):
        """Write the improved code to the code file"""
        try:
            with open(filepath, "w") as file:
                file.write(data)
            yield
        except Exception as e:
            logging.exception(f"Error: {e}.")
            exit()

if __name__ == "__main__":
    code_improvement = CodeImprover(args.filepath)
    category = (
        code_improvement._get_categories_and_actions()
    )
    print(category)
    selected_improvements = code_improvement.select_suggestions(
        category
    )
    print(selected_improvements)
    improved_code = code_improvement.apply_improvements(
        selected_improvements, code_improvement._get_file_content()
    )
    # Log the improved code
    logging.info(f'Improved code: \n{improved_code}')

    # Print success message
    logging.info("Successfully applied improvements to code file!")


# New but needs to be finished
'''
import argparse
import contextlib
import logging
import os
import time
import random

import openai

# Error Handling
try:
    openai.api_key = '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'
except Exception as e:
    logging.exception('Error: invalid OpenAI API key.')
    exit()

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(name)s:%(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

# Argument Parsing
parser = argparse.ArgumentParser(description='Improve code file.')
parser.add_argument('filepath', help='path to the code file')
args = parser.parse_args()

# Read/Write File Handling
file_contents = ''
if os.path.exists(args.filepath):
    with contextlib.suppress(Exception):
        with open(args.filepath, 'r') as code_file:
            file_contents = code_file.read()
else:
    logging.error('Error: invalid file path.')
    exit()

# User Interface Utilization
class CodeImprover:
    def __init__(self, filepath, engine="text-davinci-003"):
        self.filepath = filepath
        self.file_contents = file_contents
        self.file_type = self._get_file_type()
        self.selected_suggestions = None
        self.engine = engine
    
    def _get_file_type(self):
        """Gets the file type of the code file"""
        if self.filepath.endswith(".py"):
            return "python"
        elif self.filepath.endswith(".js"):
            return "javascript"
        elif self.filepath.endswith(".java"):
            return "java"
        # add more file types as necessary
        else:
            logging.error(f"Unsupported file type: {self.filepath}")
            exit()
    
    def _get_file_content(self):
        """Gets the content of the code file"""
        try:
            with open(self.filepath, "r") as file:
                return file.read()
        except Exception as e:
            logging.exception(f"Error: {e}.")
            exit()
    
    def _get_suggestions_for_improvement(self, prompt):
        """API: Get the suggestions for code improvement from the OpenAI API"""
        try:
            response = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            return response.choices[0].text
        except Exception as e:
            logging.exception(f"Error: {e}.")
            exit()
    
    def _get_categories_and_actions(self):
        """Gets the possible categories for code improvement based on file type and contents"""
        instruction = f"List specific improvement categories and actions for {self.file_type} code file with contents:\n{self._get_file_content()}\nCode Refactoring, Syntax Refactoring, Algorithmic Optimization, Standardization of Code Style, Use of Optimized Library Functions, Logging of Code Performance Metrics, Automated Testing of Code"
        return self._get_suggestions_for_improvement(instruction)
    
    def _select_suggestions(self, category):
        """Select suggestions from the list of suggestions for the given category of code improvement"""
        suggestions = category.split(" ")
        self.selected_suggestions = self.allow_user_to_select_suggestions(suggestions)
        return self.selected_suggestions
    
    def select_suggestions(self, category):
        """Wrapper for _select_suggestions, to make it more readable"""
        return self._select_suggestions(category)
    
    def apply_improvements(self, suggestions, old_code):
        """Apply the selected suggestions to the code"""
        instruction = f"#### Implement the following suggestions in {self.file_type} code file with contents:\n\n### Old Code\n{old_code}\n\n\n### Suggestions\n{suggestions}\n\n\n### New Code"
        print("apply improvement instruction", instruction)
        start_time = time.time()
        improved_code = self._get_suggestions_for_improvement(instruction)
        end_time = time.time()
        logging.info(f'Time taken to generate improved code: {end_time - start_time} seconds')
        # Randomize the improved code
        improved_code = improved_code.replace(" ", "")
        improved_code = ''.join(random.sample(improved_code, len(improved_code)))
        with self._write_file(self.filepath, improved_code) as file:
            return improved_code
    
    def allow_user_to_select_suggestions(self, suggestions):
        """Allow the user to select which suggestions they would like to apply to the code"""
        selected_suggestions = []
        # Get user input
        user_input = input("Select the suggestions you would like to apply to the code (separated by commas): ")
        # Parse user input
        user_input_list = user_input.split(",")
        # Check if the user's input is valid
        for suggestion in suggestions:
            if suggestion in user_input_list:
                selected_suggestions.append(suggestion)
        # Return the selected suggestions
        return selected_suggestions
    
    def _apply_code_refactoring(self, code):
        """Apply code refactoring to the code"""
        instruction = f"Code refactoring:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    def _apply_syntax_refactoring(self, code):
        """Apply syntax refactoring to the code"""
        instruction = f"Syntax refactoring:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    def _apply_algorithmic_optimization(self, code):
        """Apply algorithmic optimization to the code"""
        instruction = f"Algorithmic optimization:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    def _apply_standardization_of_code_style(self, code):
        """Apply standardization of code style to the code"""
        instruction = f"Standardization of code style:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    def _apply_use_of_optimized_library_functions(self, code):
        """Apply use of optimized library functions to the code"""
        instruction = f"Use of optimized library functions:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    def _apply_logging_of_code_performance_metrics(self, code):
        """Apply logging of code performance metrics to the code"""
        instruction = f"Logging of code performance metrics:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    def _apply_automated_testing_of_code(self, code):
        """Apply automated testing of code to the code"""
        instruction = f"Automated testing of code:\n{code}"
        return self._get_suggestions_for_improvement(instruction)
    
    @contextlib.contextmanager
    def _write_file(self, filepath, data):
        """Write the improved code to the code file"""
        try:
            with open(filepath, "w") as file:
                file.write(data)
            yield
        except Exception as e:
            logging.exception(f"Error: {e}.")
            exit()

if __name__ == "__main__":
'''