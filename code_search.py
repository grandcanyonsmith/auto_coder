
import logging
import os
from glob import glob
import unittest
import time

import openai
import pandas as pd
from openai.embeddings_utils import cosine_similarity, get_embedding

openai.api_key = "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"

logging.basicConfig(level=logging.INFO)

def get_function_name(code: str) -> str:
    """
    Extract the function name from a line beginning with "def ".
    """
    try:
        # Check if the code starts with "def"
        assert code.startswith("def ")
        # Return the function name
        return code[len("def "): code.index("(")]
    except AssertionError:
        # Log an error message if the code does not start with "def"
        logging.error("Function does not start with 'def'")
        raise

def get_until_no_space(all_lines: list, start_index: int) -> str:
    """
    Get all lines until a line outside the function definition is found.
    """
    ret = [all_lines[start_index]]
    # Set a limit of 10000 lines to avoid infinite loops
    for i in range(start_index + 1, start_index + 10000):
        # Check if the index is within the array length
        if i < len(all_lines):
            # Check if the line is empty
            if not all_lines[i].strip():
                # Add the line to the return value
                ret.append(all_lines[i])
            else:
                # Break out of the loop if a non-empty line is found
                break
    # Return all lines as a single string
    return "\n".join(ret)

def get_functions(filepath: str) -> list:
    """
    Get all functions in a Python file.
    """
    try:
        # Open the file
        with open(filepath) as f:
            # Read the content, replacing any carriage returns with new lines
            whole_code = f.read().replace("\r", "\n")
        # Split the content into lines
        all_lines = whole_code.split("\n")
        functions = []
        # Loop through each line
        for i, line in enumerate(all_lines):
            # Check if the line starts with "def"
            if line.startswith("def "):
                # Get all the lines until the end of the function definition
                code = get_until_no_space(all_lines, i)
                # Get the function name
                function_name = get_function_name(code)
                # Add the function details to the list
                functions.append(
                    {"code": code, "function_name": function_name, "filepath": filepath}
                )
        return functions
    except FileNotFoundError:
        # Log an error message if the file is not found
        logging.error("File not found")
        raise

def get_all_functions(code_root: str) -> list:
    """
    Get all functions from all Python files in the given directory.
    """
    try:
        # Get the list of all Python files in the directory
        code_files = [
            y for x in os.walk(code_root) for y in glob(os.path.join(x[0], "*.py"))
        ]
        # Filter out venv files
        code_files = [x for x in code_files if "venv" not in x]
        all_funcs = []
        # Loop through each Python file
        for code_file in code_files:
            # Get the functions from the file
            funcs = get_functions(code_file)
            # Add the functions to the list
            all_funcs.extend(iter(funcs))
        return all_funcs
    except TypeError:
        # Log an error message if the argument type is invalid
        logging.error("Invalid argument type")
        raise

def search_functions(
    df: pd.DataFrame,
    code_query: str,
    num_results: int = 3,
    pprint: bool = True,
    num_lines: int = 7,
) -> pd.DataFrame:
    """
    Search for functions similar to the given code query.
    """
    logging.info("Getting embedding for code query")
    try:
        # Get the embedding for the code query
        embedding = get_embedding(code_query, engine="text-embedding-ada-002")
        # Get the cosine similarities between the embedding and the dataframe embeddings
        df["similarities"] = df.code_embedding.apply(
            lambda x: cosine_similarity(x, embedding)
        )

        # Sort the dataframe in descending order of similarities
        res = df.sort_values("similarities", ascending=False).head(num_results)
        # Print the results
        if pprint:
            for r in res.iterrows():
                logging.info(
                    f"{r[1].filepath}:{r[1].function_name}  score={str(round(r[1].similarities, 3))}"
                )
                logging.info("\n".join(r[1].code.split("\n")[:num_lines]))
                logging.info("-" * 70)
                return res
    except TypeError:
        # Log an error message if the argument type is invalid
        logging.error("Invalid argument type")
        raise

# Logging and error handling
def log_error(error_message: str):
    logging.error(error_message)

# Unit Testing
class TestSearchFunctions(unittest.TestCase):
    def test_search_functions(self):
        self.assertEqual(search_functions([], "test_code", 3, True, 7).shape, (3, 5))


def main():
    # Performance optimization
    start = time.time()
    # Get the user's home directory
    root_dir = os.path.expanduser("~")
    logging.info(f"Root directory: {root_dir}")

    # Set the root directory for the code
    code_root = "."
    logging.info(f"Code root: {code_root}")

    # Get the functions from all Python files in the directory
    all_funcs = get_all_functions(code_root)

    # Security checks
    if not all_funcs:
        print("No functions found.")
        return

    # Create a dataframe from the list of functions
    df = pd.DataFrame(all_funcs)
    # Get the embeddings for each function
    df["code_embedding"] = df.code.apply(
        lambda x: get_embedding(x, engine="text-embedding-ada-002")
    )
    # Print the total number of functions with embeddings
    print("Total number of functions with embeddings:", len(df))
    # Set the code query
    code_query = "github"
    # Search for functions similar to the code query
    end = time.time()
    print("Time taken:", end - start)
    return search_functions(df, code_query, num_results=3, pprint=True, num_lines=7)


# Documentation
if __name__ == "__main__":
    """
    The main method searches for functions similar to the given code query.
    """
    main()