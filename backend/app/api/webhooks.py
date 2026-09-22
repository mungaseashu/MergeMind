"""
Webhook API Endpoint — POST /api/webhooks/github

This endpoint receives real-time events from GitHub.
Every incoming request is first verified using HMAC-SHA256 before any processing occurs.
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
from app.core.security import verify_github_signature
from app.brain.pr_handlers import handle_pr_opened, handle_pr_synchronize, handle_pr_closed

router = APIRouter()

# GitHub events we care about
SUPPORTED_PR_ACTIONS = {"opened", "synchronize", "closed", "reopened"}


@router.post("/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None),
    x_github_event: Optional[str] = Header(None),
):
    """
    Receives and processes GitHub webhook payloads.

    Security:
    - Verifies the HMAC-SHA256 signature in X-Hub-Signature-256 header.
    - Rejects requests that don't match the configured GITHUB_WEBHOOK_SECRET.

    Supported events: pull_request
    Supported actions: opened, synchronize, closed, reopened
    """
    # 1. Read raw body BEFORE parsing JSON (needed for HMAC)
    raw_body = await request.body()

    # 2. Verify the signature immediately
    verify_github_signature(raw_body, x_hub_signature_256 or "")

    # 3. Parse the JSON payload
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    # 4. Route by event type
    event = x_github_event or ""

    if event == "ping":
        # GitHub sends this when a webhook is first created — just confirm receipt
        return {"message": "pong", "status": "webhook configured successfully"}

    if event == "pull_request":
        action = payload.get("action", "")

        if action not in SUPPORTED_PR_ACTIONS:
            return {"status": "ignored", "reason": f"PR action '{action}' is not handled"}

        repo_url = payload.get("repository", {}).get("html_url")
        from app.brain.indexing_pipeline import repo_tokens
        from app.core.config import settings
        token = repo_tokens.get(repo_url) or settings.GITHUB_TOKEN if repo_url else settings.GITHUB_TOKEN

        if action in ("opened", "reopened"):
            result = handle_pr_opened(payload, github_token=token)
        elif action == "synchronize":
            result = handle_pr_synchronize(payload, github_token=token)
        elif action == "closed":
            result = handle_pr_closed(payload)
        else:
            result = {"status": "ignored"}

        return result

    if event == "push":
        # A push to the default branch means the codebase changed directly.
        # We trigger a background re-scan. Neo4j MERGE ensures we just update/add new nodes.
        repo_url = payload.get("repository", {}).get("html_url")
        if repo_url:
            from app.brain.indexing_pipeline import pipeline, repo_tokens
            from app.core.config import settings
            # Try to get token from memory first, then fallback to .env settings
            token = repo_tokens.get(repo_url) or settings.GITHUB_TOKEN
            pipeline.start_job(repo_url, token)
            return {"status": "accepted", "action": "re-indexing"}
        return {"status": "ignored", "reason": "No repository URL in payload"}

    # Any other event (stars, issues, etc.) — acknowledge but don't process
    return {"status": "ignored", "reason": f"Event '{event}' is not handled by MergeMind"}
