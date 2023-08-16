# Convert OpenAPI 3.0.0 specs to OpenAPI 3.1.0

Welcome to the Dreams API OpenAPI conversion toolkit! This tool is specifically designed to convert OpenAPI 3.0.0 specifications to OpenAPI 3.1.0, helping developers ensure their API documentation remains up-to-date with the latest standards. Please fork this project and make it better for yourself and everyone else


> **OpenAPI 3.1.0**:  <img src="assets/openapi310.png" lenght="85" alt="OpenAPI 3.1.0 Logo">

## 📌 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact & Support](#contact--support)

## 📥 Installation

To get started with the toolkit:

1. Clone the repository:
   ```bash
   git clone https://github.com/inayet/openapi30_to_openapi31.git
   ```
2. Navigate to the project directory:
   ```bash
   cd openapi30_to_openapi31
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

To convert an OpenAPI spec:

1. Navigate to the project directory.
2. Run the main conversion script:
   ```bash
   python openapi_converter_main.py <input_file> <output_file>
   ```
   - `<input_file>`: The path to your OpenAPI 3.0.0 specification.
   - `<output_file>`: The desired path for your converted OpenAPI 3.1.0 specification. 

**Example**:
```bash
python openapi_converter_main.py example_old_spec.yml example_new_spec.yml
```

## 🏗 Project Structure

- **OpenAPI Tools**:
  - `openapi_converter_main.py`: The main script to initiate the conversion.
  - `openapi_converter.py`: Contains functions to handle the conversion process.
- **Git Automation**:
  - `useful.git-commands`: A list of handy Git commands.
  - `useful.git-update-remote.py`: A Python script for Git remote updates.
  - `useful.git-create-new-repo.py`: A Python script to initialize and set up a new repo.

## ✍️ Contributing

Contributions are always welcome! Here's how you can help:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/YourNewFeature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/YourNewFeature`
5. Submit a pull request.

## 📜 License

This project is licensed under the MIT License. See the [License](./License) file for details.

## 📞 Contact & Support

For inquiries, issues, or feedback, please raise an issue in the [repository](https://github.com/inayet/openapi30_to_openapi31/issues) or contact us directly at `inayet@dreamsapi.com`.