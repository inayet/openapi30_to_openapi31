# Filename: useful.git-create-new-repo.py
# This script helps create a new Git repository

import os
import logging
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("script.log"), logging.StreamHandler()])

def initialize_and_setup_repo():
    # Set the absolute path for the current directory
    directory_path = os.path.abspath('.')
    logging.info(f"Directory path: {directory_path}")
    
    # Get the last part of the directory path
    repo_name = os.path.basename(directory_path)
    logging.info(f"Repo name: {repo_name}")

    # Check if the directory already has a Git repo
    if os.path.isdir(os.path.join(directory_path, ".git")):
        logging.info("Directory already has a git repo")
        return

    # Create a new GitHub repository with the current directory name
    subprocess.run(["gh", "repo", "create", repo_name, "--private", "-y"])
    logging.info(f"GitHub repository '{repo_name}' created successfully!")

    # Initialize a new Git repo
    subprocess.run(["git", "init", "--quiet"])

    # Add all of the files to the repo
    subprocess.run(["git", "add", "*"])

    # Commit the changes to the repo
    subprocess.run(["git", "commit", "-m", "Initial commit on main branch"])

    # Add the remote origin
    remote_url = f"https://github.com/inayet/{repo_name}.git"
    subprocess.run(["git", "remote", "add", "origin", remote_url])

    # Push the main branch to the new GitHub repository
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

    # Log the success message
    logging.info("Repo setup complete!")

if __name__ == "__main__":
    initialize_and_setup_repo()
