import requests
import os
import logging

class FaceAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get('FACEPLUS_API_KEY')
        self.api_secret = os.environ.get('FACEPLUS_API_SECRET')
        self.detect_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
        self.analyze_url = 'https://api-us.faceplusplus.com/facepp/v3/face/analyze'
        
    def analyze_skin(self, image_path_or_url):
        """
        Analyze skin using Face++ API
        Returns analysis results including skin type, age, and concerns
        """
        if not self.api_key or not self.api_secret:
            logging.error("Face++ API credentials not found")
            return self._get_fallback_analysis()
            
        try:
            # First, detect face in the image
            detect_data = {
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'return_attributes': 'age,gender,skinstatus,beauty'
            }
            
            # Check if it's a URL or file path
            if image_path_or_url.startswith('http'):
                detect_data['image_url'] = image_path_or_url
            else:
                with open(image_path_or_url, 'rb') as image_file:
                    files = {'image_file': image_file}
                    response = requests.post(self.detect_url, data=detect_data, files=files)
            
            if image_path_or_url.startswith('http'):
                response = requests.post(self.detect_url, data=detect_data)
            
            if response.status_code == 200:
                result = response.json()
                return self._process_analysis_result(result)
            else:
                logging.error(f"Face++ API error: {response.status_code} - {response.text}")
                return self._get_fallback_analysis()
                
        except Exception as e:
            logging.error(f"Error in skin analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def _process_analysis_result(self, api_result):
        """Process Face++ API result into our format"""
        if not api_result.get('faces'):
            return self._get_fallback_analysis()
        
        face = api_result['faces'][0]
        attributes = face.get('attributes', {})
        
        # Extract skin status
        skin_status = attributes.get('skinstatus', {})
        age = attributes.get('age', {}).get('value', 25)
        gender = attributes.get('gender', {}).get('value', 'Female')
        
        # Determine skin type based on analysis
        skin_type = self._determine_skin_type(skin_status)
        
        # Identify skin concerns
        concerns = self._identify_concerns(skin_status)
        
        # Generate skincare routine recommendations
        routine = self._generate_routine(skin_type, concerns, age)
        
        return {
            'success': True,
            'skin_type': skin_type,
            'age': age,
            'gender': gender,
            'concerns': concerns,
            'skin_status': skin_status,
            'recommended_routine': routine,
            'confidence': face.get('face_rectangle', {})
        }
    
    def _determine_skin_type(self, skin_status):
        """Determine skin type from Face++ skin status"""
        if not skin_status:
            return 'normal'
        
        # Face++ provides various skin metrics
        health = skin_status.get('health', 50)
        stain = skin_status.get('stain', 50)
        acne = skin_status.get('acne', 50)
        
        if health > 70:
            return 'normal'
        elif acne > 60:
            return 'oily'
        elif stain > 60:
            return 'combination'
        else:
            return 'sensitive'
    
    def _identify_concerns(self, skin_status):
        """Identify skin concerns from analysis"""
        concerns = []
        
        if not skin_status:
            return concerns
        
        # Check various skin issues
        if skin_status.get('acne', 0) > 50:
            concerns.append('acne')
        if skin_status.get('stain', 0) > 50:
            concerns.append('dark_spots')
        if skin_status.get('health', 100) < 60:
            concerns.append('dryness')
        
        return concerns
    
    def _generate_routine(self, skin_type, concerns, age):
        """Generate skincare routine based on analysis"""
        routine = {
            'morning': [],
            'evening': [],
            'weekly': []
        }
        
        # Basic routine for all skin types
        routine['morning'].extend([
            'Sữa rửa mặt nhẹ nhàng',
            'Toner cân bằng da',
            'Serum vitamin C',
            'Kem dưỡng ẩm',
            'Kem chống nắng SPF 30+'
        ])
        
        routine['evening'].extend([
            'Tẩy trang (nếu có makeup)',
            'Sữa rửa mặt',
            'Toner',
            'Serum phục hồi da',
            'Kem dưỡng ẩm ban đêm'
        ])
        
        # Specific recommendations based on skin type
        if skin_type == 'oily':
            routine['morning'][1] = 'Toner kiểm soát dầu'
            routine['evening'].insert(3, 'BHA/Salicylic Acid (2-3 lần/tuần)')
            
        elif skin_type == 'dry':
            routine['morning'].insert(3, 'Serum hyaluronic acid')
            routine['evening'].insert(3, 'Dầu dưỡng da')
            
        elif skin_type == 'sensitive':
            routine['morning'][2] = 'Serum niacinamide'
            routine['evening'][3] = 'Serum làm dịu da'
        
        # Additional treatments based on concerns
        if 'acne' in concerns:
            routine['evening'].append('Điều trị mụn spot treatment')
            
        if 'dark_spots' in concerns:
            routine['evening'].insert(3, 'Serum làm sáng da')
            
        if age > 30:
            routine['evening'].insert(3, 'Serum chống lão hóa/retinol')
            routine['weekly'].append('Mặt nạ chống lão hóa')
        
        return routine
    
    def _get_fallback_analysis(self):
        """Return fallback analysis when API is unavailable"""
        return {
            'success': False,
            'error': 'Không thể phân tích da lúc này. Vui lòng thử lại sau.',
            'skin_type': 'normal',
            'concerns': [],
            'recommended_routine': {
                'morning': [
                    'Sữa rửa mặt nhẹ nhàng',
                    'Toner cân bằng da',
                    'Kem dưỡng ẩm',
                    'Kem chống nắng SPF 30+'
                ],
                'evening': [
                    'Sữa rửa mặt',
                    'Toner',
                    'Kem dưỡng ẩm ban đêm'
                ],
                'weekly': [
                    'Tẩy da chết (1-2 lần/tuần)',
                    'Mặt nạ dưỡng ẩm'
                ]
            }
        }

# Initialize global analyzer instance
face_analyzer = FaceAnalyzer()
