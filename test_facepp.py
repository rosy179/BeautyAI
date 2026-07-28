import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('FACEPP_API_KEY')
api_secret = os.environ.get('FACEPP_API_SECRET')
# You can use a sample cloudinary image url here if needed, or just a public image
image_url = 'https://res.cloudinary.com/desbm8hos/image/upload/v1715174548/beauty_ai/sample_face.jpg' # I'll use a dummy URL or let it fail just to see the error format. Actually I need a real face URL.
image_url = 'https://raw.githubusercontent.com/computervisioneng/face-attendance-system/master/data/elon_musk/1.jpg'
print(f"Testing with public URL: {image_url}")

print(f"Using API Key: {api_key[:5]}...")

detect_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
skin_analyze_url = 'https://api-us.faceplusplus.com/facepp/v1/skinanalyze'

# Test Detect API
data = {
    'api_key': api_key,
    'api_secret': api_secret,
    'image_url': image_url,
    'return_attributes': 'age,gender'
}
print("Testing Detect API...")
res = requests.post(detect_url, data=data)
print(res.status_code)
print(res.text)

# Test Skin Analyze API
print("\nTesting Skin Analyze API...")
res2 = requests.post(skin_analyze_url, data=data)
print(res2.status_code)
print(res2.text)
