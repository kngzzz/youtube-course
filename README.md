# YouTube Course Generator

A full-stack application that converts YouTube videos into structured educational courses using AI.

## Features
- Convert YouTube videos into structured courses with logical sections
- AI-powered content organization using Google Gemini
- Automatic transcript extraction from YouTube videos
- MongoDB storage for created courses
- Modern React frontend with responsive design
- Docker containerization for easy deployment

## Tech Stack
- **Frontend**: 
  - React 19 with hooks
  - TailwindCSS for styling
  - React Router for navigation
  - Axios for API calls
- **Backend**: 
  - FastAPI framework
  - Python 3.11
  - Async MongoDB driver
  - YouTube Transcript API
- **Database**: MongoDB (Atlas or local)
- **AI Integration**: Google Gemini API
- **Infrastructure**: 
  - Docker for containerization
  - Nginx as reverse proxy
  - Multi-stage Docker builds

## Prerequisites
- Node.js 20+
- Python 3.11
- Docker and Docker Compose
- MongoDB Atlas account or local MongoDB instance
- Google Gemini API key (optional for AI features)
- YouTube API key (optional for enhanced metadata)

## Setup Instructions

### Development Environment
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd youtube-course
   ```

2. Configure environment variables:
   - Backend: Create `.env` file in `backend/` with:
     ```
     MONGO_URL=mongodb://localhost:27017
     DB_NAME=youtube_courses
     GEMINI_API_KEY=your_key_here (optional)
     YOUTUBE_API_KEY=your_key_here (optional)
     ```
   - Frontend: Create `.env` file in `frontend/` with:
     ```
     REACT_APP_API_URL=http://localhost:8001
     ```

3. Install dependencies:
   ```bash
   # Frontend
   cd frontend && yarn install

   # Backend
   cd ../backend && pip install -r requirements.txt
   ```

4. Run services:
   ```bash
   # Start MongoDB (if using local)
   docker run -d -p 27017:27017 --name mongo mongo

   # Backend
   cd backend && uvicorn server:app --reload --port 8001

   # Frontend (in separate terminal)
   cd frontend && yarn start
   ```

## Configuration

### Required Environment Variables
- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name for courses
- `FRONTEND_ENV`: Comma-separated frontend variables (API_URL)

### Optional Environment Variables
- `GEMINI_API_KEY`: For AI-powered content processing
- `YOUTUBE_API_KEY`: For enhanced video metadata

## API Documentation

### Endpoints
- `POST /api/convert-youtube`: Convert YouTube URL to course
  ```json
  {
    "video_url": "https://youtube.com/watch?v=example"
  }
  ```

- `GET /api/courses`: List all courses
- `GET /api/courses/{id}`: Get specific course by ID
- `GET /api/status`: Service health check

## Deployment

### Docker Build
```bash
docker build -t youtube-course .
```

### Docker Run
```bash
docker run -p 8080:8080 \
  -e MONGO_URL=mongodb://host.docker.internal:27017 \
  -e DB_NAME=youtube_courses \
  youtube-course
```

### Docker Compose
```yaml
version: '3'
services:
  app:
    image: youtube-course
    ports:
      - "8080:8080"
    environment:
      - MONGO_URL=mongodb://mongo:27017
      - DB_NAME=youtube_courses
    depends_on:
      - mongo

  mongo:
    image: mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

## Troubleshooting
- If YouTube transcripts aren't available, ensure the video has captions enabled
- For AI features, verify your Gemini API key is valid
- Check MongoDB connection if courses aren't saving
