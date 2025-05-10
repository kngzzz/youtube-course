import { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const [inputUrl, setInputUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [course, setCourse] = useState(null);
  const [recentCourses, setRecentCourses] = useState([]);

  // Fetch recent courses on load
  useEffect(() => {
    const fetchRecentCourses = async () => {
      try {
        const response = await axios.get(`${API}/courses`);
        setRecentCourses(response.data);
      } catch (err) {
        console.error("Error fetching recent courses:", err);
      }
    };

    fetchRecentCourses();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Form validation
    if (!inputUrl) {
      setError("Please enter a YouTube URL");
      return;
    }
    
    // Simple URL validation
    if (!inputUrl.includes('youtube.com/watch') && !inputUrl.includes('youtu.be') && !inputUrl.includes('learnfromvideo.com/watch')) {
      setError("Please enter a valid YouTube or LearnFromVideo URL");
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API}/convert-youtube`, {
        video_url: inputUrl
      });
      
      setCourse(response.data);
      setLoading(false);
      
      // Add to recent courses if not already there
      if (!recentCourses.find(c => c.id === response.data.id)) {
        setRecentCourses(prevCourses => [response.data, ...prevCourses.slice(0, 4)]);
      }
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.detail || "An error occurred while processing the video");
      console.error("Error:", err);
    }
  };

  const handleExampleUrl = () => {
    setInputUrl("https://www.youtube.com/watch?v=dQw4w9WgXcQ");
  };
  
  // Function to convert YouTube URLs to our site format
  const convertUrl = (url) => {
    if (!url) return "";
    return url.replace("youtube.com", "learnfromvideo.com");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-900 to-purple-900 text-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-indigo-300">
              <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
            </svg>
            <h1 className="text-2xl font-bold">LearnFromVideo</h1>
          </div>
          <div>
            <button className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg">
              Sign In
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Hero Section */}
        <section className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400">
            Transform YouTube Videos Into Interactive Courses
          </h1>
          <p className="text-xl text-indigo-200 max-w-3xl mx-auto mb-8">
            Our AI instantly converts any YouTube video into a beautifully structured
            course with diagrams, summaries, and interactive learning materials.
          </p>
          
          {/* URL Input Form */}
          <div className="max-w-2xl mx-auto mb-10">
            <form onSubmit={handleSubmit} className="flex flex-col items-center">
              <div className="w-full flex flex-col md:flex-row gap-2 mb-4">
                <input
                  type="text"
                  value={inputUrl}
                  onChange={(e) => setInputUrl(e.target.value)}
                  placeholder="Paste YouTube URL here (e.g., https://www.youtube.com/watch?v=...)"
                  className="flex-grow px-4 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 rounded-lg font-semibold transition-colors disabled:bg-gray-400"
                >
                  {loading ? "Converting..." : "Create Course"}
                </button>
              </div>
              
              {error && (
                <div className="text-red-300 mb-4">{error}</div>
              )}
              
              <p className="text-indigo-300 text-sm">
                Don't have a URL? <button 
                  type="button" 
                  onClick={handleExampleUrl}
                  className="text-cyan-400 hover:underline"
                >
                  Try an example
                </button>
              </p>
            </form>
          </div>
          
          <div className="mb-8">
            <div className="inline-block px-3 py-1 rounded-full bg-indigo-800/50 text-indigo-300 text-sm">
              Just replace "youtube.com" with "learnfromvideo.com" in any URL!
            </div>
          </div>
        </section>

        {/* Course Display Section */}
        {course && (
          <section className="mb-16 bg-white/10 backdrop-blur-sm rounded-xl p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold mb-2">{course.title}</h2>
              <div className="flex items-center space-x-2 text-indigo-300 text-sm mb-4">
                <span>Course URL:</span>
                <a 
                  href={convertUrl(inputUrl)}
                  className="hover:text-cyan-400 break-all"
                >
                  {convertUrl(inputUrl)}
                </a>
              </div>
              <div className="flex flex-col md:flex-row gap-6">
                <div className="w-full md:w-1/3">
                  <img 
                    src={course.thumbnail_url} 
                    alt={course.title} 
                    className="w-full h-auto rounded-lg"
                  />
                  <div className="mt-4 p-4 bg-indigo-800/30 rounded-lg">
                    <h3 className="font-semibold mb-2">Course Overview</h3>
                    <p className="text-indigo-200 text-sm">{course.description}</p>
                  </div>
                </div>
                <div className="w-full md:w-2/3">
                  <h3 className="text-xl font-semibold mb-4">Course Content</h3>
                  <div className="space-y-4">
                    {course.sections.map(section => (
                      <div key={section.id} className="p-4 bg-indigo-800/30 rounded-lg transition-all hover:bg-indigo-700/40">
                        <h4 className="font-bold text-lg">{section.title}</h4>
                        <p className="text-indigo-200">{section.content}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
            
            {/* Visualizations */}
            {course.visualizations.length > 0 && (
              <div className="mt-8">
                <h3 className="text-xl font-semibold mb-4">Visual Learning Aids</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {course.visualizations.map(vis => (
                    <div key={vis.id} className="p-4 bg-indigo-800/30 rounded-lg">
                      <h4 className="font-bold text-lg mb-2">{vis.title}</h4>
                      {vis.image_url ? (
                        <img src={vis.image_url} alt={vis.title} className="w-full h-auto rounded mb-2" />
                      ) : (
                        <div className="bg-indigo-700/50 p-4 rounded mb-2 flex items-center justify-center h-40">
                          <span className="text-indigo-300">Visualization will appear here</span>
                        </div>
                      )}
                      <p className="text-indigo-200 text-sm">{vis.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </section>
        )}

        {/* Recent Courses Section */}
        {recentCourses.length > 0 && !course && (
          <section>
            <h2 className="text-2xl font-bold mb-6">Recent Courses</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {recentCourses.map(recentCourse => (
                <div 
                  key={recentCourse.id} 
                  className="bg-white/10 backdrop-blur-sm rounded-lg overflow-hidden hover:bg-white/15 transition-all"
                  onClick={() => setCourse(recentCourse)}
                >
                  <img 
                    src={recentCourse.thumbnail_url} 
                    alt={recentCourse.title} 
                    className="w-full h-48 object-cover"
                  />
                  <div className="p-4">
                    <h3 className="font-bold text-lg mb-2 line-clamp-1">{recentCourse.title}</h3>
                    <p className="text-indigo-200 text-sm line-clamp-2 mb-3">{recentCourse.description}</p>
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-indigo-300">
                        {new Date(recentCourse.created_at).toLocaleDateString()}
                      </span>
                      <button className="text-sm bg-indigo-600 hover:bg-indigo-700 px-2 py-1 rounded">
                        View Course
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Features Section */}
        {!course && (
          <section className="py-12">
            <h2 className="text-2xl font-bold mb-6 text-center">Transform How You Learn From Videos</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg">
                <div className="rounded-full bg-emerald-500/20 w-12 h-12 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-emerald-400">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 0 1 0 3.75H5.625a1.875 1.875 0 0 1 0-3.75Z" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-2">Structured Content</h3>
                <p className="text-indigo-200">
                  Our AI analyzes videos and organizes content into logical sections, 
                  making it easier to understand and review complex topics.
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg">
                <div className="rounded-full bg-cyan-500/20 w-12 h-12 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-cyan-400">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 0 0 6 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0 1 18 16.5h-2.25m-7.5 0h7.5m-7.5 0-1 3m8.5-3 1 3m0 0 .5 1.5m-.5-1.5h-9.5m0 0-.5 1.5m.75-9 3-3 2.148 2.148A12.061 12.061 0 0 1 16.5 7.605" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-2">Visual Learning</h3>
                <p className="text-indigo-200">
                  Automatically generated diagrams and visualizations help you 
                  understand complex concepts through interactive visual aids.
                </p>
              </div>
              
              <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg">
                <div className="rounded-full bg-purple-500/20 w-12 h-12 flex items-center justify-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 text-purple-400">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 0 1-.825-.242m9.345-8.334a2.126 2.126 0 0 0-.476-.095 48.64 48.64 0 0 0-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0 0 11.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
                  </svg>
                </div>
                <h3 className="text-xl font-bold mb-2">Conversational AI</h3>
                <p className="text-indigo-200">
                  Ask questions about the content and receive instant, intelligent 
                  responses to deepen your understanding of the material.
                </p>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-indigo-950 py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <p className="text-indigo-400">&copy; 2025 LearnFromVideo. All rights reserved.</p>
            </div>
            <div className="flex space-x-4">
              <a href="#" className="text-indigo-400 hover:text-white">About</a>
              <a href="#" className="text-indigo-400 hover:text-white">Privacy</a>
              <a href="#" className="text-indigo-400 hover:text-white">Terms</a>
              <a href="#" className="text-indigo-400 hover:text-white">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <Home />
    </div>
  );
}

export default App;
