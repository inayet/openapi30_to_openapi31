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
