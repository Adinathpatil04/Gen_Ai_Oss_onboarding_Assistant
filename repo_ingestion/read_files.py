import os

IGNORE_DIRS = {".git", "venv", "__pycache__", "tests", "docs"}

def read_source_files(repo_path):
    """
    Reads Python source files from a repository.
    Returns a list of (file_path, file_content).
    """
    code_files = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        code_files.append((full_path, content))
                except Exception as e:
                    print(f"Could not read {full_path}: {e}")

    return code_files
