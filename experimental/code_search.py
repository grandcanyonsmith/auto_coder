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
