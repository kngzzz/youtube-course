from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import re
import requests
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class YouTubeInput(BaseModel):
    video_url: str

class CourseSection(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    timestamp: Optional[str] = None
    order: int

class CourseVisualization(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    image_url: Optional[str] = None
    description: str
    related_section_id: str

class Course(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    video_id: str
    title: str
    description: str
    thumbnail_url: str
    sections: List[CourseSection] = []
    visualizations: List[CourseVisualization] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Helper functions
def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    youtube_regex = (
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    match = re.match(youtube_regex, url)
    if not match:
        return None
    return match.group(6)

async def fetch_video_metadata(video_id: str) -> Dict:
    """Placeholder for fetching video metadata - will use Google API in production."""
    # This is a mock - in real implementation, we'd call the YouTube Data API
    # We'll need to ask the user for a YouTube Data API key when implementing that part
    mock_data = {
        "title": f"Example Video {video_id}",
        "description": "This is a placeholder description for the video.",
        "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    }
    return mock_data

async def process_course_content(video_id: str, video_metadata: Dict) -> Course:
    """Create a course object with placeholder content."""
    # This is where we'd use Gemini 2.5 Pro to process the video transcript
    # For now, we'll create a mock course structure
    course = Course(
        video_id=video_id,
        title=video_metadata["title"],
        description=video_metadata["description"],
        thumbnail_url=video_metadata["thumbnail_url"],
        sections=[
            CourseSection(
                title="Introduction",
                content="Welcome to this course! This section introduces the main concepts.",
                order=1
            ),
            CourseSection(
                title="Main Concepts",
                content="The core ideas of this topic are explained here in detail.",
                order=2
            ),
            CourseSection(
                title="Practical Examples",
                content="Here are some examples to help illustrate the concepts.",
                order=3
            ),
            CourseSection(
                title="Summary and Conclusion",
                content="Let's review what we've learned and discuss next steps.",
                order=4
            ),
        ],
        visualizations=[
            CourseVisualization(
                title="Concept Map",
                description="A visual representation of the main concepts covered in this video.",
                related_section_id="2"
            )
        ]
    )
    
    # Store in database
    course_dict = course.dict()
    await db.courses.insert_one(course_dict)
    
    return course

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.post("/convert-youtube", response_model=Course)
async def convert_youtube_to_course(input: YouTubeInput, background_tasks: BackgroundTasks):
    # Extract video ID from the URL
    video_id = extract_video_id(input.video_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Check if we've already processed this video
    existing_course = await db.courses.find_one({"video_id": video_id})
    if existing_course:
        # Return the existing course
        return Course(**existing_course)
    
    # Fetch video metadata (title, description, thumbnail)
    video_metadata = await fetch_video_metadata(video_id)
    
    # Process the video content and create a course
    course = await process_course_content(video_id, video_metadata)
    
    return course

@api_router.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: str):
    course = await db.courses.find_one({"id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return Course(**course)

@api_router.get("/courses", response_model=List[Course])
async def get_all_courses():
    courses = await db.courses.find().to_list(20)
    return [Course(**course) for course in courses]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
