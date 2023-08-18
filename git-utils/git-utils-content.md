## Table of Contents
- [useful.git-update-all-branches.py](#useful-git-update-all-branches-py)
- [useful.git-create-new-repo.py](#useful-git-create-new-repo-py)


## Directory Structure
```json
[
  {"type":"directory","name":"./git-utils","contents":[
    {"type":"file","name":"useful.git-create-new-repo.py"},
    {"type":"file","name":"useful.git-update-all-branches.py"}
  ]}
,
  {"type":"report","directories":1,"files":2}
]

```


### useful.git-update-all-branches.py
```python
"""
Git Branch Update Utility

Methods:
- log_to_db: Log actions to SQLite database
- backup_database: Back up SQLite database  
- stash_changes: Stash local changes
- pop_changes: Pop stashed changes
- check_for_merge_conflicts: Check and handle merge conflicts
- handle_pull_failure: Handle pull failures
- merge_and_push: Merge source into target branch and push
- fetch_all_remote_branches: Fetch all remote branches
- ensure_correct_branch_for_action: Ensure user is on correct branch
- update_branches: Update target branches with source changes
- update_branch_with_source: Update target branch with source changes 
- get_all_branches: Get all branches in the repo
- get_all_local_branches: Get all local branches in the repo
- select_source_branch: Select source branch interactively
- select_target_branches: Select target branches interactively
- main: Main function

This script provides functionalities to:
1. Dynamically list all branches in the repository.
2. Allow users to select a source branch and multiple target branches.
3. Update the target branches with the latest changes from the source branch.  
4. Ensure users are on the correct branch before proceeding with updates.
5. Handle merge conflicts and allow users to decide how to proceed.
6. Log all actions to an SQLite database. 
7. Backup the SQLite database.
8. Fetch all remote branches to ensure the local repository is up-to-date.
"""

import os
import logging
import subprocess
import sqlite3
import shutil

DATABASE_NAME = "git_actions_log.db"

\# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("script.log"), logging.StreamHandler()])

def log_to_db(action, message):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS actions
                          (timestamp TEXT, action TEXT, message TEXT)''')
        cursor.execute("INSERT INTO actions (timestamp, action, message) VALUES (datetime('now'), ?, ?)",
                       (action, message))
        conn.commit()

def backup_database():
    backup_name = DATABASE_NAME.split('.')[0] + "_backup.db"
    shutil.copy(DATABASE_NAME, backup_name)
    logging.info(f"Backed up database to {backup_name}.")
    log_to_db("INFO", f"Backed up database to {backup_name}.")

def stash_changes():
    subprocess.run(["git", "stash", "push", "-m", "changes_stash_for_script"])

def pop_changes():
    stashes = subprocess.getoutput("git stash list")
    if "changes_stash_for_script" in stashes:
        subprocess.run(["git", "stash", "pop"])

def check_for_merge_conflicts():
    status = subprocess.getoutput("git status")
    if "You have unmerged paths" in status or "fix conflicts" in status:
        logging.error("You have unresolved merge conflicts.")
        print("1: Resolve conflicts manually and exit script.")
        print("2: Prioritize local changes.")
        print("3: Prioritize remote changes.")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            print("Resolve the conflicts manually and then run the script again.")
            exit(1)
        elif choice == '2':
            subprocess.run(["git", "checkout", "--", "."])
        elif choice == '3':
            current_branch = subprocess.getoutput("git branch --show-current")
            subprocess.run(["git", "reset", "--hard", f"origin/{current_branch}"])
        else:
            logging.warning("Invalid choice. Exiting.")
            exit(1)

def handle_pull_failure(branch_name):
    logging.error(f"Failed to pull from {branch_name}")
    user_decision = input(f"Failed to pull from {branch_name}. Do you want to proceed? (yes/no): ")
    if user_decision.lower() != 'yes':
        return False

    priority_decision = input("Which files do you want to prioritize? (local/remote): ")
    if priority_decision.lower() == 'local':
        subprocess.run(["git", "checkout", "--", "."])
    elif priority_decision.lower() == 'remote':
        subprocess.run(["git", "reset", "--hard", f"origin/{branch_name}"])
    return True

def merge_and_push(source_branch, target_branch):
    merge_result = subprocess.run(["git", "merge", source_branch, "--no-ff",
                                  "-m", f"Merging changes from {source_branch} into {target_branch}"], capture_output=True, text=True)
    if merge_result.returncode != 0:
        error_msg = f"Failed to merge {source_branch} into {target_branch}. Resolve conflicts manually."
        logging.error(error_msg + "\n" + merge_result.stderr)
        return

    push_result = subprocess.run(["git", "push", "origin", target_branch], capture_output=True, text=True)
    if push_result.returncode != 0:
        error_msg = f"Failed to push changes to {target_branch}."
        logging.error(error_msg + "\n" + push_result.stderr)
        return

    success_msg = f"Merged '{source_branch}' into '{target_branch}' and pushed changes."
    logging.info(success_msg)

def fetch_all_remote_branches():
    result = subprocess.run(["git", "fetch", "--all"], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("Failed to fetch remote branches. Please check your internet connection.")
        exit(1)
    else:
        logging.info("Successfully fetched all remote branches.")

def ensure_correct_branch_for_action(source_branch):
    current_branch = subprocess.getoutput("git branch --show-current")
    if current_branch.replace('*', '').strip() != source_branch.replace('*', '').strip():
        switch = input(f"You must be on the '{source_branch}' branch to update other branches. Switch to '{source_branch}'? (yes/no): ")
        if switch.lower() == 'yes':
            subprocess.run(["git", "checkout", source_branch])
            check_for_merge_conflicts()
        else:
            logging.warning("Operation cancelled by user.")
            exit(1)


def update_branches(source_branch, target_branches):
    """Update target branches with source changes."""
    print(f"Will merge changes from '{source_branch}' into the following branches: {', '.join(target_branches)}")
    confirmation = input("Do you want to proceed? (yes/no): ")
    if confirmation.lower() != 'yes':
        logging.info("Operation cancelled by user.")
        return

    check_for_merge_conflicts()
    stash_changes()

    for target_branch in target_branches:
        if target_branch == source_branch:
            logging.info(f"Skipping {source_branch} as it's the same as the source branch.")
            continue

        subprocess.run(["git", "checkout", target_branch])
        if not update_branch_with_source(target_branch, source_branch):
            logging.error(f"Failed to update {target_branch} with changes from {source_branch}")
            continue

    subprocess.run(["git", "checkout", source_branch])
    pop_changes()

def update_branch_with_source(target_branch, source_branch):
    pull_result = subprocess.run(["git", "pull", "origin", source_branch], capture_output=True, text=True)
    if pull_result.returncode != 0:
        logging.error(f"Failed to pull latest code from {source_branch}.")
        return False

    subprocess.run(["git", "checkout", target_branch])
    pull_target_result = subprocess.run(["git", "pull", "origin", target_branch], capture_output=True, text=True)
    if pull_target_result.returncode != 0 and not handle_pull_failure(target_branch):
        return False

    merge_and_push(source_branch, target_branch)
    return True

def get_all_branches():
    branches = subprocess.getoutput("git branch -a")
    return [branch.strip() for branch in branches.split('\n')]

def get_all_local_branches():
    branches = subprocess.getoutput("git branch")
    return [branch.strip() for branch in branches.split('\n')]

def clean_branch_name(branch):
    """Standardize and clean the branch name."""
    return branch.replace('*', '').strip().split('/')[-1]

def select_source_branch():
    """Select source branch interactively."""
    print("Select the source branch:")
    all_branches = get_all_branches()
    for idx, branch in enumerate(all_branches, start=1):
        print(f"{idx}: {branch}")

    choice = int(input(f"Enter choice (1 to {len(all_branches)}): "))
    if choice < 1 or choice > len(all_branches):
        logging.error("Invalid choice.")
        exit(2)

    source_branch = clean_branch_name(all_branches[choice - 1])
    return source_branch

def select_target_branches():
    """Select target branches interactively."""
    print("Select the target branches:")
    
    all_local_branches = get_all_local_branches()
    for idx, branch in enumerate(all_local_branches, start=1):
        print(f"{idx}: {branch}")

    choices = list(map(int, input("Enter choices (comma separated): ").split(',')))
    target_branches = [all_local_branches[choice - 1].replace('*', '').strip() for choice in choices]
    return target_branches



def handle_unstaged_changes():
    """Handle any unstaged changes in the repo."""
    status = subprocess.getoutput("git status")
    if "Changes not staged for commit:" in status:
        print("\nThere are some unstaged changes in your repository. Here's what changed:\n")
        os.system("git diff")
        
        \# Extract filenames here, outside of the choice blocks.
        filenames = [line.split(":")[1].strip() for line in status.split("\n") if "modified:" in line]

        print("\nOptions:")
        print("1: Stage and commit the changes.")
        print("2: Discard the changes.")
        print("3: Exit and handle the changes manually.")
        
        choice = input("\nEnter your choice (1/2/3): ")
        
        if choice == '1':
            for filename in filenames:
                subprocess.run(["git", "add", filename])
            commit_message = input("Enter commit message: ")
            subprocess.run(["git", "commit", "-m", commit_message])
            print("Changes have been staged and committed.")
        
        elif choice == '2':
            for filename in filenames:
                subprocess.run(["git", "checkout", "--", filename])
            print("Changes have been discarded.")
        
        elif choice == '3':
            print("Exiting. You can handle the changes manually.")
            exit(1)



def main():
    logging.info("Git Branch Update Utility")
    
    fetch_all_remote_branches()
    backup_database()
    
    source_branch = select_source_branch()
    ensure_correct_branch_for_action(source_branch)
    
    target_branches = select_target_branches()
    confirm = input(f"Will merge changes from '{source_branch}' into the following branches: {', '.join(target_branches)}\nDo you want to proceed? (yes/no): ")
    
    if confirm.lower() != 'yes':
        logging.warning("Operation cancelled by user.")
        exit(1)
    
    update_branches(source_branch, target_branches)
    handle_unstaged_changes()

if __name__ == "__main__":
    main()
```


### useful.git-create-new-repo.py
```python
\# Filename: useful.git\-create\-new\-repo.py
\# This script helps create a new Git repository

import os
import logging
import subprocess

\# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("script.log"), logging.StreamHandler()])

def initialize_and_setup_repo():
    \# Set the absolute path for the current directory
    directory_path = os.path.abspath('.')
    logging.info(f"Directory path: {directory_path}")
    
    \# Get the last part of the directory path
    repo_name = os.path.basename(directory_path)
    logging.info(f"Repo name: {repo_name}")

    \# Check if the directory already has a Git repo
    if os.path.isdir(os.path.join(directory_path, ".git")):
        logging.info("Directory already has a git repo")
        return

    \# Create a new GitHub repository with the current directory name
    subprocess.run(["gh", "repo", "create", repo_name, "--private", "-y"])
    logging.info(f"GitHub repository '{repo_name}' created successfully!")

    \# Initialize a new Git repo
    subprocess.run(["git", "init", "--quiet"])

    \# Add all of the files to the repo
    subprocess.run(["git", "add", "*"])

    \# Commit the changes to the repo
    subprocess.run(["git", "commit", "-m", "Initial commit on main branch"])

    \# Add the remote origin
    remote_url = f"https://github.com/inayet/{repo_name}.git"
    subprocess.run(["git", "remote", "add", "origin", remote_url])

    \# Push the main branch to the new GitHub repository
    subprocess.run(["git", "push", "-u", "origin", "main"])

    \# Create the 'production' branch, commit, and push
    subprocess.run(["git", "checkout", "-b", "production"])
    subprocess.run(["git", "push", "-u", "origin", "production"])
    logging.info("Created and pushed 'production' branch.")

    \# Switch back to main to create the 'development' branch, commit, and push
    subprocess.run(["git", "checkout", "main"])
    subprocess.run(["git", "checkout", "-b", "development"])
    subprocess.run(["git", "push", "-u", "origin", "development"])
    logging.info("Created and pushed 'development' branch.")

    \# Log the success message
    logging.info("Repo setup complete!")

if __name__ == "__main__":
    initialize_and_setup_repo()

```
