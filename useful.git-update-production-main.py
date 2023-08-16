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
