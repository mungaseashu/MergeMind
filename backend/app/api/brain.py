from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any
from app.brain.indexing_pipeline import pipeline

router = APIRouter()

class IndexRequest(BaseModel):
    repository_url: str

@router.post("/index")
async def start_indexing(req: IndexRequest):
    if not req.repository_url:
        raise HTTPException(status_code=400, detail="Repository URL is required")
    
    # We will trigger the background pipeline
    try:
        job_id = pipeline.start_job(req.repository_url)
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
