### README.md

# Convert OpenAPI 3.0.0 specs to OpenAPI 3.1.0

> ![OpenAPI](assets/openapi310.png)

## Table of Contents
- [Description](#description)
- [How to Use](#how-to-use)
- [Dependencies](#dependencies)
- [License](#license)

## Description

This repository contains scripts and tools to convert OpenAPI 3.0.0 specifications to OpenAPI 3.1.0.

## How to Use

### 1. openapi_converter_main.py

Converts an OpenAPI 3.0.0 specification saved in json  and outputs 3.1.0 yml spec format: 

Usage:

```bash
python openapi_converter_main.py [input_file.json] [output_file.yml]
```

### 2. openapi_converter.py

Contains functions that assist `openapi_converter_main.py` in converting OpenAPI 3.0 to 3.1.

### 3. useful.git-create-new-repo.py

![GitHub](https://www.vectorlogo.zone/logos/github/github-ar21.svg)

Initializes a new GitHub repository and sets up the main, production, and development branches.

Usage:

```bash
python useful.git-create-new-repo.py
```

### 4. useful.git-update-production-main.py

Updates the production and main branches.

Usage:

```bash
python useful.git-update-production-main.py
```

### 5. useful.git-update-development-production.py

Updates the development and production branches.

Usage:

```bash
python useful.git-update-development-production.py
```

### 6. display_content_readme.py

Asynchronously scans the directory to generate a content markdown file based on the files in the directory.

Usage:

```bash
python display_content_readme.py
```

## Dependencies

Install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## License

This project is under the MIT License. See the `License` file in the repository for more details.