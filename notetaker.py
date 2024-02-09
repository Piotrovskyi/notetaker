import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import re

def main():
    repo_path = read_from_config('repo_path')

    if repo_path is None:
        display_first_time_setup_banner()
        config_location = get_config_location()
        os.makedirs(config_location, exist_ok=True)

        repo_path = input("Absolute path to your idea repo: ")
        write_to_config('repo_path', relative_to_absolute(repo_path))

    editor_path = read_from_config('editor_path')
    if editor_path is None:
        print("What editor do you want to use for writing down your ideas?")
        print("1) vim (/usr/bin/vim)")
        print("2) nano (/usr/bin/nano)")
        print("3) Other (provide path to binary)")
        print()

        editor_choice = input("Alternative: ")
        if editor_choice == '1':
            editor_path = "/usr/bin/vim"
        elif editor_choice == '2':
            editor_path = "/usr/bin/nano"
        elif editor_choice == '3':
            editor_path = input("Path to editor binary: ")
        else:
            print("Invalid option, falling back to vim")
            editor_path = "/usr/bin/vim"

        if not os.path.exists(editor_path):
            raise Exception("Invalid editor path")

        write_to_config('editor_path', editor_path)

    commit_msg = input("Idea commit subject: ")
    current_datetime = datetime.now()
    human_readable = current_datetime.strftime("[%Y-%m-%d-%H:%M:%S]")

    dest_path = os.path.join(repo_path, "notes", human_readable + "-" + slugify(commit_msg))

    try:
        open_editor(editor_path, dest_path)
        print('Saved to: ', dest_path)
    except Exception as e:
        print(f"Could not open editor at path {editor_path}: {e}")

def relative_to_absolute(relative_path):
    return os.path.abspath(relative_path)

def slugify(text):
    # Replace non-word (alphanumeric and underscores) characters with a space
    text = re.sub(r'[^\w\s]', ' ', text)

    # Replace any whitespace or repeated hyphens with a single hyphen
    text = re.sub(r'[\s-]+', '-', text).strip('-')

    # Convert to lowercase
    return text.lower()

def display_first_time_setup_banner():
    banner = [
        "##########################################################",
        "####               Welcome to Notetaker!              ####",
        "##########################################################",
        "",
        "To get started, ensure you have a designated repository.",
        "This markdown file will be your canvas for brilliant ideas.",
        ""
    ]

    print("\n".join(banner))


def open_editor(bin_path, file_path):
    subprocess.check_call([bin_path, file_path])

def path_exists(path):
    return os.path.exists(path)

def read_from_config(key):
    location = get_config_location()
    path = os.path.join(location, key)
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def write_to_config(key, data):
    location = get_config_location()
    path = os.path.join(location, key)
    with open(path, 'w') as file:
        json.dump(data, file)

def get_config_location():
    return os.path.join(Path.home(), '.notetaker')

if __name__ == "__main__":
    main()
