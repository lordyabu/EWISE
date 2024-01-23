import pandas as pd

def generate_key(Volume_issue, journal_name):
    new_entry = (Volume_issue, journal_name)
    return pd.factorize([new_entry])[0][0] + 1
