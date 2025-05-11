# LearnFromVideo - AI-Powered YouTube Course Generator

![LearnFromVideo Banner](https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg)

## 🚀 Product Overview

LearnFromVideo is an innovative AI-powered platform that transforms any YouTube video into a structured, educational course. Simply paste a YouTube URL or use our easy URL conversion (just replace "youtube.com" with "learnfromvideo.com" in any YouTube URL), and our AI will generate a beautifully organized course with:

- 📚 **Structured Content**: Automatically organized into logical sections
- 🖼️ **Interactive Diagrams**: Visual representations of key concepts
- 💬 **Conversational AI**: Ask questions about any part of the course
- 📱 **Responsive Design**: Beautiful on any device

Perfect for students, educators, and lifelong learners who want to extract maximum value from educational YouTube content.

## ✨ Features

- **URL Conversion**: Simply replace "youtube.com" with "learnfromvideo.com" in any YouTube URL
- **AI Content Processing**: Uses Gemini 2.5 Pro to analyze and structure video content
- **Transcript Extraction**: Automatically retrieves and processes video transcripts
- **Visual Learning Aids**: Generates diagrams and visualizations to enhance understanding
- **Interactive Q&A**: Conversational AI to answer questions about the course content
- **Beautiful UI**: Intuitive, responsive design for a great learning experience

## 📋 Prerequisites

- Python 3.10+ for the backend
- Node.js 16+ for the frontend
- MongoDB (local installation or MongoDB Atlas)
- API keys for:
  - Google Gemini (for AI processing)
  - YouTube Data API (for video metadata)

## 🔧 Installation

### Windows Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/learnfromvideo.git
   cd learnfromvideo
   ```

2. **Set up the backend**
   ```
   cd backend
   python -m venv venv
   venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. **Create .env file in the backend directory**
   ```
   MONGO_URL="mongodb://localhost:27017"
   DB_NAME="learnfromvideo"
   GEMINI_API_KEY="your_gemini_api_key"
   YOUTUBE_API_KEY="your_youtube_api_key"
   ```

4. **Set up the frontend**
   ```
   cd ../frontend
   npm install
   ```

5. **Create .env file in the frontend directory**
   ```
   REACT_APP_BACKEND_URL="http://localhost:8001"
   ```

6. **Start MongoDB** (if using local installation)
   ```
   mongod --dbpath=data
   ```

7. **Start the application**
   ```
   # Terminal 1 (Backend)
   cd backend
   venv\\Scripts\\activate
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload

   # Terminal 2 (Frontend)
   cd frontend
   npm start
   ```

### macOS/Linux Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/learnfromvideo.git
   cd learnfromvideo
   ```

2. **Set up the backend**
   ```
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create .env file in the backend directory**
   ```
   MONGO_URL="mongodb://localhost:27017"
   DB_NAME="learnfromvideo"
   GEMINI_API_KEY="your_gemini_api_key"
   YOUTUBE_API_KEY="your_youtube_api_key"
   FAL_KEY="your_fal_api_key"
   ```

4. **Set up the frontend**
   ```
   cd ../frontend
   npm install
   ```

5. **Create .env file in the frontend directory**
   ```
   REACT_APP_BACKEND_URL="http://localhost:8001"
   ```

6. **Start MongoDB** (if using local installation)
   ```
   mongod --dbpath=data
   ```

7. **Start the application**
   ```
   # Terminal 1 (Backend)
   cd backend
   source venv/bin/activate
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload

   # Terminal 2 (Frontend)
   cd frontend
   npm start
   ```

## ⚙️ Configuration

### API Keys

To use all features of LearnFromVideo, you'll need to obtain the following API keys:

1. **Google Gemini API Key**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Add to your backend `.env` file as `GEMINI_API_KEY`

2. **YouTube Data API Key**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the YouTube Data API v3
   - Create credentials and get the API key
   - Add to your backend `.env` file as `YOUTUBE_API_KEY`


## 🖥️ Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter a YouTube URL in the input field and click "Create Course"
3. Alternatively, replace "youtube.com" with "learnfromvideo.com" in any YouTube URL and paste it in your browser
4. Wait for the AI to process the video (this may take a few seconds)
5. Explore the structured course content, visualizations, and use the chat interface to ask questions

## 🔮 Future Improvements

- Enhanced diagram generation with more types of visual aids
- Expanded conversational AI capabilities
- Downloadable course materials (PDF, EPUB)
- User accounts and saved courses
- Collaborative learning features
- Mobile applications
