def generate_key(journal_website, journal_name, volume, issue):
    # Convert journal website and journal name to a string of ASCII values
    website_code = ''.join(str(ord(char)) for char in journal_website)
    name_code = ''.join(str(ord(char)) for char in journal_name)

    # Ensure fixed length for volume and issue altogether (e.g., 6 digits in total)
    number_code = str(str(volume) + str(issue)).zfill(6)

    # Concatenate the parts to form the key
    key = website_code + name_code + number_code

    return key
