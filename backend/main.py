from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid
import asyncio

from scraper import InstagramCommentScraper

app = FastAPI(title="Instagram Comment Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs_db = {}
user_comments_db = {}

class AnalyzeRequest(BaseModel):
    username: str

def run_scraper_sync(task_id: str, username: str):
    """
    Synchronous worker method executing the real Instaloader engine.
    """
    scraper = InstagramCommentScraper(target_username=username)
    
    def progress_callback(msg: str):
        jobs_db[task_id]["progress"] = msg

    try:
        # Run real scrape
        results = scraper.scan_target_posts(update_progress_callback=progress_callback)
        
        jobs_db[task_id]["status"] = "completed"
        if not results:
             jobs_db[task_id]["progress"] = "Scan complete. No comments found on recent public posts or account is private."
        else:
             jobs_db[task_id]["progress"] = f"Extraction complete! Found {len(results)} verified comments."
             
        jobs_db[task_id]["comments"] = results
        user_comments_db[username] = results
        
    except Exception as e:
        jobs_db[task_id]["status"] = "failed"
        jobs_db[task_id]["progress"] = f"Engine Error: {str(e)}"

async def background_scrape_task(task_id: str, username: str):
    jobs_db[task_id] = {"status": "scraping", "progress": "Allocating scraper node...", "comments": []}
    await asyncio.sleep(1) # Brief setup delay
    # Offload the blocking scraper to a background thread
    await asyncio.to_thread(run_scraper_sync, task_id, username)

@app.post("/api/v1/analyze")
async def start_analysis(req: AnalyzeRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(background_scrape_task, task_id, req.username)
    return {"task_id": task_id, "status": "job_enqueued"}

@app.get("/api/v1/jobs/{task_id}")
async def get_job_status(task_id: str):
    job = jobs_db.get(task_id, {"status": "not_found"})
    return {"task_id": task_id, **job}

@app.get("/api/v1/users/{username}/comments")
async def get_user_comments(username: str):
    comments = user_comments_db.get(username, [])
    return {
        "username": username,
        "comments": comments
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
