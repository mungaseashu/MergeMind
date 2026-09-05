import hmac
import hashlib
from fastapi import HTTPException, Request
from app.core.config import settings


def verify_github_signature(payload_body: bytes, signature_header: str) -> bool:
    """
    Verifies that a webhook payload was sent by GitHub by validating the HMAC-SHA256 signature.

    GitHub computes:  sha256 = HMAC-SHA256(key=GITHUB_WEBHOOK_SECRET, data=raw_body)
    and sends it in the X-Hub-Signature-256 header as: 'sha256=<hex_digest>'

    Args:
        payload_body: The raw bytes of the request body.
        signature_header: The value of the X-Hub-Signature-256 header.

    Returns:
        True if valid.

    Raises:
        HTTPException 401 if signature is missing or invalid.
    """
    if not signature_header:
        raise HTTPException(
            status_code=401,
            detail="X-Hub-Signature-256 header is missing. Ensure the webhook secret is configured in GitHub."
        )

    if not signature_header.startswith("sha256="):
        raise HTTPException(status_code=401, detail="Invalid signature format.")

    secret_bytes = settings.GITHUB_WEBHOOK_SECRET.encode("utf-8")
    expected_signature = "sha256=" + hmac.new(
        key=secret_bytes,
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    # Use compare_digest to prevent timing attacks
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(
            status_code=401,
            detail="Signature mismatch. Payload may have been tampered with."
        )

    return True
