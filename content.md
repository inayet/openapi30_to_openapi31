## Table of Contents
- [script.log](#script.log)
- [dir_structure](#dir_structure)
- [useful.git-commands](#useful.git-commands)
- [display_content_readme.py](#display_content_readme.py)
- [display_project_files.ignore](#display_project_files.ignore)
- [requirements.txt](#requirements.txt)
- [.gitignore](#.gitignore)
- [__init__.py](#__init__.py)
- [openapi_converter_main.py](#openapi_converter_main.py)
- [content.md](#content.md)
- [openapi_converter.py](#openapi_converter.py)
- [useful.git-commands-update-remote.py](#useful.git-commands-update-remote.py)
- [useful.git-create-new-repo.py](#useful.git-create-new-repo.py)
- [README.md](#README.md)
- [License](#License)

###BEGIN_AUTO_GENERATED###

### script.log
2023-08-16 11:05:19,178 - INFO - Directory already has a git repo


### dir_structure
.
├── calendars.json
├── content.md
├── dir_structure
├── display_content_readme.py
├── __init__.py
├── License
├── openapi_converter_main.py
├── openapi_converter.py
├── __pycache__
│   ├── content.md
│   ├── openapi_converter.cpython-311.pyc
│   └── README.md
├── README.md
├── requirements.txt
├── script.log
├── useful.git-commands
├── useful.git-create-new-repo.py
└── useful.git-create-new-repo.sh

2 directories, 17 files


### useful.git-commands
# Create a new GitHub repo

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your_username/your_repo.git
git push -u origin master

# Create the main, production, and development branches

git checkout -b main
git checkout -b production
git checkout -b development

# Update all branches

git fetch
git merge main production
git merge main development

# Switch back to the development branch

git checkout development

### display_content_readme.py
import os
import re
import asyncio
import aiofiles
import logging

logging.basicConfig(level=logging.INFO)

DEFAULT_IGNORE_PATTERNS = [r"\./__pycache__", r".*\.git.*", r".*\.env.*"]

CONCURRENT_TASKS_LIMIT = 4  # Adjust this based on your system's capacity and drive type
sem = asyncio.Semaphore(CONCURRENT_TASKS_LIMIT)

def compile_patterns(patterns):
    return [re.compile(pattern) for pattern in patterns]

async def should_ignore(item, compiled_patterns):
    for pattern in compiled_patterns:
        if pattern.search(item):
            logging.info(f"Ignoring item due to pattern {pattern.pattern}: {item}")
            return True
    logging.info(f"Item not ignored: {item}")
    return False

async def generate_md_files(directory, ignore_patterns):
    logging.info(f"Processing directory: {directory}")
    async with sem:
        content_filepath = os.path.join(directory, "content.md")
        readme_filepath = os.path.join(directory, "README.md")

        user_content = ""
        if os.path.exists(readme_filepath):
            async with aiofiles.open(readme_filepath, 'r') as f:
                content = await f.read()
            user_content_match = re.search('###BEGIN_USER_GENERATED###.*###END_USER_GENERATED###', content, re.DOTALL)
            if user_content_match:
                user_content = user_content_match.group(0)

        toc_content = "## Table of Contents\n"
        file_content_list = []
        toc_set = set()  # Used to ensure no duplication in TOC

        for entry in os.scandir(directory):
            if entry.is_file() and not await should_ignore(entry.path, ignore_patterns):
                if entry.name not in toc_set:
                    toc_content += f"- [{entry.name}](#{entry.name})\n"
                    toc_set.add(entry.name)
                try:
                    async with aiofiles.open(entry.path, 'r', encoding='utf-8') as f:
                        file_content = await f.read()
                        if entry.name not in ["content.md", "README.md"] and file_content not in toc_content:
                            file_content_list.append(f"\n### {entry.name}\n{file_content}\n")
                except UnicodeDecodeError:
                    file_content_list.append(f"\n### {entry.name}\n**[ERROR reading {entry.name} as text. Might be a binary file or use a different encoding.]**\n")

        new_content = toc_content + "\n###BEGIN_AUTO_GENERATED###\n" + ''.join(file_content_list) + "###END_AUTO_GENERATED###\n"

        async with aiofiles.open(content_filepath, 'w') as f:
            await f.write(new_content)

        if os.path.exists(readme_filepath):
            async with aiofiles.open(readme_filepath, 'r') as f:
                existing_content = await f.read()
            content_start = existing_content.find("###BEGIN_AUTO_GENERATED###")
            content_end = existing_content.find("###END_AUTO_GENERATED###")
            if content_start != -1 and content_end != -1:
                existing_content = existing_content[:content_start] + new_content + existing_content[content_end + len("###END_AUTO_GENERATED###"):]
                new_content = existing_content

        async with aiofiles.open(readme_filepath, 'w') as f:
            await f.write(new_content)
            await f.write("\n" + user_content)

async def process_directory(directory):
    logging.info(f"Checking directory: {directory}")

    ignore_file_path = os.path.join(directory, "display_project_files.ignore")
    if os.path.exists(ignore_file_path):
        async with aiofiles.open(ignore_file_path, 'r') as f:
            ignore_patterns = compile_patterns([line.strip() for line in await f.readlines()])
        logging.info(f"Loaded ignore patterns for {directory}: {ignore_patterns}")
    else:
        ignore_patterns = compile_patterns(DEFAULT_IGNORE_PATTERNS)

    await generate_md_files(directory, ignore_patterns)

    for entry in os.scandir(directory):
        logging.info(f"Checking item against ignore patterns: {entry.path}")
        if entry.is_dir():
            await process_directory(entry.path)

if __name__ == "__main__":
    asyncio.run(process_directory("."))


### display_project_files.ignore
^./__pycache__
^.*?/\.git/
^.*?/\.git(/|$)
^.*?/\.env
.*\.json$
.*\.yml$

### requirements.txt
aiofiles==23.2.1
annotated-types==0.5.0
anyio==3.7.1
click==8.1.6
fastapi==0.101.1
gh==0.0.4
gitdb==4.0.10
GitPython==3.1.32
h11==0.14.0
idna==3.4
pydantic==2.1.1
pydantic_core==2.4.0
python-logstash==0.4.8
PyYAML==6.0.1
smmap==5.0.0
sniffio==1.3.0
starlette==0.27.0
typing_extensions==4.7.1
uvicorn==0.23.2


### .gitignore
# User added
**/.env*
# git_notes.md
**/.bk*

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# FastAPI specific
*.log
db.sqlite3

# IDEs and editors
# Intellij and PyCharm
.idea/
# VS Code
.vscode/

# OS
*.DS_Store  # macOS
*.swp  # Vim
*.swo  # Vim


# Ignore .env files everywhere
**/*.env

# Virtual environment
venv/
env/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

.git
**/^.git

### openapi_converter_main.py
# Filename is openapi_converter_main.py
# This file contains the main function to convert an OpenAPI 3.0 spec to 3.1

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


### openapi_converter.py
# Filename openapi_converter.py
# This module contains functions to convert an OpenAPI 3.0 spec to 3.1

import yaml
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.INFO)

def convert_openapi(openapi_dict):
    # Input validation

    validate_required_fields(openapi_dict)
    validate_openapi_version(openapi_dict, versions=["3.0.0", "3.1.0"])
    check_incompatible_inputs(openapi_dict, incompatible_keys=["securityDefinitions"])

    # Retain operation details

    for path in openapi_dict['paths'].values():
        for operation in path.values():
            if 'description' in operation:
                operation['x-original-description'] = operation['description']
            if 'operationId' in operation:
                operation['x-original-operationId'] = operation['operationId']

    # Retain schema details

    for schema in openapi_dict['components']['schemas'].values():
        if 'description' in schema:
            schema['x-original-description'] = schema['description']

    # Update to OpenAPI version 3.1.0

    openapi_dict['openapi'] = "3.1.0"

    # Security schemes

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

    # YAML conversion

    yaml_string = yaml.dump(openapi_dict, sort_keys=True)

    return yaml_string

# Input validation functions

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


### useful.git-commands-update-remote.py
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_current_branch():
    """Check the current git branch."""
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
    return result.stdout.strip()

def switch_branch(branch_name):
    """Switch to a specified git branch."""
    subprocess.run(['git', 'checkout', branch_name])
    logging.info(f"Switched to {branch_name} branch.")

def add_and_commit():
    """Add and commit changes."""
    subprocess.run(['git', 'add', '.'])
    commit_message = input("Enter your commit message: ")
    subprocess.run(['git', 'commit', '-m', commit_message])
    logging.info("Changes committed.")

def push_changes(branch_name):
    """Push changes to the specified branch."""
    subprocess.run(['git', 'push', 'origin', branch_name])
    logging.info(f"Pushed changes to {branch_name}.")

def main():
    if check_current_branch() != "development":
        logging.error("Not on 'development' branch. Please switch to 'development' branch to proceed.")
        return

    # Add and commit changes on development branch
    add_and_commit()
    push_changes('development')

    # Update production branch with changes from development
    switch_branch('production')
    subprocess.run(['git', 'merge', 'development'])
    push_changes('production')

    # Switch back to development branch
    switch_branch('development')

if __name__ == "__main__":
    main()


### useful.git-create-new-repo.py
import os
import logging
import subprocess

import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("script.log"), logging.StreamHandler()])


def initialize_and_setup_repo(directory):
    
    # Set the absolute path for the directory
    directory_path = os.path.abspath(directory)
    print(f"directory_path: {directory_path}")

    # Get the name of the current directory to use as the repository name.
    repo_name = os.path.basename(directory_path)
    print(f"repo_name: {repo_name}")

    # Check if the directory already has a Git repo.
    if os.path.isdir(os.path.join(directory_path, ".git")):
        logging.info("Directory already has a git repo")
        return

    # Create a new GitHub repository with the current directory name.
    subprocess.run(["gh", "repo", "create", repo_name, "--private", "-y"])
    logging.info(f"GitHub repository '{repo_name}' created successfully!")

    # Initialize a new Git repo.
    subprocess.run(["git", "init", "--quiet"])

    # Add all of the files to the repo.
    subprocess.run(["git", "add", "*"])

    # Commit the changes to the repo.
    subprocess.run(["git", "commit", "-m", "Initial commit on main branch"])

    # Add the remote origin.
    remote_url = f"https://github.com/inayet/{repo_name}.git"
    print(f"remote_url: {remote_url}")
    subprocess.run(["git", "remote", "add", "origin", remote_url])

    # Push the main branch to the new GitHub repository.
    subprocess.run(["git", "push", "-u", "origin", "main"])

    # Create the 'production' branch, commit, and push
    subprocess.run(["git", "checkout", "-b", "production"])
    subprocess.run(["git", "push", "-u", "origin", "production"])
    logging.info("Created and pushed 'production' branch.")

    # Switch back to main to create the 'development' branch, commit, and push
    subprocess.run(["git", "checkout", "main"])
    subprocess.run(["git", "checkout", "-b", "development"])
    subprocess.run(["git", "push", "-u", "origin", "development"])
    logging.info("Created and pushed 'development' branch.")

    # Log the success message.
    logging.info("Repo setup complete!")

if __name__ == "__main__":
    initialize_and_setup_repo(".")


### License
MIT License

Copyright (c) 2023 Bard

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
###END_AUTO_GENERATED###
