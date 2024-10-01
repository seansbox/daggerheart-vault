import os
import csv
import random
import json
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from urllib.parse import quote_plus
from urllib.parse import quote
import hashlib
import string

# Define the base62 alphabet (lowercase, uppercase, and digits)
BASE62_ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits


def base62_encode(num: int) -> str:
    """Convert an integer to a base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]

    base62 = []
    base = len(BASE62_ALPHABET)

    while num:
        num, rem = divmod(num, base)
        base62.append(BASE62_ALPHABET[rem])

    return "".join(reversed(base62))


def string_to_alphanumeric_hash(input_string: str, length: int = 16) -> str:
    # Generate a SHA-256 hash of the input string and convert to an integer
    sha256_hash = hashlib.sha256(input_string.encode("utf-8")).digest()
    hash_int = int.from_bytes(sha256_hash, byteorder="big")

    # Convert the integer hash to base62 (alphanumeric characters)
    base62_hash = base62_encode(hash_int)

    # Return the first `length` characters of the base62-encoded hash
    return base62_hash[:length]


import re


def wrap_dice_notation(text):
    # Define the regex pattern for dice notation
    dice_pattern = re.compile(r"\b(\d*)[dD](\d+)([+-]\d+)?\b")

    # Replacement function to wrap the matched dice notation
    def replacer(match):
        full_match = match.group(0)
        return f"[[/roll {full_match}]]"

    # Substitute all occurrences in the text
    wrapped_text = dice_pattern.sub(replacer, text)
    return wrapped_text


# Custom filter to URL encode strings
def urlencode(value):
    return quote(value)


def slugify(value):
    return (
        value.replace("’", "'")
        .replace(": ", " ")
        .replace(":", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
    )


class HexGenerator:
    def __init__(self, seed):
        self.random_instance = random.Random(seed)

    def hex(self):
        return "".join(self.random_instance.choices("0123456789abcdef", k=8))


def starts_with_digit(value):
    try:
        return value[0] in "0123456789"
    except IndexError:
        return False


# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader("./_jinja2"))
env.filters["starts_with_digit"] = starts_with_digit
env.filters["urlencode"] = urlencode
env.filters["slugify"] = slugify
env.filters["diceify"] = wrap_dice_notation


# Function to process CSV rows and look for "subrows" (cols ending in 1-9)
def find_subrows(row):
    subrows = []
    dels = []
    for key, value in row.items():
        if key[-1] in "123456789":
            index = int(key[-1]) - 1
            subkey = key[:-1]
            while index >= len(subrows):
                subrows.append({})
            subrows[index][subkey] = value
            dels.append(key)
    for deli in dels:
        del row[deli]
    # Convert defaultdict to list of dictionaries
    row["subrows"] = subrows
    return dict(row)


# Loop through each CSV file in the ./csv directory
for csv_filename in os.listdir("./_csv"):
    if not csv_filename.endswith(".csv"):
        continue

    csv_filepath = os.path.join("./_csv", csv_filename)
    template_filename = csv_filename.replace(".csv", ".jinja2")
    template_filepath = os.path.join("./_jinja2", template_filename)
    template = env.get_template(template_filename)

    foundry_template_filename = csv_filename.replace(".csv", "_foundry.jinja2")
    foundry_template_filepath = os.path.join("./_jinja2", foundry_template_filename)
    foundry_template = None
    if os.path.exists(foundry_template_filepath):
        foundry_template = env.get_template(foundry_template_filename)

    index_template_filename = csv_filename.replace(".csv", "_index.jinja2")
    index_template_filepath = os.path.join("./_jinja2", index_template_filename)

    foundry_pages = []

    with open(csv_filepath, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            row = find_subrows(row)
            rows.append(row)
            md_filename = slugify(f"{row['Name']}.md")
            md_directory = os.path.join("../compendium", csv_filename.replace(".csv", ""))
            os.makedirs(md_directory, exist_ok=True)
            md_filepath = os.path.join(md_directory, md_filename)

            # Render the template with the CSV row data
            hex_generator = HexGenerator(seed=row["Name"])
            md_content = template.render(row, hex=hex_generator.hex)
            if foundry_template:
                foundry_pages.append(
                    {
                        "_id": string_to_alphanumeric_hash(row["Name"]),
                        "name": row["Name"],
                        "type": "text",
                        "title": {"show": True, "level": 1},
                        "text": {
                            "format": 1,
                            "content": foundry_template.render(row),
                        },
                    }
                )

            # Write the rendered content to the Markdown file
            with open(md_filepath, "w") as md_file:
                md_file.write(
                    md_content.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").rstrip()
                )

            print(f"Saved {md_filepath}")

    # Check for index template and generate index file if found
    if os.path.exists(index_template_filepath):
        index_template = env.get_template(index_template_filename)
        index_md_filename = f"{csv_filename.replace('.csv', '').capitalize()}.md"
        index_md_filepath = os.path.join("../compendium", index_md_filename)
        index_content = index_template.render(rows=rows)

        with open(index_md_filepath, "w") as index_md_file:
            index_md_file.write(
                index_content.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").rstrip()
            )
        print(f"Saved {index_md_filepath}")

    # Write the Foundry JSON file
    with open(f"foundry-{csv_filename.replace('.csv', '.json')}", "w") as foundry_file:
        foundry_pages = sorted(foundry_pages, key=lambda x: x["name"])
        for i, page in enumerate(foundry_pages):
            page["sort"] = i * 10 + 10
        foundry_file.write(
            json.dumps({"name": csv_filename.replace(".csv", "").capitalize(), "pages": foundry_pages}, indent=2)
        )
        print(f"Saved foundry-{csv_filename.replace('.csv', '.json')}")
