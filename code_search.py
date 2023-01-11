
import os
from glob import glob
import pandas as pd
import logging

import openai
from openai.embeddings_utils import cosine_similarity, get_embedding


logging.basicConfig(level=logging.INFO)

def get_function_name(code: str) -> str:
    """
    Extract the function name from a line beginning with "def ".
    """
    assert code.startswith("def ")
    return code[len("def "): code.index("(")]


def get_until_no_space(all_lines: list, start_index: int) -> str:
    """
    Get all lines until a line outside the function definition is found.
    """
    ret = [all_lines[start_index]]
    for i in range(start_index + 1, start_index + 10000):
        if i < len(all_lines):
            if not all_lines[i].strip():
                ret.append(all_lines[i])
            else:
                break
    return "\n".join(ret)


def get_functions(filepath: str) -> list:
    """
    Get all functions in a Python file.
    """
    with open(filepath) as f:
        whole_code = f.read().replace("\r", "\n")
    all_lines = whole_code.split("\n")
    functions = []
    for i, line in enumerate(all_lines):
        if line.startswith("def "):
            code = get_until_no_space(all_lines, i)
            function_name = get_function_name(code)
            functions.append({"code": code, "function_name": function_name, "filepath": filepath})
    return functions


def get_all_functions(code_root: str) -> list:
    """
    Get all functions from all Python files in the given directory.
    """
    code_files = [y for x in os.walk(code_root)
                  for y in glob(os.path.join(x[0], "*.py"))]
    # skip venv files
    code_files = [x for x in code_files if "venv" not in x]
    all_funcs = []
    for code_file in code_files:
        funcs = get_functions(code_file)
        all_funcs.extend(iter(funcs))
    return all_funcs


def search_functions(df: pd.DataFrame, code_query: str, num_results: int = 3, pprint: bool = True, num_lines: int = 7) -> pd.DataFrame:
    """
    Search for functions similar to the given code query.
    """
    logging.info("Getting embedding for code query")
    embedding = get_embedding(code_query, engine="text-embedding-ada-002")
    df["similarities"] = df.code_embedding.apply(
        lambda x: cosine_similarity(x, embedding)
    )

    res = df.sort_values("similarities", ascending=False).head(num_results)
    if pprint:
        for r in res.iterrows():
            logging.info(
                f"{r[1].filepath}:{r[1].function_name}  score={str(round(r[1].similarities, 3))}"
            )
            logging.info("\n".join(r[1].code.split("\n")[:num_lines]))
            logging.info("-" * 70)
    return res


def main() -> None:
    root_dir = os.path.expanduser("~")
    logging.info(f"Root directory: {root_dir}")

    code_root = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/auto_coder"
    logging.info(f"Code root: {code_root}")

    all_funcs = get_all_functions(code_root)


    if not all_funcs:
        print("No functions found.")
        return
    
    df = pd.DataFrame(all_funcs)
    df["code_embedding"] = df.code.apply(lambda x: get_embedding(x, engine="text-embedding-ada-002"))
    print("Total number of functions with embeddings:", len(df))
    code_query = "github"
    return search_functions(df, code_query, num_results=3, pprint=True, num_lines=7)

if __name__ == "__main__":
    main()