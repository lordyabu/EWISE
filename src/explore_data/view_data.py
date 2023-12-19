import json
import os.path

from config import DATA_PATH
# Load the list from the file
with open(os.path.join(DATA_PATH, 'elsevier_journal-of-macroeconomics.json'), 'r') as json_file:
    loaded_list = json.load(json_file)

# Print the contents of the list
for v in loaded_list:
    print(v)
