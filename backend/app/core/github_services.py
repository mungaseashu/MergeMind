import logging
from github import Github
from app.core.config import settings

logger = logging.getLogger(__name__)

def setup_github_webhook(repository_url: str, token: str) -> bool:
    """
    Sets up a GitHub webhook for the given repository.
    """
    if not settings.WEBHOOK_BASE_URL:
        logger.warning("WEBHOOK_BASE_URL is not set. Skipping webhook creation.")
        return False

    try:
        # Extract owner/repo from url, e.g. https://github.com/owner/repo
        parts = repository_url.rstrip("/").split("/")
        if len(parts) < 2:
            raise ValueError("Invalid repository URL format.")
        repo_name = f"{parts[-2]}/{parts[-1]}"

        g = Github(token)
        repo = g.get_repo(repo_name)
        
        webhook_url = f"{settings.WEBHOOK_BASE_URL.rstrip('/')}/api/webhooks/github"
        
        config = {
            "url": webhook_url,
            "content_type": "json",
            "secret": settings.GITHUB_WEBHOOK_SECRET
        }
        
        # Check if webhook already exists
        for hook in repo.get_hooks():
            if hook.config.get("url") == webhook_url:
                logger.info(f"Webhook already exists for {repo_name}")
                return True
                
        repo.create_hook("web", config, ["push", "pull_request"], active=True)
        logger.info(f"Successfully created webhook for {repo_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to create webhook: {str(e)}")
        # We return False but don't raise, so indexing can still proceed
        return False
