## Table of Contents
- [__init__.py](#__init__-py)
- [openapi_converter_main.py](#openapi_converter_main-py)
- [openapi_converter.py](#openapi_converter-py)
- [md_content_aggregator.py](#md_content_aggregator-py)


## Directory Structure
```json
[
  {"type":"directory","name":"./src","contents":[
    {"type":"directory","name":"__pycache__","contents":[
      {"type":"file","name":"openapi_converter.cpython-311.pyc"},
      {"type":"file","name":"src-__pycache__-content.md"}
    ]},
    {"type":"file","name":"__init__.py"},
    {"type":"file","name":"md_content_aggregator.py"},
    {"type":"file","name":"openapi_converter_main.py"},
    {"type":"file","name":"openapi_converter.py"}
  ]}
,
  {"type":"report","directories":2,"files":6}
]

```


### __init__.py
```python

```


### openapi_converter_main.py
```python
\# Filename is openapi\_converter\_main.py
\# This file contains the main function to convert an OpenAPI 3.0 spec to 3.1

import argparse
import openapi_converter as converter 
import yaml
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file', nargs='?', default=None)
    args = parser.parse_args()

    if args.output_file is None:
        base_name = os.path.splitext(args.input_file)[0]  # Get the name without extension
        args.output_file = os.path.join(os.getcwd(), f"{base_name}.yml")

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' does not exist.")

    with open(args.input_file, 'r') as f:
        openapi_dict = yaml.safe_load(f.read())  # <-- Fixed here

    try:
        converted_spec = converter.convert_openapi(openapi_dict)
        with open(args.output_file, 'w') as f:
            f.write(converted_spec)
        print(f"Converted spec saved to {args.output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()

```


### openapi_converter.py
```python
\# Filename openapi\_converter.py
\# This module contains functions to convert an OpenAPI 3.0 spec to 3.1

import yaml
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.INFO)

def convert_openapi(openapi_dict):
    \# Input validation

    validate_required_fields(openapi_dict)
    validate_openapi_version(openapi_dict, versions=["3.0.0", "3.1.0"])
    check_incompatible_inputs(openapi_dict, incompatible_keys=["securityDefinitions"])

    \# Retain operation details

    for path in openapi_dict['paths'].values():
        for operation in path.values():
            if 'description' in operation:
                operation['x-original-description'] = operation['description']
            if 'operationId' in operation:
                operation['x-original-operationId'] = operation['operationId']

    \# Retain schema details

    for schema in openapi_dict['components']['schemas'].values():
        if 'description' in schema:
            schema['x-original-description'] = schema['description']

    \# Update to OpenAPI version 3.1.0

    openapi_dict['openapi'] = "3.1.0"

    \# Security schemes

    security_schemes = {}

    if 'securityDefinitions' in openapi_dict:
        logging.warning(
            f"'securityDefinitions' found - converting to 'securitySchemes'. "
            "This key is deprecated in OpenAPI 3.1.0 and should be replaced with 'securitySchemes'."
        )
        security_definitions = openapi_dict.pop('securityDefinitions')
        for def_name, definition in security_definitions.items():
            scheme = {
                'type': definition.get('type', 'http'),
                'scheme': definition.get('scheme', 'bearer')
            }
            if 'bearerFormat' in definition:
                scheme['bearerFormat'] = definition['bearerFormat']
            if 'description' in definition:
                scheme['description'] = definition['description']
            security_schemes[def_name] = scheme

    openapi_dict['components']['securitySchemes'] = security_schemes

    \# YAML conversion

    yaml_string = yaml.dump(openapi_dict, sort_keys=True)

    return yaml_string

\# Input validation functions

def validate_required_fields(openapi_dict):
    required_fields = ['openapi', 'info', 'paths']
    for field in required_fields:
        if field not in openapi_dict:
            raise Exception(f"Field '{field}' is required")

def validate_openapi_version(openapi_dict, versions=["3.0.0", "3.1.0"]):
    if openapi_dict['openapi'] not in versions:
        raise Exception(
            f"Input version must be one of {versions}. Found {openapi_dict['openapi']}"
        )

def check_incompatible_inputs(openapi_dict, incompatible_keys=['securityDefinitions']):
    for key in incompatible_keys:
        if key in openapi_dict:
            raise Exception(f"Input contains deprecated key '{key}'.")

```


### md_content_aggregator.py
```python
'''
Name: md_content_aggregator.py

Purpose:
The MD Content Aggregator is designed to scan a directory structure, extracting content from files that match specific criteria, and generate a content.md file for each directory and an all-contents.md file in the root directory. The generated files contain aggregated content from the scanned files, appropriately formatted in Markdown.

Methods and Functionalities:
- escape_markdown_characters_in_python_code(code: str) -> str:
    Escapes markdown special characters in a given string containing Python code to ensure they're not interpreted as markdown formatting.

- get_repo_structure(directory: str) -> str:
    Uses the tree command to generate a JSON representation of the directory structure.

- should_include(file_path: str, is_dir: bool = False) -> bool:
    Determines if a file or directory should be included based on specified patterns and extensions.

- directory_structure(directory: str) -> str:
    Retrieve the structure of a specific directory in JSON format.

- generate_filename(directory: str) -> str:
    Generates the filename for the content.md file based on the directory structure.

- generate_md_files(directory: str) -> None:
    Asynchronously processes a directory to identify files for aggregation and generate a content.md file.

- combine_md_files() -> None:
    Generates the all-contents.md file in the root directory by combining all the content.md files.

- process_directory(directory: str) -> None:
    Recursively processes directories to generate content.md files.

- main() -> None:
    The main asynchronous function that initiates the content aggregation process.

Configuration and Constants:
- EXCLUDED_EXTENSIONS: File extensions that are to be ignored.
- EXCLUSIVE_EXTENSION: Patterns and directories that the content aggregation process should exclusively focus on.
- Logging: Captures information, warnings, and error messages to script.log.

How to Use:
1. Ensure the script has access to the directories you wish to scan.
2. Run the script.
3. Once complete, find a content.md file in each directory and an all-contents.md file in the root directory.

Note: The script uses asynchronous file operations for improved performance with a large number of files or large-sized files. Ensure required libraries are installed.
'''

import os
import asyncio
import aiofiles
import logging
import fnmatch
import subprocess
import re


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("script.log"), logging.StreamHandler()])


ALLOWED_EXTENSIONS = ['*.py', '*.md']
EXCLUDED_EXTENSIONS = ['.db', '.log', '.sh', '.pyc', 'content.md']

EXCLUDED_DIRECTORIES = ['.git']
ALLOWED_DIRECTORIES = ['docs/*', 'git-utils/*', 'src/*', '.']


added_content = set()


def escape_markdown_characters_in_python_code(code: str) -> str:
    """Escape markdown special characters within Python code."""
    lines = code.split('\n')
    escaped_lines = []
    for line in lines:
        if line.strip().startswith("#"):
            line = line.replace("#", r"\#")
            line = line.replace("*", r"\*")
            line = line.replace("_", r"\_")
            line = line.replace("[", r"\[")
            line = line.replace("]", r"\]")
            line = line.replace("(", r"\(")
            line = line.replace(")", r"\)")
            line = line.replace(">", r"\>")
            line = line.replace("-", r"\-")
        escaped_lines.append(line)
    return '\n'.join(escaped_lines)

def get_repo_structure(directory):
    """Retrieve the repository structure in JSON format."""
    try:
        result = subprocess.run(['tree', '--dirsfirst', '-J', directory],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting repo structure: {e}")
        return ""

def should_include(file_path, is_dir=False):
    """
    Determine if a file or directory should be included based on allowed and excluded patterns.
    """
    if is_dir:
        if file_path in EXCLUDED_DIRECTORIES:
            return False
        return any(check in file_path for check in ALLOWED_DIRECTORIES)

    if any(fnmatch.fnmatch(file_path, pattern) for pattern in EXCLUDED_EXTENSIONS):
        return False

    return any(fnmatch.fnmatch(file_path, pattern) for pattern in ALLOWED_EXTENSIONS)

def directory_structure(directory):
    """Retrieve the structure of a specific directory in JSON format."""
    try:
        result = subprocess.run(['tree', '--dirsfirst', '-J', directory],
                                capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting directory structure: {e}")
        return ""



def generate_filename(directory):
    """Generate filename based on the directory structure."""
    if directory == ".":
        return "root-content.md"
    else:
        parts = [part for part in directory.split(os.sep) if part != "."]
        return "-".join(parts) + "-content.md"

async def generate_md_files(directory):
    """Generate content.md files for the specified directory."""
    logging.info(f"Processing directory: {directory}")
    content_filepath = os.path.join(directory, generate_filename(directory))
    \# Delete the existing content.md file if it exists
    if os.path.exists(content_filepath):
        os.remove(content_filepath)
    toc_content = "## Table of Contents\n"
    dir_structure = f"\n\n## Directory Structure\n```json\n{directory_structure(directory)}\n```\n\n"
    file_content_list = []

    for entry in os.scandir(directory):
        if entry.is_file() and should_include(entry.path) and entry.name != content_filepath:
            try:
                async with aiofiles.open(entry.path, 'r', encoding='utf-8') as f:
                    file_content = await f.read()

                if file_content in added_content:
                    continue
                added_content.add(file_content)

                toc_content += f"- [{entry.name}](#{entry.name.replace('.', '-')})\n"

                if entry.name.endswith('.py'):
                    file_content = escape_markdown_characters_in_python_code(file_content)
                    file_content_list.append(f"\n### {entry.name}\n```python\n{file_content}\n```\n")
                elif entry.name.endswith('.md'):
                    file_content_list.append(f"\n### {entry.name}\n{file_content}\n")
            except UnicodeDecodeError:
                logging.warning(f"Unable to read file {entry.name} as it's not in UTF-8 encoding. Skipping.")

    async with aiofiles.open(content_filepath, 'w') as f:
        await f.write(toc_content + dir_structure + '\n'.join(file_content_list))


def combine_md_files():
    combined_content_sections = ["# Project Documentation\n\n", "## Table of Contents\n"]
    \# Delete the existing all\-contents.md file if it exists
    if os.path.exists("all-contents.md"):
        os.remove("all-contents.md")
    toc_links = set()

    for directory, _, filenames in os.walk("."):
        content_md_name = generate_filename(directory)
        content_md_path = os.path.join(directory, content_md_name)
        if content_md_name in filenames:
            logging.info(f"Reading {content_md_path}")
            with open(content_md_path, 'r', encoding='utf-8') as f:
                content = f.read()

            sections = content.split("\n## ")
            toc_section = sections[0]
            toc_links.update(re.findall(r"- \[.*?\]\(.*?\)", toc_section))
            for section in sections[1:]:
                combined_content_sections.append("## " + section)

    combined_content_sections.insert(2, "\n".join(toc_links))
    combined_content_sections.append("\n\n## Repo Structure\n```json\n")
    combined_content_sections.append(get_repo_structure("."))
    combined_content_sections.append("\n```\n\n")

    with open("all-contents.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(combined_content_sections))



async def process_directory(directory):
    """Process a directory and its subdirectories to generate content.md files."""
    logging.info(f"Checking directory: {directory}")
    if should_include(directory, is_dir=True):
        await generate_md_files(directory)


    for entry in os.scandir(directory):
        if entry.is_dir() and should_include(entry.path, is_dir=True):
            await process_directory(entry.path)

async def main():
    """Main asynchronous function to start content aggregation."""
    global added_content
    added_content = set()  # Reset the set
    await process_directory(".")
    combine_md_files()

if __name__ == "__main__":
    asyncio.run(main())
```
