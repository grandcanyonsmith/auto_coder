import argparse
import datetime
import json
import logging
import os
import re
import readline
import shutil
import subprocess
import sys
import textwrap
import time

import boto3
import openai
import termcolor

# openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = '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'



def get_code_from_file(file_path: str) -> str:
    """
    Gets the code from a file.
    :param file_path: the path to the file
    :return: the code
    """
    code = ""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                code = file.read()
        except Exception as e:
            print(f"Error getting code from file:{e}")
            logging.error(f"Error getting code from file: {e}")
    else:
        print(f"Error: file path {file_path} does not exist.")
        logging.error(f"Error: file path {file_path} does not exist.")
    return code


def replace_broken_code_with_new_code(file_path: str, new_code: str) -> None:
    """
    Replaces the code in a file.
    :param file_path: the path to the file
    :param new_code: the new code to replace the old code
    :return: None
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "w") as file:
                file.write(new_code)
        except Exception as e:
            print(f"Error replacing code in file: {e}")
            logging.error(f"Error replacing code in file: {e}")
    else:
        print(f"Error: file path {file_path} does not exist.")
        logging.error(f"Error: file path {file_path} does not exist.")


def write_error_message_to_file(file_path: str, code: str) -> None:
    """
    Writes the error to a file.
    :param file_path: the file path
    :param code: the code to write
    :return: None
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "a") as file:
                file.write(code + "\n")
        except Exception as e:
            print(f"Error writing error to file: {e}")
            logging.error(f"Error writing error to file: {e}")
    else:
        print(f"Error: file path {file_path} does not exist.")
        logging.error(f"Error: file path {file_path} does not exist.")


def get_function_code(file_path: str, function_name: str) -> str:
    """
    Gets the code of the function.
    :param file_path: the path to the file
    :param function_name: the name of the function to get the code of
    :return: the code of the function
    """
    code = ""
    if os.path.exists(file_path):
        in_function = False
        try:
            with open(file_path, "r") as file:
                for line in file:
                    if f"def {function_name}(" in line:
                        code += f"{line}"
                        in_function = True
                    elif in_function and line == "\n":
                        code += "\n"
                        in_function = False
                        break
                    elif in_function:
                        code += f"{line}"
                # return code
        except Exception as e:
            print(f"Error getting function code: {e}")
            logging.error(f"Error getting function code: {e}")
    else:
        print(f"Error: file path {file_path} does not exist.")
        logging.error(f"Error: file path {file_path} does not exist.")
    print("\n\n\n")
    print(code)
    print("\n\n\n")

    return code


def replace_function(function_name, file_path, new_code):
    """
    Replaces the function with new code.
    :param: file_path: the path to the file
    :param: function_name: the name of the function
    :param: new_code: the new code
    :return: None
    """
    with open(file_path, "r") as file:
        code = file.read()
    start = code.find(f"def {function_name}(")
    end = code.find("\n\n", start)

    new_code = new_code.replace("    ", "\t")
    replaced_code = code[:start] + new_code
    replaced_code = replaced_code + code[end:]
    replace_broken_code_with_new_code(file_path, replaced_code)


def format_code(file_path):
    """
    Formats the code
    :param: file_path: the path to the file
    :return: None
    """
    with open(file_path, "r") as file:
        code = file.read()
    with open(file_path, "w") as file:
        file.write(textwrap.dedent(code))
        os.system(f"black {file_path}")