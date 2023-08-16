## Table of Contents
- [display_content_readme.py](#display_content_readme.py)
- [requirements.txt](#requirements.txt)
- [dir-structure](#dir-structure)
- [openapi_converter_main.py](#openapi_converter_main.py)
- [content.md](#content.md)
- [openapi_converter.py](#openapi_converter.py)
- [README.md](#README.md)
- [License](#License)

## Table of Contents
- [display_content_readme.py](#display_content_readme.py)
- [requirements.txt](#requirements.txt)
- [dir-structure](#dir-structure)
- [openapi_converter_main.py](#openapi_converter_main.py)
- [content.md](#content.md)
- [openapi_converter.py](#openapi_converter.py)
- [README.md](#README.md)
- [License](#License)

###BEGIN_AUTO_GENERATED###

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


### requirements.txt
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
aiofiles

### dir-structure
.
├── dir-structure
├── License
├── openapi_converter_main.py
├── openapi_converter.py
├── README.md
├── requirements.txt
├── useful.git-commands
├── useful.git-create-new-repo.py
└── useful.git-create-new-repo.sh

1 directory, 9 files


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

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' does not exist.")

    with open(args.input_file, 'r') as f:
        openapi_dict = yaml.safe_load

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
\n"

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


### requirements.txt
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
aiofiles

### dir-structure
.
├── dir-structure
├── License
├── openapi_converter_main.py
├── openapi_converter.py
├── README.md
├── requirements.txt
├── useful.git-commands
├── useful.git-create-new-repo.py
└── useful.git-create-new-repo.sh

1 directory, 9 files


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

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' does not exist.")

    with open(args.input_file, 'r') as f:
        openapi_dict = yaml.safe_load

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

###BEGIN_USER_GENERATED###

# OpenAPI converter app

The OpenAPI converter app converts an OpenAPI 3.0 spec to 3.1.

## Usage

To use the app, you need to provide two command-line arguments:

- The path to the input file
- The path to the output file

The input file must be a valid OpenAPI 3.0 spec. The output file will contain the converted OpenAPI 3.1 spec.

For example, to convert the OpenAPI 3.0 spec in the file `input.yaml` to OpenAPI 3.1 and save the output to the file `output.yaml`, you would use the following command:

#

```bash
openapi_converter.py input.yaml output.yaml
```

## Output

The output file will contain the following information:

- The OpenAPI version (3.1.0)
- The info object, including the title, description, version, and contact information
- The paths object, which maps paths to operations
- The components object, which contains the schemas and security schemes

## Reference guide

The following is a reference guide for the API of the OpenAPI converter app:

- `convert_openapi(openapi_dict)`: This function converts an OpenAPI 3.0 spec to 3.1. The `openapi_dict` parameter is a dictionary that contains the OpenAPI spec.
- `validate_required_fields(openapi_dict)`: This function validates that the `openapi_dict` parameter contains all of the required fields for an OpenAPI spec.
- `validate_openapi_version(openapi_dict, versions)`: This function validates that the `openapi_dict` parameter has the correct OpenAPI version. The `versions` parameter is a list of valid OpenAPI versions.
- `check_incompatible_inputs(openapi_dict, incompatible_keys)`: This function checks for deprecated keys in the `openapi_dict` parameter. The `incompatible_keys` parameter is a list of deprecated keys.

## Troubleshooting guide

If you encounter any problems using the OpenAPI converter app, you can try the following troubleshooting steps:

1. Make sure that the input file is a valid OpenAPI 3.0 spec.
2. Make sure that the output file does not already exist.
3. Try running the app with the `-v` flag to enable verbose logging. This will help you to diagnose the problem.
4. If you are still having problems, you can open an issue on the GitHub repository for the app.

###END_USER_GENERATED###
###BEGIN_USER_GENERATED###.*###END_USER_GENERATED###', content, re.DOTALL)
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


### requirements.txt
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
aiofiles

### dir-structure
.
├── dir-structure
├── License
├── openapi_converter_main.py
├── openapi_converter.py
├── README.md
├── requirements.txt
├── useful.git-commands
├── useful.git-create-new-repo.py
└── useful.git-create-new-repo.sh

1 directory, 9 files


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

    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Input file '{args.input_file}' does not exist.")

    with open(args.input_file, 'r') as f:
        openapi_dict = yaml.safe_load

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

###BEGIN_USER_GENERATED###

# OpenAPI converter app

The OpenAPI converter app converts an OpenAPI 3.0 spec to 3.1.

## Usage

To use the app, you need to provide two command-line arguments:

- The path to the input file
- The path to the output file

The input file must be a valid OpenAPI 3.0 spec. The output file will contain the converted OpenAPI 3.1 spec.

For example, to convert the OpenAPI 3.0 spec in the file `input.yaml` to OpenAPI 3.1 and save the output to the file `output.yaml`, you would use the following command:

#

```bash
openapi_converter.py input.yaml output.yaml
```

## Output

The output file will contain the following information:

- The OpenAPI version (3.1.0)
- The info object, including the title, description, version, and contact information
- The paths object, which maps paths to operations
- The components object, which contains the schemas and security schemes

## Reference guide

The following is a reference guide for the API of the OpenAPI converter app:

- `convert_openapi(openapi_dict)`: This function converts an OpenAPI 3.0 spec to 3.1. The `openapi_dict` parameter is a dictionary that contains the OpenAPI spec.
- `validate_required_fields(openapi_dict)`: This function validates that the `openapi_dict` parameter contains all of the required fields for an OpenAPI spec.
- `validate_openapi_version(openapi_dict, versions)`: This function validates that the `openapi_dict` parameter has the correct OpenAPI version. The `versions` parameter is a list of valid OpenAPI versions.
- `check_incompatible_inputs(openapi_dict, incompatible_keys)`: This function checks for deprecated keys in the `openapi_dict` parameter. The `incompatible_keys` parameter is a list of deprecated keys.

## Troubleshooting guide

If you encounter any problems using the OpenAPI converter app, you can try the following troubleshooting steps:

1. Make sure that the input file is a valid OpenAPI 3.0 spec.
2. Make sure that the output file does not already exist.
3. Try running the app with the `-v` flag to enable verbose logging. This will help you to diagnose the problem.
4. If you are still having problems, you can open an issue on the GitHub repository for the app.

###END_USER_GENERATED###