import os
from github import Github, Auth
from app.core.config import settings

class GitHubClient:
    def __init__(self):
        # We can use a token if provided, otherwise unauthenticated (rate-limited)
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            auth = Auth.Token(token)
            self.client = Github(auth=auth)
        else:
            self.client = Github()

    def get_repository_info(self, repo_full_name: str):
        """
        repo_full_name format: 'owner/repo'
        """
        try:
            repo = self.client.get_repo(repo_full_name)
            return {
                "owner": repo.owner.login,
                "name": repo.name,
                "full_name": repo.full_name,
                "default_branch": repo.default_branch,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url
            }
        except Exception as e:
            raise Exception(f"Failed to fetch repository info: {e}")

github_client = GitHubClient()
