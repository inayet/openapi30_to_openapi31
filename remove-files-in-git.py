import os

# Starting directory (change this to the directory containing `.git`)
start_directory = ".git"

# Walk through every directory and sub-directory
for dirpath, dirnames, filenames in os.walk(start_directory):
    # If 'content.md' exists in the directory, delete it
    if 'content.md' in filenames:
        content_md_path = os.path.join(dirpath, 'content.md')
        os.remove(content_md_path)
        print(f"Deleted: {content_md_path}")
    
    # If 'README.md' exists in the directory, delete it
    if 'README.md' in filenames:
        readme_md_path = os.path.join(dirpath, 'README.md')
        os.remove(readme_md_path)
        print(f"Deleted: {readme_md_path}")

print("Finished checking and deleting files.")
