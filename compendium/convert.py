import os
import csv
import random
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader
from urllib.parse import quote_plus
from urllib.parse import quote


# Custom filter to URL encode strings
def urlencode(value):
    # return quote_plus(value)
    return quote(value)


def hex():
    return "".join(random.choices("0123456789abcdef", k=8))


def starts_with_digit(value):
    return value and value[0] in "123456789"


# Set up the Jinja2 environment
env = Environment(loader=FileSystemLoader("./.jinja2"))
env.filters["starts_with_digit"] = starts_with_digit
env.filters["urlencode"] = urlencode


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
for csv_filename in os.listdir("./.csv"):
    if not csv_filename.endswith(".csv"):
        continue

    csv_filepath = os.path.join("./.csv", csv_filename)
    template_filename = csv_filename.replace(".csv", ".jinja2")
    template_filepath = os.path.join("./.jinja2", template_filename)
    index_template_filename = csv_filename.replace(".csv", "_index.jinja2")
    index_template_filepath = os.path.join("./.jinja2", index_template_filename)
    template = env.get_template(template_filename)

    with open(csv_filepath, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = []
        for row in reader:
            row = find_subrows(row)
            rows.append(row)
            md_filename = f"{row['Name']}.md".replace("’", "'").replace(": ", " ").replace(":", " ").replace("  ", " ")
            md_directory = os.path.join(".", csv_filename.replace(".csv", ""))
            os.makedirs(md_directory, exist_ok=True)
            md_filepath = os.path.join(md_directory, md_filename)

            # Render the template with the CSV row data
            md_content = template.render(row, hex=hex)

            # Write the rendered content to the Markdown file
            with open(md_filepath, "w") as md_file:
                md_file.write(md_content.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n"))

            print(f"Saved {md_filepath}")

    # Check for index template and generate index file if found
    if os.path.exists(index_template_filepath):
        index_template = env.get_template(index_template_filename)
        index_md_filename = f"{csv_filename.replace('.csv', '').capitalize()} Index.md"
        index_md_filepath = os.path.join(".", index_md_filename)
        index_content = index_template.render(rows=rows)

        with open(index_md_filepath, "w") as index_md_file:
            index_md_file.write(
                index_content.replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n")
            )
        print(f"Saved {index_md_filepath}")
