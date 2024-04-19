import pandas as pd

def generate_key(Volume_issue, journal_name):
    new_entry = (Volume_issue, journal_name)
    return pd.factorize([new_entry])[0][0] + 1


# extraction_volume_issue = 'Volume 75, Issue 3'
# extraction_journal_name = 'Example Journal Nme'
#
# # Generate primary key for the new entry
# print(generate_key(extraction_volume_issue, extraction_journal_name))