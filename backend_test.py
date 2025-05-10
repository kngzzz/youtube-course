import requests
import sys
import json
from datetime import datetime

class YouTubeCourseGeneratorTester:
    def __init__(self, base_url="https://81a81887-9ef8-490f-b5ed-b91803d55c4f.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.content:
                    try:
                        return success, response.json()
                    except json.JSONDecodeError:
                        print("Warning: Response is not valid JSON")
                        return success, None
                return success, None
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                if response.content:
                    try:
                        print(f"Response: {response.json()}")
                    except json.JSONDecodeError:
                        print(f"Response: {response.text}")
                return False, None

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, None

    def test_root_endpoint(self):
        """Test the root API endpoint"""
        return self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )

    def test_convert_youtube(self, video_url):
        """Test converting a YouTube URL to a course"""
        return self.run_test(
            "Convert YouTube URL",
            "POST",
            "convert-youtube",
            200,
            data={"video_url": video_url}
        )

    def test_get_all_courses(self):
        """Test retrieving all courses"""
        return self.run_test(
            "Get All Courses",
            "GET",
            "courses",
            200
        )

    def test_get_course_by_id(self, course_id):
        """Test retrieving a specific course by ID"""
        return self.run_test(
            "Get Course by ID",
            "GET",
            f"courses/{course_id}",
            200
        )

    def test_invalid_youtube_url(self):
        """Test with an invalid YouTube URL"""
        return self.run_test(
            "Invalid YouTube URL",
            "POST",
            "convert-youtube",
            400,
            data={"video_url": "https://example.com/not-a-youtube-url"}
        )

def main():
    # Setup
    tester = YouTubeCourseGeneratorTester()
    test_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("=" * 50)
    print("YouTube Course Generator API Test Suite")
    print("=" * 50)
    
    # Test root endpoint
    tester.test_root_endpoint()
    
    # Test getting all courses (before adding a new one)
    success, courses_before = tester.test_get_all_courses()
    initial_course_count = len(courses_before) if success and courses_before else 0
    print(f"Initial course count: {initial_course_count}")
    
    # Test converting a YouTube URL to a course
    success, course_data = tester.test_convert_youtube(test_video_url)
    
    # If we successfully created a course, test getting it by ID
    if success and course_data and 'id' in course_data:
        course_id = course_data['id']
        print(f"Created course with ID: {course_id}")
        
        # Test getting the specific course
        tester.test_get_course_by_id(course_id)
        
        # Test getting all courses again (should include the new one)
        success, courses_after = tester.test_get_all_courses()
        if success and courses_after:
            new_course_count = len(courses_after)
            if new_course_count > initial_course_count:
                print(f"✅ Course count increased from {initial_course_count} to {new_course_count}")
            else:
                print(f"⚠️ Course count did not increase as expected")
    
    # Test with an invalid YouTube URL
    tester.test_invalid_youtube_url()
    
    # Print results
    print("\n" + "=" * 50)
    print(f"📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    print("=" * 50)
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())