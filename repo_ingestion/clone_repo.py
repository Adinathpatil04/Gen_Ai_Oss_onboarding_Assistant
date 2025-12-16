from git import Repo
import os

def clone_repository(repo_url, base_dir="repos"):
    """
    Clones a GitHub repository to a local directory.
    """
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        print(f"Repository already exists at {repo_path}")
        return repo_path

    print("Cloning repository...")
    Repo.clone_from(repo_url, repo_path)
    print("Clone completed!")

    return repo_path
