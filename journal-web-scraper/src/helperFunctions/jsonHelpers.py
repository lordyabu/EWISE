from config import DATA_PATH
import json
import os
def load_json_as_dict(file_name):
    """
    Loads a JSON file and returns it as a Python dictionary.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        dict: The content of the JSON file.
    """
    with open(os.path.join(DATA_PATH ,file_name), 'r', encoding='utf-8') as f:
        return json.load(f)


def save_dict_as_json(data_dict, file_name):
    """
    Saves a dictionary as a JSON file.

    Args:
        data_dict (dict): The dictionary to save.
        file_name (str): The name of the file to save the dictionary in.
    """
    with open(os.path.join(DATA_PATH ,file_name), 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)