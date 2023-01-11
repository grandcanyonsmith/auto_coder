import argparse
import contextlib

import openai

from user_interface_utils import allow_user_to_select_suggestions


class CodeImprover:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file_contents = self._read_file(filepath)
        self.file_type = self._get_file_type()
        self.selected_suggestions = None

    @contextlib.contextmanager
    def _read_file(self, filepath):
        """Reads a file and returns its contents"""
        with open(filepath, "r") as file:
            yield file.read()

    @contextlib.contextmanager
    def _write_file(self, filepath, content):
        """Writes content to a file"""
        with open(filepath, "w") as file:
            yield file.write(content)
            file.close()

    def _get_file_type(self):
        """Gets the file type of the code file"""
        if self.filepath.endswith(".py"):
            return "python"
        # add more file types as necessary
        else:
            raise ValueError(f"Unsupported file type: {self.filepath}")

    def _get_file_content(self):
        """Gets the content of the code file"""
        with self._read_file(self.filepath) as file:
            return file

    def _get_suggestions_for_improvement(self, prompt):
        """API: Get the suggestions for code improvement from the OpenAI API"""
        response = openai.Completion.create(
            engine="code-davinci-002",
            # engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].text

    def get_possible_improvement_categories(self):
        """Gets the possible categories for code improvement based on file type and contents"""
        instruction = f"List specific improvement categories for {self.file_type} code file with contents:\n{self._get_file_content()}"
        print("instruction", instruction)
        return self._get_suggestions_for_improvement(instruction)

    def get_improvement_actions(self, improvement_category):
        """Gets the specific actions for the selected category of code improvement"""
        instruction = f"List specific things that need to be done for '{improvement_category}' improvement category for {self.file_type} code file with contents:\n{self._get_file_content()}"
        print("improve action instruction", instruction)
        return self._get_suggestions_for_improvement(instruction)

    def _select_suggestions(self, suggestions, category):
        """Select suggestions from the list of suggestions for the given category of code improvement"""
        self.selected_suggestions = suggestions
        return self.selected_suggestions

    def select_suggestions(self, suggestions, category):
        """Wrapper for _select_suggestions, to make it more readable"""
        return self._select_suggestions(suggestions, category)

    def apply_improvements(self, suggestions, old_code):
        """Apply the selected suggestions to the code"""
        instruction = f"#### Implement the following suggestions in {self.file_type} code file with contents:\n\n### Old Code\n{old_code}\n\n\n### Suggestions{suggestions}\n\n\n### New Code"
        print("apply improvement instruction", instruction)
        improved_code = self._get_suggestions_for_improvement(instruction)
        with self._write_file(self.filepath, improved_code) as file:
            return improved_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()
    code_improvement = CodeImprover(args.filepath)
    possible_improvement_categories = (
        code_improvement.get_possible_improvement_categories()
    )
    print(possible_improvement_categories)
    selected_category = code_improvement.select_suggestions(
        possible_improvement_categories, "Code Improvement Categories"
    )
    print(selected_category)
    improvement_actions = code_improvement.get_improvement_actions(selected_category)
    print(improvement_actions)
    selected_improvements = code_improvement.select_suggestions(
        improvement_actions, selected_category
    )
    print(selected_improvements)
    code_improvement.apply_improvements(
        selected_improvements, code_improvement._get_file_content()
    )


### TODO
# - Set engine as a parameter
# - Add more file types
# - Fix the categories. Right now it just dumps the categories. It should be a list of categories with their respective actions based on the file type and contents
# - Refactor selected_category
# - Fix the prompts to match the prompts in the older version of auto_improve_code. The prompts should be formatted correctly.