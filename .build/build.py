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


def hashify(input_string: str, length: int = 16) -> str:
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
    except:
        return False


# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader("./_jinja2"))
env.filters["starts_with_digit"] = starts_with_digit
env.filters["urlencode"] = urlencode
env.filters["slugify"] = slugify
env.filters["diceify"] = wrap_dice_notation
env.filters["hashify"] = hashify


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
    md_page_template, md_index_template, vtt_page_template = None, None, None

    sb_page_template = None
    sb_page_filename = csv_filename.replace(".csv", "_sb_page.jinja2")
    sb_page_filepath = os.path.join("./_jinja2", sb_page_filename)
    if os.path.exists(sb_page_filepath):
        sb_page_template = env.get_template(sb_page_filename)

    # Find all of the templates for this CSV file
    md_page_filename = csv_filename.replace(".csv", "_md_page.jinja2")
    md_page_filepath = os.path.join("./_jinja2", md_page_filename)
    if os.path.exists(md_page_filepath):
        md_page_template = env.get_template(md_page_filename)
    md_index_filename = csv_filename.replace(".csv", "_md_index.jinja2")
    md_index_filepath = os.path.join("./_jinja2", md_index_filename)
    if os.path.exists(md_index_filepath):
        md_index_template = env.get_template(md_index_filename)
    vtt_page_filename = csv_filename.replace(".csv", "_vtt_page.jinja2")
    vtt_page_filepath = os.path.join("./_jinja2", vtt_page_filename)
    vtt_page_template = None
    if os.path.exists(vtt_page_filepath):
        vtt_page_template = env.get_template(vtt_page_filename)
    vtt_index_filename = csv_filename.replace(".csv", "_vtt_index.jinja2")
    vtt_index_filepath = os.path.join("./_jinja2", vtt_index_filename)
    vtt_index_template = None
    if os.path.exists(vtt_index_filepath):
        vtt_index_template = env.get_template(vtt_index_filename)

    vtt_pages = []

    with open(csv_filepath, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            row = {key: value.strip() for key, value in row.items()}
            row = find_subrows(row)
            rows.append(row)
            md_filename = slugify(f"{row['Name']}.md")
            md_directory = os.path.join("../compendium", csv_filename.replace(".csv", ""))
            os.makedirs(md_directory, exist_ok=True)
            md_filepath = os.path.join(md_directory, md_filename)

            if md_page_template:
                # Render the template with the CSV row data
                hex_generator = HexGenerator(seed=row["Name"])
                md_page = md_page_template.render(row, hex=hex_generator.hex)
                # Write the rendered content to the Markdown file
                with open(md_filepath, "w") as md_file:
                    md_file.write(
                        md_page.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").rstrip()+"\n"
                    )

            sb_filename = slugify(f"{row['Name']}.md")
            sb_directory = os.path.join("silverbullet", csv_filename.replace(".csv", "").title())
            os.makedirs(sb_directory, exist_ok=True)
            sb_filepath = os.path.join(sb_directory, sb_filename)
            if sb_page_template:
                sb_page = sb_page_template.render(row)
                with open(sb_filepath, "w") as sb_file:
                    sb_file.write(
                        sb_page.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").rstrip()+"\n"
                    )

            if vtt_page_template:
                vtt_pages.append(
                    {
                        "_id": hashify(row["Name"]),
                        "name": row["Name"],
                        "type": "text",
                        "title": {"show": True, "level": 1},
                        "text": {
                            "format": 1,
                            "content": vtt_page_template.render(row),
                        },
                    }
                )

    # Check for index template and generate index file if found
    if md_index_template:
        index_md_content = md_index_template.render(rows=rows)
        with open(
            os.path.join("..", "compendium", f"{csv_filename.replace('.csv', '').capitalize()}.md"), "w"
        ) as index_md_file:
            index_md_file.write(
                index_md_content.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").rstrip()
            )

    # Write the Foundry JSON file
    if vtt_page_template:
        obj_name = csv_filename.replace(".csv", "").capitalize()
        with open(f"foundry-{csv_filename.replace('.csv', '.json')}", "w") as index_vtt_file:
            vtt_pages = sorted(vtt_pages, key=lambda x: x["name"])
            if vtt_index_template:
                vtt_pages.insert(
                    0,
                    {
                        "_id": hashify(obj_name + " Index"),
                        "name": obj_name + " Index",
                        "type": "text",
                        "title": {"show": True, "level": 1},
                        "text": {
                            "format": 1,
                            "content": vtt_index_template.render(rows=rows),
                        },
                    },
                )
            for i, page in enumerate(vtt_pages):
                page["sort"] = i * 10 + 10
            index_vtt_file.write(json.dumps({"name": obj_name, "pages": vtt_pages}, indent=2))
