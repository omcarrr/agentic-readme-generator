"""
Tools for the agent to read file structures and contents safely.
"""
import os
from langchain.tools import tool

# Edge Case Handling: Prevent massive folders from breaking the LLM
IGNORE_DIRS = {'.git', '__pycache__', 'node_modules', 'venv', 'env', '.idea', '.vscode', 'dist', 'build'}
IGNORE_EXTS = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.tar', '.gz'}

IGNORE_FILES = {'.env', '.env.local', '.env.development', 'secrets.json', 'credentials.json', 'config.local.py'}
MAX_FILE_CHARS = 10000

@tool
def get_project_structure(folder_path: str) -> str:
    """Returns the directory tree structure of the project."""
    if not os.path.exists(folder_path):
        return "Error: Directory does not exist."
    
    tree_str = f"Project Structure for {os.path.basename(folder_path)}:\n"
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        level = root.replace(folder_path, '').count(os.sep)
        indent = ' ' * 4 * level
        tree_str += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        
        for f in files:
            # Added: "and f not in IGNORE_FILES"
            if not any(f.endswith(ext) for ext in IGNORE_EXTS) and f not in IGNORE_FILES:
                tree_str += f"{subindent}{f}\n"
    return tree_str

@tool
def read_project_files(folder_path: str) -> str:
    """Reads the contents of relevant files in the directory."""
    if not os.path.exists(folder_path):
        return "Error: Directory does not exist."
    
    file_contents = ""
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            # Added: "or file in IGNORE_FILES"
            if any(file.endswith(ext) for ext in IGNORE_EXTS) or file in IGNORE_FILES:
                continue
            
            filepath = os.path.join(root, file)
            relative_path = os.path.relpath(filepath, folder_path)
            
            # Edge Case: Empty Files
            if os.path.getsize(filepath) == 0:
                file_contents += f"\n--- File: {relative_path} ---\n[EMPTY FILE]\n"
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Edge Case: Extremely large files
                    if len(content) > MAX_FILE_CHARS:
                        content = content[:MAX_FILE_CHARS] + "\n...[TRUNCATED DUE TO SIZE]..."
                    file_contents += f"\n--- File: {relative_path} ---\n{content}\n"
            except UnicodeDecodeError:
                file_contents += f"\n--- File: {relative_path} ---\n[BINARY OR UNREADABLE FILE]\n"
                
    return file_contents