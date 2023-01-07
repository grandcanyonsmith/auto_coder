import os
import re
import time
import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime
from tkinter import ttk

import inquirer
import keyboard
import openai
from inquirer.themes import GreenPassion
from user_interface_utils import allow_user_to_select_suggestions


class CodeImprovement:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_contents = self.read_file(file_path)
        self.file_type = "Python"

    def read_file(self, file_path: str) -> str:
        """Reads the contents of a file and returns it as a string."""
        try:
            with open(file_path, "r") as file:
                file_contents = file.read()
            return file_contents

        except FileNotFoundError:
            print("File not found.")
            return None

        except IOError:
            print("Error reading file.")
            return None

    def get_possible_improvement_categories(self) -> str:
        """
        Use the OpenAI API to get suggestions on how to improve the code.
        """

        prompt = f'Code:\n"""\n{self.file_contents}\n"""\n    \n    \nList the specific improvement category types that can be made to the {self.file_type} above:"""'
        return self._extract_improvement_suggestions(prompt, 0.7)

    def get_improvement_actions(self, improvement_category) -> str:
        """
        Use the OpenAI API to get suggestions on how to improve the code.
        """

        prompt = f'Code:\n"""\n{self.file_contents}\n"""\n    \n    \nList the specific things that need to be done to {improvement_category} the {self.file_type} above:"""'
        return self._extract_improvement_suggestions(prompt, 0)

    def select_suggestions(self, suggestions: str) -> tuple:
        """
        Selects the suggestions to implement using a GUI.
        """
        root = tk.Tk()
        frame = tk.Frame(root)
        frame.pack()
        label = tk.Label(frame, text="Select the suggestions you want to implement.")
        listbox = tk.Listbox(frame, selectmode="multiple")
        listbox.config(
            width=0,
            height=0,
            font=("Courier", 12),
            selectmode="multiple",
            activestyle="none",
            selectbackground="red",
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            background="black",
            fg="white",
        )

        for suggestion in suggestions.splitlines():
            listbox.insert("end", suggestion)

        button = tk.Button(
            frame, text="Select", command=lambda: self.on_select(listbox)
        )
        label.pack()
        listbox.pack()
        button.pack()
        root.mainloop()

        return self.selected_suggestions

    def on_select(self, listbox) -> list:
        """
        Gets the selected items from the listbox and closes the window.
        """

        selected_items = listbox.curselection()
        self.selected_suggestions = [listbox.get(item) for item in selected_items]
        print(self.selected_suggestions)
        root = listbox.master
        root.destroy()
        return self.selected_suggestions

    def apply_improvements(self, suggestions) -> str:
        """
        Uses the OpenAI API to implement the suggestions.
        """

        print(suggestions)
        restart_sequence = '#END"""'
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f'##### Fix bugs in the below {self.file_type} according to the instructions\n \
            \n### Buggy {self.file_type}\n"""\n{self.file_contents}\n#END\n"""\n\
            \n### Instructions\n"""\n{suggestions}\n"""\n\
            \n### Fixed {self.file_type}\n"""',
            temperature=0,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#END"],
        )
        with open(self.file_path, "w") as file:
            file.write(response["choices"][0]["text"])

        return response["choices"][0]["text"]

    def _extract_improvement_suggestions(self, prompt, temperature) -> str:
        """
        Uses the OpenAI API to get the code improvement suggestions
        given a prompt and a temperature value.
        """
        restart_sequence = '"""'
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


if __name__ == "__main__":

    # Create a CodeImprovement object for a file called "code.py"
    # code_improvement = CodeImprovement(input("Enter the file path: "))
    code_improvement = CodeImprovement("aws.py")

    # Get the possible improvement categories for the code
    improvement_categories = code_improvement.get_possible_improvement_categories()

    # Select the improvement categories to implement
    selected_categories = allow_user_to_select_suggestions(improvement_categories)

    # Get the improvement actions for each selected improvement category
    improvement_actions = code_improvement.get_improvement_actions(selected_categories)

    # Select the improvements to implement
    selected_improvements = allow_user_to_select_suggestions(improvement_actions)
    # Apply the selected improvements to the code
    code_improvement.apply_improvements(selected_improvements)

    # Print the modified code
    print(code_improvement.file_contents)