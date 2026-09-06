from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.brain.indexing_pipeline import pipeline
from app.core.github_services import setup_github_webhook

router = APIRouter()

class IndexRequest(BaseModel):
    project_name: str
    repository_url: str
    github_token: Optional[str] = None

@router.post("/index")
async def start_indexing(req: IndexRequest):
    if not req.repository_url:
        raise HTTPException(status_code=400, detail="Repository URL is required")
    
    # Try to set up webhook if token is provided
    if req.github_token:
        setup_github_webhook(req.repository_url, req.github_token)

    # We will trigger the background pipeline
    try:
        # Pass project_name to start_job (we need to update start_job signature if we want to store it, 
        # but for now we just start the pipeline for the repo)
        job_id = pipeline.start_job(req.repository_url, req.github_token)
        return {
            "job_id": job_id,
            "repository": req.repository_url,
            "status": "queued"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    status = pipeline.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status
