import requests
import os
import logging

class FaceAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get('FACEPP_API_KEY')
        self.api_secret = os.environ.get('FACEPP_API_SECRET')
        self.detect_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
        self.skin_analyze_url = 'https://api-us.faceplusplus.com/facepp/v1/skinanalyze'
        
    def analyze_skin(self, image_path_or_url):
        """
        Analyze skin using Face++ API
        Returns analysis results including skin type, age, and concerns
        """
        if not self.api_key or not self.api_secret:
            logging.error("Face++ API credentials not found")
            return self._get_fallback_analysis()
            
        try:
            # Use Face++ Skin Analyze API v1 for detailed skin analysis
            analyze_data = {
                'api_key': self.api_key,
                'api_secret': self.api_secret
            }
            
            response = None
            # Check if it's a URL or file path
            if image_path_or_url.startswith('http'):
                analyze_data['image_url'] = image_path_or_url
                response = requests.post(self.skin_analyze_url, data=analyze_data)
            else:
                # For file uploads
                with open(image_path_or_url, 'rb') as image_file:
                    files = {'image_file': image_file}
                    response = requests.post(self.skin_analyze_url, data=analyze_data, files=files)
            
            if response and response.status_code == 200:
                result = response.json()
                logging.info(f"Face++ Skin Analyze API response: {result}")
                return self._process_skin_analysis_result(result)
            else:
                error_msg = response.text if response else "No response"
                logging.error(f"Face++ Skin Analyze API error: {response.status_code if response else 'No response'} - {error_msg}")
                return self._get_fallback_analysis()
                
        except Exception as e:
            logging.error(f"Error in skin analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def _process_skin_analysis_result(self, api_result):
        """Process Face++ Skin Analyze API v1 result into our format"""
        if not api_result.get('result'):
            return self._get_fallback_analysis()
        
        result = api_result['result']
        
        # Extract detailed skin analysis from v1 API
        skin_type_data = result.get('skin_type', {})
        skin_problems = result.get('skin_problem', {})
        skin_age = result.get('skin_age', {}).get('value', 25)
        
        # Handle the nested structure of skin_type
        skin_type_score = skin_type_data.get('skin_type', {}) if 'skin_type' in skin_type_data else skin_type_data
        
        # Determine skin type from detailed analysis
        skin_type = self._determine_skin_type_v1(skin_type_score)
        
        # Identify skin concerns from detailed problems analysis
        concerns = self._identify_concerns_v1(skin_problems)
        
        # Generate skincare routine recommendations
        routine = self._generate_routine(skin_type, concerns, skin_age)
        
        return {
            'success': True,
            'skin_type': skin_type,
            'age': skin_age,
            'concerns': concerns,
            'skin_analysis': result,
            'recommended_routine': routine,
            'confidence': api_result.get('confidence', 0.8)
        }
    
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
    
    def _determine_skin_type_v1(self, skin_type_score):
        """Determine skin type from Face++ Skin Analyze API v1"""
        if not skin_type_score:
            return 'normal'
        
        # Face++ v1 provides detailed skin type scores
        oily_score = skin_type_score.get('oily', 0)
        dry_score = skin_type_score.get('dry', 0)
        neutral_score = skin_type_score.get('neutral', 0)
        
        # Find the highest scoring skin type
        scores = {
            'oily': oily_score,
            'dry': dry_score,
            'normal': neutral_score
        }
        
        skin_type = max(scores.keys(), key=lambda k: scores[k])
        
        # If scores are close, classify as combination
        if abs(oily_score - dry_score) < 20 and max(oily_score, dry_score) > neutral_score:
            return 'combination'
        
        return skin_type
    
    def _identify_concerns_v1(self, skin_problems):
        """Identify skin concerns from Face++ Skin Analyze API v1"""
        concerns = []
        
        if not skin_problems:
            return concerns
        
        # Face++ v1 provides detailed problem analysis
        acne_score = skin_problems.get('acne_spot', {}).get('value', 0)
        blackhead_score = skin_problems.get('blackhead', {}).get('value', 0)
        wrinkle_score = skin_problems.get('wrinkle', {}).get('value', 0)
        stain_score = skin_problems.get('stain', {}).get('value', 0)
        dark_circle_score = skin_problems.get('dark_circle', {}).get('value', 0)
        
        # Threshold for concern identification
        threshold = 30
        
        if acne_score > threshold:
            concerns.append('acne')
        if blackhead_score > threshold:
            concerns.append('blackheads')
        if wrinkle_score > threshold:
            concerns.append('wrinkles')
        if stain_score > threshold:
            concerns.append('dark_spots')
        if dark_circle_score > threshold:
            concerns.append('dark_circles')
        
        return concerns
    
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
