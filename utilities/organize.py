import os
import shutil

def reorganize_files():
    # Create new directories if they don't exist
    new_directories = ["src", "data", "docs", "utilities"]
    for directory in new_directories:
        if not os.path.exists(directory):
            os.mkdir(directory)
    
    # Move main code to src
    src_files = ["__init__.py", "md_content_aggregator.py", "openapi_converter_main.py", "openapi_converter.py"]
    for file in src_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("src", file))
    
    # Move data-related files to data
    data_files = ["calendars.json", "calendars.yml"]
    for file in data_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("data", file))
    
    # Move markdown documentation to docs
    docs_files = ["CODE_OF_CONDUCT.md", "SECURITY.md", "content.md"]
    for file in docs_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("docs", file))
    
    # Move utility scripts to utilities
    utility_files = ["organize.py"]
    for file in utility_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("utilities", file))

    # Handle assets, git-utils, and configuration as before
    assets_files = ["openapi310.png"]
    for file in assets_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("assets", file))
    
    git_utils_files = ["useful.git-commands", "useful.git-create-new-repo.py", 
                       "useful.git-update-development-production.py", 
                       "useful.git-update-production-main.py"]
    for file in git_utils_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("git-utils", file))
    
    config_files = ["display_project_files.ignore"]
    for file in config_files:
        if os.path.exists(file):
            shutil.move(file, os.path.join("configuration", file))

if __name__ == '__main__':
    reorganize_files()
