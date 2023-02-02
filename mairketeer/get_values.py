import json


def get_background_information(info_name):
    """
    Open the background information file and return the info_name
    :return: a list
    """
    return list(_get_data_from_file("examples/background_information.jsonl")[info_name].values())


def get_hooks_examples_from_file():
    """
    Open the hook examples file and return the hooks
    :return: a string of hooks
    """
    return "\n".join(json.loads(line)["hook"] for line in open("examples/hook_examples.jsonl", "r"))


def _get_data_from_file(file_name):
    """
    Open a file and return the data
    :param file_name: the name of the file
    :return: the data of the file
    """
    return json.load(open(file_name))
