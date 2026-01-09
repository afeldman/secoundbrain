import os
import shutil
import frontmatter
from datetime import datetime
from fabric_second_brain.translator import translate_markdown # Added this import

def should_process_file(file_path, vault_path):
    """
    Determines if a file should be processed based on its path.
    - It's a Markdown file (.md).
    - It's not in a directory starting with '.'.
    - It's not in the 'Templates' directory.
    - It's not the README.md in the vault root.
    """
    if not file_path.lower().endswith('.md'):
        return False

    relative_path = os.path.relpath(file_path, vault_path)
    path_components = relative_path.split(os.sep)

    if any(part.startswith('.') for part in path_components):
        return False

    if 'Templates' in path_components:
        return False

    if relative_path == 'README.md':
        return False

    return True


def process_and_move_file(file_path, vault_path, daily_notes_path):
    """
    Processes a single Markdown file and moves it to the appropriate directory.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read() # Read content as string
        
        content = translate_markdown(content) # Apply translation

        post = frontmatter.loads(content) # Load frontmatter from string
        tags = post.get('tags', [])

        if 'daily-note' in tags:
            creation_date_str = post.get('creation_date')
            if creation_date_str:
                try:
                    creation_date = datetime.fromisoformat(creation_date_str)
                    year_dir = os.path.join(daily_notes_path, str(creation_date.year))
                    if not os.path.exists(year_dir):
                        os.makedirs(year_dir)
                    
                    new_file_path = os.path.join(year_dir, os.path.basename(file_path))
                    
                    if os.path.abspath(file_path) != os.path.abspath(new_file_path):
                        shutil.move(file_path, new_file_path)
                        print(f"Moved daily note: {file_path} to {new_file_path}")
                    else:
                        print(f"Skipped moving daily note as it's already in the target directory: {file_path}")

                except (ValueError, TypeError) as e:
                    print(f"Error processing date for {file_path}: {e}")
            else:
                print(f"Warning: 'creation_date' not found in daily note: {file_path}")
        else:
            print(f"Skipping non-daily note: {file_path}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def organize(vault_path: str):
    """
    Organizes files in the vault by moving them to the appropriate directories.
    """
    print(f"Organizing vault at: {vault_path}")
    
    daily_notes_path = os.path.join(vault_path, 'daily')
    if not os.path.exists(daily_notes_path):
        os.makedirs(daily_notes_path)
        print(f"Created directory: {daily_notes_path}")

    for root, _, files in os.walk(vault_path):
        if '.git' in root or '.obsidian' in root:
            continue
        
        for file in files:
            file_path = os.path.join(root, file)
            if should_process_file(file_path, vault_path):
                process_and_move_file(file_path, vault_path, daily_notes_path)

    print("Vault organization complete.")