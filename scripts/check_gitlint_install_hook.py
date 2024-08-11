import subprocess
import os
import sys


def is_command_available(command):
    """Check if a command is available on the system."""
    ## check windows and linux both
    check_command = ['where', command] if os.name == 'nt' else ['which', command]
    result = subprocess.run(check_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0


def is_commitmsg_hook_set():
    """Check if the gitlint hook is set up in the commit-msg file."""
    ##
    commit_msg_hook_path = '.git/hooks/commit-msg'
    if not os.path.isfile(commit_msg_hook_path):
        return False
    with open(commit_msg_hook_path, 'r') as file:
        content = file.read()
    return 'gitlint' in content


def install_gitlint_hook():
    """Install the gitlint hook."""
    result = subprocess.run(['gitlint', 'install-hook'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0


def main():
    if not is_command_available('gitlint'):
        print("gitlint could not be found. Please install gitlint first.")
        sys.exit(1)

    if not is_commitmsg_hook_set():
        print("commit-msg hook is not set up. Setting it up now...")
        if install_gitlint_hook():
            print("gitlint install-hook set up successfully.")
        else:
            print("Failed to set up gitlint install-hook.")
            sys.exit(1)
    else:
        # print("gitlint install-hook is already set up.")
        print("commit-msg is already set up.")


if __name__ == "__main__":
    main()
