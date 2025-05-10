from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Depends
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
import json
from datetime import datetime
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Optional Gemini configuration (will be used if API key is provided)
gemini_api_key = os.environ.get('GEMINI_API_KEY')
youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

# Configure Gemini if API key is available
if gemini_api_key and gemini_api_key != "YOUR_GEMINI_API_KEY":
    genai.configure(api_key=gemini_api_key)
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 4096,
    }
    has_gemini = True
else:
    has_gemini = False

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
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie|learnfromvideo)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    match = re.match(youtube_regex, url)
    if not match:
        return None
    return match.group(6)

async def fetch_video_metadata(video_id: str) -> Dict:
    """Fetch video metadata using YouTube API."""
    # This is a mock - in real implementation we'd use the YouTube Data API
    # We'd need to ask for a YouTube API key for a full implementation
    api_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key=YOUR_API_KEY&part=snippet"
    
    # For now, we'll just use a placeholder with the thumbnail
    mock_data = {
        "title": f"Video: {video_id}",
        "description": "This is a placeholder description for the video.",
        "thumbnail_url": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    }
    return mock_data

async def get_video_transcript(video_id: str) -> str:
    """Get transcript of a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = " ".join([item["text"] for item in transcript_list])
        return full_transcript
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        # If transcript is not available, return an empty string
        logger.warning(f"Transcript not available for video {video_id}: {str(e)}")
        return ""
    except Exception as e:
        logger.error(f"Error fetching transcript for video {video_id}: {str(e)}")
        return ""

# This function would use Gemini API to process course content
async def process_with_gemini(transcript: str, video_metadata: Dict) -> Dict:
    """Process the video transcript with Gemini to create a structured course."""
    
    if has_gemini and transcript:
        try:
            # Use Gemini to process the transcript
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"""
            You are an expert educator who specializes in creating structured educational content.
            
            Please analyze the following video transcript and create a structured course with clear sections.
            
            Video Title: {video_metadata['title']}
            Video Description: {video_metadata['description']}
            
            Transcript:
            {transcript[:10000]}  # Truncate if too long
            
            Create a structured course with the following:
            1. 4-8 logical sections, each with a title and detailed content
            2. Each section should have a timestamp if you can identify when in the video that section starts
            3. Also create one visualization idea for the course (a diagram or chart that would help illustrate a key concept)
            
            Format your response as a JSON object with the following structure:
            {{
                "sections": [
                    {{
                        "title": "Section Title",
                        "content": "Detailed content for this section",
                        "timestamp": "MM:SS",
                        "order": 1
                    }},
                    ...
                ],
                "visualizations": [
                    {{
                        "title": "Visualization Title",
                        "description": "Description of what this visualization shows",
                        "related_section_id": "1" // The order number of the related section
                    }}
                ]
            }}
            
            Ensure the content is educational, well-structured, and enhances learning.
            """
            
            response = model.generate_content(prompt, generation_config=generation_config)
            try:
                # Try to parse the response as JSON
                response_text = response.text
                # Find the JSON part if there's any text before or after
                json_start = response_text.find('{')
                json_end = response_text.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response_text[json_start:json_end]
                    return json.loads(json_str)
                raise ValueError("No valid JSON found in response")
                raise ValueError("No valid JSON found in response")
            except Exception as e:
                # If parsing fails, fall back to mock data
                logger.error(f"Error parsing Gemini response: {str(e)}")
                return get_mock_data()
        except Exception as e:
            logger.error(f"Error using Gemini API: {str(e)}")
            return get_mock_data()
    
    return get_mock_data()

def get_mock_data():
    """Return mock data when Gemini API is not available or fails."""
    mock_sections = [
        {
            "title": "Introduction",
            "content": "Welcome to this course! This section introduces the main concepts.",
            "timestamp": "00:00",
            "order": 1
        },
        {
            "title": "Main Concepts",
            "content": "The core ideas of this topic are explained here in detail.",
            "timestamp": "03:45",
            "order": 2
        },
        {
            "title": "Practical Examples",
            "content": "Here are some examples to help illustrate the concepts.",
            "timestamp": "08:30",
            "order": 3
        },
        {
            "title": "Summary and Conclusion",
            "content": "Let's review what we've learned and discuss next steps.",
            "timestamp": "12:15",
            "order": 4
        },
    ]
    
    mock_visualizations = [
        {
            "title": "Concept Map",
            "image_url": None,  # In a real implementation, we'd generate and store an image
            "description": "A visual representation of the main concepts covered in this video.",
            "related_section_id": "2"
        }
    ]
    
    return {
        "sections": mock_sections,
        "visualizations": mock_visualizations
    }

async def process_course_content(video_id: str, video_metadata: Dict) -> Course:
    """Create a course object from the video content."""
    # Get the video transcript
    transcript = await get_video_transcript(video_id)
    
    # Process with Gemini (currently using mock data)
    processed_content = await process_with_gemini(transcript, video_metadata)
    
    # Create course object
    course = Course(
        video_id=video_id,
        title=video_metadata["title"],
        description=video_metadata["description"],
        thumbnail_url=video_metadata["thumbnail_url"],
        sections=[CourseSection(**section) for section in processed_content["sections"]],
        visualizations=[CourseVisualization(**vis) for vis in processed_content["visualizations"]]
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
