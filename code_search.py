import os
from glob import glob
import pandas as pd


def get_function_name(code):
    """
    Extract function name from a line beginning with "def "
    """
    assert code.startswith("def ")
    return code[len("def ") : code.index("(")]


def get_until_no_space(all_lines, i) -> str:
    """
    Get all lines until a line outside the function definition is found.
    """
    ret = [all_lines[i]]
    for j in range(i + 1, i + 10000):
        if j < len(all_lines):
            if len(all_lines[j]) == 0 or all_lines[j][0] in [" ", "\t", ")"]:
                ret.append(all_lines[j])
            else:
                break
    return "\n".join(ret)


def get_functions(filepath):
    """
    Get all functions in a Python file.
    """
    whole_code = open(filepath).read().replace("\r", "\n")
    all_lines = whole_code.split("\n")
    for i, l in enumerate(all_lines):
        if l.startswith("def "):
            code = get_until_no_space(all_lines, i)
            function_name = get_function_name(code)
            yield {"code": code, "function_name": function_name, "filepath": filepath}


# get user root directory
root_dir = os.path.expanduser("~")
print("Root directory:", root_dir)
# note: for this code to work, the openai-python repo must be downloaded and placed in your root directory

# path to code repository directory
code_root = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"
print("Code root:", code_root)

code_files = [y for x in os.walk(code_root) for y in glob(os.path.join(x[0], "*.py"))]
# skip venv files
code_files = [x for x in code_files if "venv" not in x]
print("Total number of py files:", len(code_files))

if not code_files:
    print(
        "Double check that you have downloaded the openai-python repo and set the code_root variable correctly."
    )

all_funcs = []
for code_file in code_files:
    funcs = list(get_functions(code_file))
    all_funcs.extend(iter(funcs))
print("Total number of functions extracted:", len(all_funcs))

from openai.embeddings_utils import get_embedding

df = pd.DataFrame(all_funcs)
df["code_embedding"] = df["code"].apply(
    lambda x: get_embedding(x, engine="text-embedding-ada-002")
)
df["filepath"] = df["filepath"].apply(lambda x: x.replace(code_root, ""))
df.to_csv("data/code_search_openai-python.csv", index=False)
df.head()


from openai.embeddings_utils import cosine_similarity


def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
    embedding = get_embedding(code_query, engine="text-embedding-ada-002")
    df["similarities"] = df.code_embedding.apply(
        lambda x: cosine_similarity(x, embedding)
    )

    res = df.sort_values("similarities", ascending=False).head(n)
    if pprint:
        for r in res.iterrows():
            print(
                r[1].filepath
                + ":"
                + r[1].function_name
                + "  score="
                + str(round(r[1].similarities, 3))
            )
            print("\n".join(r[1].code.split("\n")[:n_lines]))
            print("-" * 70)
    return res


res = search_functions(df, "searching github for functions", n=1, n_lines=20)


# import openai

# embedding = openai.Embedding.create(
#     input="f",
#     engine="text-embedding-ada-002"
# )["data"][0]["embedding"]
# len(embedding)


# import openai
# from tenacity import retry, wait_random_exponential, stop_after_attempt

# @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
# def get_embedding(text: str, engine="text-embedding-ada-002") -> list[float]:

#     # replace newlines, which can negatively affect performance.
#     text = text.replace("\n", " ")

#     return openai.Embedding.create(input=[text], engine=engine)["data"][0]["embedding"]


# embedding = get_embedding("Your text goes here", engine="text-embedding-ada-002")
# print(len(embedding))


import functools
import mmap
import os
import pickle
import re
import subprocess
from glob import glob

import openai
import pandas as pd
import termcolor
from openai.embeddings_utils import cosine_similarity, get_embedding
from sentence_transformers import SentenceTransformer

openai.api_key = "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"


def check_model_path(model):
    """
    Check if the model path exists.

    Args:
        model (str): The path to the model.

    Returns:
        bool: True if the model path exists, False otherwise.
    """
    return bool(os.path.exists(model))


def create_functions_csv(functions, filepath):
    """
    Apply the same indentation level to all lines of code within the function definition.

    Create a functions.csv file in the specified directory.

    """

    subprocess.call(["echo", "function,code", ">", filepath + "functions.csv"])
    for function in functions:
        subprocess.call(["echo", function + ",", ">>",
                        filepath + "functions.csv"])


def insert_code_into_functions_csv(filepath):
    """
    Insert the code into the 'code' column of the functions.csv file.
    """
    functions_df = pd.read_csv(filepath + "functions.csv", index_col=0)
    for index, row in functions_df.iterrows():
        if "code" not in functions_df.columns:
            functions_df.insert(1, "code", "")
        if index.lower() in filepath.lower():
            functions_df.at[index, "code"] = open(filepath, "r").read()
    functions_df.to_csv(filepath + "functions.csv")


def timer(func):
    """
    A timer decorator.
    """

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        import time

        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        print("")
        run_time = end_time - start_time
        run_time = termcolor.colored(f"{run_time:.4f}", "cyan")
        print(f"Finished {func.__name__!r} in {run_time} secs")
        return value

    return wrapper_timer


def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
    embedding = model.encode(code_query)
    df["similarities"] = df.code_embedding.apply(
        lambda x: cosine_similarity(x, embedding)
    )
    return df.sort_values("similarities", ascending=False).head(n)


def get_functions(filepath):
    """
    Get all functions in a Python file.
    """
    whole_code = open(filepath).read().replace("\r", "\n")
    all_lines = whole_code.split("\n")
    for i, l in enumerate(all_lines):
        if l.startswith("def "):
            code = get_until_no_space(all_lines, i)
            function_name = get_function_name(code)
            yield {"code": code, "function_name": function_name, "filepath": filepath}


def get_until_no_space(all_lines, i):
    """


    Get all lines until a line outside the function definition is found.

    """
    ret = [all_lines[i]]
    for j in range(i + 1, i + 10000):
        if j < len(all_lines):
            ret.append(all_lines[j])
            if len(all_lines[j]) != 0 and all_lines[j][0] not in [" ", "\t", ")"]:
                break

    return "\n".join(ret)


def get_function_name(code):
    """
    Extract function name from a line beginning with "def "
    """
    assert code.startswith("def ")
    return code[len("def "): code.index("(")]


def main(model):
    """

    # Instruct the AI to check if the file "functions.csv" exists in the specified directory.
    model.path = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"
    """

    if "df" not in globals():
        df = pd.DataFrame()
    model.path = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"

    model.path = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"
    # Instruct the AI to check if the "path" attribute is defined on the "model" object.
    if not hasattr(model, "path"):
        model.path = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"

    try:
        with open(f"{model.path}functions.csv", "r") as f:
            pass
    except FileNotFoundError:
        with open(f"{model.path}functions.csv", "w") as f:
            subprocess.call(
                ["echo", '"function", "description"',
                    ">", f"{model.path}functions.csv"]
            )

    if "all_funcs" not in globals():
        all_funcs = []
    if "df" not in globals():
        df = pd.DataFrame()
    if "code_files" not in globals():
        code_files = []
    if "code_root" not in globals():
        code_root = ""

    root_dir = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"
    code_root = root_dir
    code_files = [
        y
        for x in os.walk(code_root)
        for y in glob(os.path.join(x[0], "*.py"))
        if "venv" not in y and ".git" not in y and "lib" not in y
    ]
    print("Total number of py files:", len(code_files))
    # all_funcs = []
    # print(code_files)
    # for code_file in code_files:
    #     funcs = list(get_functions(code_file))
    #     all_funcs.extend(iter(funcs))
    # print("Total number of functions extracted:", len(all_funcs))
    # print(all_funcs)
    # df = pd.DataFrame(all_funcs)
    # df["code"] = df["code"].apply(lambda x: x.lower())
    # df["function_name"] = df["function_name"].apply(lambda x: x.lower())
    # df["code"] = df["code"].apply(lambda x: x.replace("    ", "\t"))
    # if "code" not in df.columns:
    #     df["code"] = df["code"].apply(lambda x: x.replace("\n", ""))
    # df["code"] = df["code"].apply(lambda x: x.replace("\t", "    "))

    # df["code"] = df["code"].apply(lambda x: x.replace("\n", ""))
    # if "code" not in df.columns:
    #     df["code"] = df["code"].apply(lambda x: x.replace("\r", ""))
    # df.to_csv("functions.csv", index=False)
    # df["code"] = df["code"].apply(lambda x: get_functions(x))
    # if "code" not in df.columns:
    #     df.insert(0, "code", "")
    # if "code" not in df.columns:
    #     df.insert(0, "code", "")
    # if "code" not in df.columns:
    #     df.insert(0, "code", "")

    # df.to_csv("files/functions.csv", index=False)
    # if "code" not in df.columns:
    #     df.insert(0, "code", "")

    all_funcs = []
    for code_file in code_files:
        funcs = list(get_functions(code_file))
        for func in funcs:
            all_funcs.append(func)

    print("Total number of functions extracted:", len(all_funcs))

    from openai.embeddings_utils import get_embedding

    df = pd.DataFrame(all_funcs)
    df['code_embedding'] = df['code'].apply(
        lambda x: get_embedding(x, engine='text-embedding-ada-002'))
    df['filepath'] = df['filepath'].apply(lambda x: x.replace(code_root, ""))
    # df.to_csv("data/code_search_openai-python.csv", index=False)
    df.head()

    # embed the code

    df.to_csv("files/functions.csv", index=False)

    # for index, row in df.iterrows():

    #     if "similarities" not in df.columns:

    #         df.insert(0, "similarities", "")
    #         print(
    #             termcolor.colored(row["function_name"], "blue"),
    #             termcolor.colored(round(float(row["similarities"]), 1), "green"),
    #         )
    #         print(row["code"])
    #         print(termcolor.colored(row["filepath"], "yellow"))
    from openai.embeddings_utils import cosine_similarity

    def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
        embedding = get_embedding(code_query, engine='text-embedding-ada-002')
        df['similarities'] = df.code_embedding.apply(
            lambda x: cosine_similarity(x, embedding))

        res = df.sort_values('similarities', ascending=False).head(n)
        if pprint:
            for r in res.iterrows():
                print(r[1].filepath+":"+r[1].function_name +
                      "  score=" + str(round(r[1].similarities, 3)))
                print("\n".join(r[1].code.split("\n")[:n_lines]))
                print('-'*70)
        return res

    res = search_functions(
        df, 'pdf extract text', n=5, n_lines=20)


if __name__ == "__main__":
    path = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/"

    if not os.path.exists("files/model.pkl"):
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("files/model.pkl not found, creating...")
        pickle.dump(model, open("files/model.pkl", "wb"))

    else:
    
        model = pickle.load(open("files/model.pkl", "rb"))
        # model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    main(model)
