## Table of Contents
- [script.log](#script-log)
- [useful.git-commands](#useful-git-commands)
- [display_project_files.ignore](#display_project_files-ignore)
- [requirements.txt](#requirements-txt)
- [.gitignore](#-gitignore)
- [__init__.py](#__init__-py)
- [CODE_OF_CONDUCT.md](#CODE_OF_CONDUCT-md)
- [openapi_converter_main.py](#openapi_converter_main-py)
- [useful.git-update-production-main.py](#useful-git-update-production-main-py)
- [openapi_converter.py](#openapi_converter-py)
- [useful.git-create-new-repo.py](#useful-git-create-new-repo-py)
- [useful.git-update-development-production.py](#useful-git-update-development-production-py)
- [README.md](#README-md)
- [md_content_aggregator.py](#md_content_aggregator-py)
- [SECURITY.md](#SECURITY-md)
- [License](#License)


### script.log
```
2023-08-16 11:05:19,178 - INFO - Directory already has a git repo
2023-08-16 11:51:30,438 - INFO - Directory already has a git repo

```

### useful.git-commands
```
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
```

### display_project_files.ignore
```
^./__pycache__
^.*?/\.git/
^.*?/\.git(/|$)
^.*?/\.env
.*\.json$
.*\.yml$
```

### requirements.txt
```
aiofiles==23.2.1
annotated-types==0.5.0
anyio==3.7.1
click==8.1.6
fastapi==0.101.1
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

```

### .gitignore
```
# User added
**/.env*
# git_notes.md
**/.bk*

# Byte-compiled / optimized / DLL files
__pycache__/
./__pycache__/
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
```

### __init__.py
```

```

### CODE_OF_CONDUCT.md
```
# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity
and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
  overall community

Examples of unacceptable behavior include:

* The use of sexualized language or imagery, and sexual attention or
  advances of any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
  address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at
inayet@dreamsapi.com.
All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Enforcement Guidelines

Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:

### 1. Correction

**Community Impact**: Use of inappropriate language or other behavior deemed
unprofessional or unwelcome in the community.

**Consequence**: A private, written warning from community leaders, providing
clarity around the nature of the violation and an explanation of why the
behavior was inappropriate. A public apology may be requested.

### 2. Warning

**Community Impact**: A violation through a single incident or series
of actions.

**Consequence**: A warning with consequences for continued behavior. No
interaction with the people involved, including unsolicited interaction with
those enforcing the Code of Conduct, for a specified period of time. This
includes avoiding interactions in community spaces as well as external channels
like social media. Violating these terms may lead to a temporary or
permanent ban.

### 3. Temporary Ban

**Community Impact**: A serious violation of community standards, including
sustained inappropriate behavior.

**Consequence**: A temporary ban from any sort of interaction or public
communication with the community for a specified period of time. No public or
private interaction with the people involved, including unsolicited interaction
with those enforcing the Code of Conduct, is allowed during this period.
Violating these terms may lead to a permanent ban.

### 4. Permanent Ban

**Community Impact**: Demonstrating a pattern of violation of community
standards, including sustained inappropriate behavior,  harassment of an
individual, or aggression toward or disparagement of classes of individuals.

**Consequence**: A permanent ban from any sort of public interaction within
the community.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.0, available at
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html.

Community Impact Guidelines were inspired by [Mozilla's code of conduct
enforcement ladder](https://github.com/mozilla/diversity).

[homepage]: https://www.contributor-covenant.org

For answers to common questions about this code of conduct, see the FAQ at
https://www.contributor-covenant.org/faq. Translations are available at
https://www.contributor-covenant.org/translations.
```

### openapi_converter_main.py
```
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

```

### useful.git-update-production-main.py
```
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

def merge_and_push(source_branch, target_branch):
    """Merge the source branch into the target branch and push the changes."""
    # Switch to the target branch
    switch_branch(target_branch)
    
    # Merge the source branch into the target branch
    merge_result = subprocess.run(['git', 'merge', source_branch], capture_output=True, text=True)
    if merge_result.returncode != 0:
        logging.error(f"Failed to merge {source_branch} into {target_branch}. Resolve conflicts manually.")
        return

    logging.info(f"Merged {source_branch} into {target_branch}.")
    
    # Push changes to the target branch
    push_changes(target_branch)

def push_changes(branch_name):
    """Push changes to the specified branch."""
    subprocess.run(['git', 'push', 'origin', branch_name])
    logging.info(f"Pushed changes to {branch_name}.")

def main():
    initial_branch = check_current_branch()
    if initial_branch != "main":
        logging.warning(f"Currently on '{initial_branch}'. Switching to 'main' branch to proceed with the merge.")
    
    # Push updates from local 'production' branch to remote 'production' branch
    switch_branch('production')
    push_changes('production')
    
    # Merge the 'production' branch into the 'main' branch and push the changes
    merge_and_push('production', 'main')
    
    # Switch back to the initial branch
    switch_branch(initial_branch)
    logging.info(f"Switched back to the initial branch: '{initial_branch}'")

if __name__ == "__main__":
    main()

```

### openapi_converter.py
```
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

```

### useful.git-create-new-repo.py
```
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

```

### useful.git-update-development-production.py
```
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

```

### md_content_aggregator.py
```
import os
import re
import asyncio
import aiofiles
import logging
import json

logging.basicConfig(level=logging.INFO)

DEFAULT_IGNORE_PATTERNS = [r"\./__pycache__", r".*\.git.*", r".*\.env.*", r"README\.md"]
CONCURRENT_TASKS_LIMIT = 4
sem = asyncio.Semaphore(CONCURRENT_TASKS_LIMIT)

def compile_patterns(patterns):
    """Compile regex patterns."""
    return [re.compile(pattern) for pattern in patterns]

async def should_ignore(item, compiled_patterns):
    """Check if the item should be ignored based on patterns."""
    for pattern in compiled_patterns:
        if pattern.search(item):
            logging.info(f"Ignoring item due to pattern {pattern.pattern}: {item}")
            return True
    logging.info(f"Item not ignored: {item}")
    return False

added_content = set()

async def generate_md_files(directory, ignore_patterns):
    """Generate markdown files for a directory."""
    logging.info(f"Processing directory: {directory}")
    async with sem:
        content_filepath = os.path.join(directory, "content.md")
        readme_filepath = os.path.join(directory, "README.md")

        user_content = ""
        # Commented out code related to README.md
        '''
        if os.path.exists(readme_filepath):
            async with aiofiles.open(readme_filepath, 'r') as f:
                content = await f.read()
            user_content_match = re.search('###BEGIN_USER_GENERATED###.*###END_USER_GENERATED###', content, re.DOTALL)
            if user_content_match:
                user_content = user_content_match.group(0)
        '''

        toc_content = "## Table of Contents\n"
        file_content_list = []
        toc_set = set()

        for entry in os.scandir(directory):
            if entry.is_file() and not await should_ignore(entry.path, ignore_patterns):
                if entry.name.endswith(".json"):
                    try:
                        json_content = json.loads(file_content)
                        formatted_json = json.dumps(json_content, indent=4)
                        file_content_list.append(f"\n### {entry.name}\n```json\n{formatted_json}\n```\n")
                    except json.JSONDecodeError:
                        file_content_list.append(f"\n### {entry.name}\n**[ERROR reading {entry.name} as JSON.]**\n")
                else:
                    if entry.name not in toc_set:
                        toc_content += f"- [{entry.name}](#{entry.name.replace('.', '-')})\n"
                        toc_set.add(entry.name)
                    try:
                        async with aiofiles.open(entry.path, 'r', encoding='utf-8') as f:
                            file_content = await f.read()
                            if file_content not in added_content:
                                if entry.name not in ["content.md", "README.md"]:
                                    file_content_list.append(f"\n### {entry.name}\n```\n{file_content}\n```\n")
                                    added_content.add(file_content)
                    except UnicodeDecodeError:
                        file_content_list.append(f"\n### {entry.name}\n**[ERROR reading {entry.name} as text. Might be a binary file or use a different encoding.]**\n")

        new_content = toc_content + "\n" + ''.join(file_content_list)

        async with aiofiles.open(content_filepath, 'w') as f:
            await f.write(new_content)

async def process_directory(directory):
    """Recursively process directories."""
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
        if entry.is_dir():
            await process_directory(entry.path)

if __name__ == "__main__":
    asyncio.run(process_directory("."))

```

### SECURITY.md
```
### SECURITY.md

```markdown
# Security Policy

![Security](https://www.vectorlogo.zone/logos/snykio/snykio-ar21.svg)

## Supported Versions

Currently, we support the following versions of "Convert OpenAPI 3.0.0 specs to OpenAPI 3.1.0" with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

If you discover any vulnerabilities or security issues, kindly follow these steps:

1. **Avoid Creating Public Issues**: Please do not discuss vulnerabilities in public to prevent malicious use.
2. **Contact Us Directly**: Send a detailed vulnerability report to [inayet@dreamsapi.com](mailto:inayet@dreamsapi.com).
3. **Response Time**: We prioritize our users' security and will address the report as soon as possible, typically within 48 hours. You'll receive an update on the reported vulnerability, and we'll work together to address the concern.

```
```

### License
```
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
```
