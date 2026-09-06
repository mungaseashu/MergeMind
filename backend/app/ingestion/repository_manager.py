import os
import shutil
from pathlib import Path
from git import Repo
from app.github.client import github_client

class RepositoryManager:
    def __init__(self, base_clone_dir: str = "/tmp/mergemind_repos"):
        self.base_clone_dir = Path(base_clone_dir)
        self.base_clone_dir.mkdir(parents=True, exist_ok=True)

    def process_repository(self, repo_url: str, github_token: str = None):
        """
        Parses URL, fetches info, clones repo, returns local path and info.
        """
        # Simplistic URL parsing: https://github.com/owner/repo
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid repository URL")
        
        owner = parts[-2]
        repo_name = parts[-1].replace(".git", "")
        full_name = f"{owner}/{repo_name}"

        # Get info from GitHub API
        repo_info = github_client.get_repository_info(full_name, github_token)
        
        # Clone locally - use a unique UUID to prevent "directory already exists" errors on Windows
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        clone_path = self.base_clone_dir / f"{owner}_{repo_name}_{unique_id}"
        
        # Inject token into clone URL if provided
        clone_url = repo_info['clone_url']
        if github_token and clone_url.startswith("https://"):
            clone_url = clone_url.replace("https://", f"https://{github_token}@")
        
        print(f"Cloning {clone_url.replace(github_token, '***') if github_token else clone_url} to {clone_path}...")
        Repo.clone_from(clone_url, clone_path)

        return {
            "local_path": str(clone_path),
            "info": repo_info
        }

repository_manager = RepositoryManager(base_clone_dir="./data/repos")
