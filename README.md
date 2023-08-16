# Convert OpenAPI 3.0.0 to OpenAPI 3.1.0 Converter

> ![OpenAPI](assets/openapi310.png)

## Table of Contents

- [Description](#description)
- [How to Use](#how-to-use)
- [Scripts](#scripts)
- [Configuration Files](#configuration-files)
- [Documentation](#documentation)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Description

Welcome to the **OpenAPI 3.0.0 to OpenAPI 3.1.0 Converter** repository. This collection of tools and scripts is designed to seamlessly convert OpenAPI 3.0.0 specifications to the upgraded OpenAPI 3.1.0 format.

## How to Use

To efficiently convert your OpenAPI 3.0.0 specifications to OpenAPI 3.1.0 format, follow these steps:

### 1. `openapi_converter_main.py`

This script is the heart of the conversion process. It takes an OpenAPI 3.0.0 specification in JSON format and generates a 3.1.0 YAML specification.

Usage:

```bash
python openapi_converter_main.py [input_file.json] [output_file.yml]
```

### 2. `useful.git-create-new-repo.py`

![GitHub](https://www.vectorlogo.zone/logos/github/github-ar21.svg)

Need a new GitHub repository? This script not only initializes a repository but also sets up main, production, and development branches for your project.

Usage:

```bash
python useful.git-create-new-repo.py
```

### 3. `useful.git-update-production-main.py`

Keep your production and main branches up to date with this script.

Usage:

```bash
python useful.git-update-production-main.py
```

### 4. `useful.git-update-development-production.py`

Update your development and production branches efficiently.

Usage:

```bash
python useful.git-update-development-production.py
```

### 5. `md_content_aggregator.py`

Asynchronously scan your directory to generate a content markdown file based on the files present.

Usage:

```bash
python md_content_aggregator.py
```

## Configuration Files

### `display_project_files.ignore`

This file contains patterns of files and directories to ignore when generating documentation using the `md_content_aggregator.py` script.

### `.gitignore`

This file specifies patterns of files and directories to be ignored by Git. It helps maintain a clean repository by excluding unnecessary files and build artifacts.

### `requirements.txt`

This file lists the necessary Python packages required to run the scripts in this repository.

## Documentation

### `CODE_OF_CONDUCT.md`

This document outlines the code of conduct for contributors and users of the repository, ensuring a respectful and inclusive environment for collaboration.

### `SECURITY.md`

This document details the security policy for the repository. Learn how to report vulnerabilities and understand our commitment to promptly addressing security concerns.

## Dependencies

Install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License. View the [License](LICENSE) file in the repository for more details.


This layout presents the information in a clear and structured manner, making it easier for readers to understand the purpose of the repository and how to use its contents. Feel free to modify this further to align with your preferences or to include any additional details.

## Future Plans

As we continually strive to enhance and streamline the OpenAPI conversion process, we have some exciting developments on the horizon:

### 1. Automating OpenAPI Spec Retrieval

Our upcoming feature aims to simplify the acquisition of OpenAPI specifications. We're working on an automated mechanism to fetch specs directly from websites and API endpoints. This eliminates manual downloading, providing real-time access to the most current information.

### 2. Automated Conversion and External Validation

Our focus extends beyond conversion alone. We're in the process of creating an automated pipeline that not only converts OpenAPI 3.0.0 specs to 3.1.0 but also employs external tools to validate the converted files.

### 3. Enhancing Quality with OpenAPI API Validator

In our pursuit of accurate and compliant OpenAPI specifications, we're thrilled to integrate the OpenAPI API Validator into our conversion process. This powerful validator ensures the quality, accuracy, and compliance of your converted OpenAPI specs.

By incorporating the OpenAPI API Validator, we're taking proactive steps to eliminate errors and inconsistencies from your converted specifications. This tool empowers a seamless transition from OpenAPI 3.0.0 to 3.1.0 while maintaining the highest accuracy standards.

### Join Us 
We invite you to join us on this journey towards excellence. Your feedback, ideas, and suggestions are invaluable as we enhance your OpenAPI conversion experience. Share your thoughts in the Issues section, and stay tuned for updates as we roll out these exciting features to elevate your OpenAPI conversion workflows!