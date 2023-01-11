import argparse
import logging
import contextlib

import openai
from user_interface_utils import allow_user_to_select_suggestions

openai.api_key = "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"

@contextlib.contextmanager
def read_file(file_path):
    with open(file_path, "r") as file:
        yield file.read()


@contextlib.contextmanager
def write_file(file_path, contents):
    with open(file_path, "w") as file:
        yield file.write(contents)
        file.close()


class CodeImprovement:
    def __init__(self, file_path):
        self.file_path = file_path
        with read_file(file_path) as file_contents:
            self.file_contents = file_contents
        self.file_type = "Python"
        self.selected_suggestions = []

    def _extract_improvement_suggestions(
        self, prompt, temperature, tokens, restart_sequence
    ) -> str:
        """
        given a prompt and a temperature value.
        """
        # restart_sequence = '"""'
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[restart_sequence],
        )

        return response["choices"][0]["text"]

    def get_possible_improvement_categories(self) -> str:
        """
        Get the possible improvement categories for the code.
        """
        prompt = f'##### List the specific improvement category types that can be made to the {self.file_type} below according to the instructions\n \
        \n### {self.file_type}\n"""\n{self.file_contents}\n#END\n"""\n\
        \n### Instructions\n"""\nUse the OpenAI API to get suggestions on how to improve the code.\n"""\n'
        return self._extract_improvement_suggestions(prompt, 0.7, 1000, '"""')

    def get_improvement_actions(self, improvement_category) -> str:
        prompt = f'\##### List the specific things that need to be done to {improvement_category} the {self.file_type} below according to the instructions\n \
        \n### {self.file_type}\n"""\n{self.file_contents}\n#END\n"""\n\
        \n### Instructions\n"""\nUse the OpenAI API to get suggestions on how to improve the code.\n"""\n'
        return self._extract_improvement_suggestions(prompt, 0, 1000, '"""')

    def apply_improvements(self, suggestions) -> str:
        prompt = f'\
        \n### Old {self.file_type}\n"""\n{self.file_contents}\n#END\n"""\n\
        \n### Instructions\n"""\n{suggestions}\n"""\n\
        \n### New {self.file_type}\n"""'
        with read_file(self.file_path) as improvements:
            improvements = self._extract_improvement_suggestions(prompt, 0, 3000, "#END")
        with write_file(self.file_path, improvements) as file:
            file.close()
        return improvements

    def select_suggestions(self, suggestions: str) -> tuple:
        """ """
        categories = allow_user_to_select_suggestions(suggestions)
        self.selected_suggestions = categories

        return self.selected_suggestions


if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    args = parser.parse_args()

    # Create a CodeImprovement object for a file called "code.py"
    code_improvement = CodeImprovement(args.file_path)

    # Get the possible improvement categories for the code
    improvement_categories = code_improvement.get_possible_improvement_categories()

    # Select the improvement categories to implement
    selected_categories = code_improvement.select_suggestions(
        improvement_categories)

    # Get the improvement actions for each selected improvement category
    improvement_actions = code_improvement.get_improvement_actions(
        selected_categories)

    # Select the improvements to implement
    selected_improvements = code_improvement.select_suggestions(
        improvement_actions)

    # Apply the selected improvements to the code
    try:
        code_improvement.apply_improvements(selected_improvements)
    except Exception as e:
        logging.exception(e)

    # Print the modified code
    print(code_improvement.file_contents)