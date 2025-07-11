import requests
import os
import logging
import time
from datetime import datetime, timedelta

class FaceAnalyzer:
    def __init__(self):
        self.api_key = os.environ.get('FACEPP_API_KEY')
        self.api_secret = os.environ.get('FACEPP_API_SECRET')
        self.detect_url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
        self.skin_analyze_url = 'https://api-us.faceplusplus.com/facepp/v1/skinanalyze'
        self.last_request_time = None
        self.min_request_interval = 2  # 2 seconds between requests
        
    def analyze_skin(self, image_path_or_url):
        """
        Analyze skin using Face++ API
        Returns analysis results including skin type, age, and concerns
        """
        if not self.api_key or not self.api_secret:
            logging.error("Face++ API credentials not found")
            return self._get_fallback_analysis()
            
        try:
            # Rate limiting to prevent API errors
            self._handle_rate_limiting()
            
            # Try Skin Analyze API first for detailed analysis
            result = self._try_skin_analyze_api(image_path_or_url)
            if result and result.get('success', False):
                return result
            
            # If Skin Analyze fails, use detect API as fallback
            logging.info("Skin Analyze API unavailable, using detect API")
            return self._try_detect_api_fallback(image_path_or_url)
                
        except Exception as e:
            logging.error(f"Error in skin analysis: {str(e)}")
            return self._get_fallback_analysis()
    
    def _handle_rate_limiting(self):
        """Handle rate limiting to prevent API errors"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_request_interval:
                sleep_time = self.min_request_interval - elapsed
                logging.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _try_skin_analyze_api(self, image_path_or_url):
        """Try the Face++ Skin Analyze API v1"""
        try:
            analyze_data = {
                'api_key': self.api_key,
                'api_secret': self.api_secret
            }
            
            response = None
            if image_path_or_url.startswith('http'):
                analyze_data['image_url'] = image_path_or_url
                response = requests.post(self.skin_analyze_url, data=analyze_data, timeout=10)
            else:
                with open(image_path_or_url, 'rb') as image_file:
                    files = {'image_file': image_file}
                    response = requests.post(self.skin_analyze_url, data=analyze_data, files=files, timeout=10)
            
            if response and response.status_code == 200:
                result = response.json()
                logging.info(f"Face++ Skin Analyze API successful")
                return self._process_skin_analysis_result(result)
            else:
                error_msg = response.text if response else "No response"
                logging.warning(f"Skin Analyze API failed: {response.status_code if response else 'No response'} - {error_msg}")
                return None
                
        except Exception as e:
            logging.warning(f"Skin Analyze API exception: {str(e)}")
            return None
    
    def _process_skin_analysis_result(self, api_result):
        """Process Face++ Skin Analyze API v1 result into our format"""
        if not api_result.get('result'):
            return self._get_fallback_analysis()
        
        result = api_result['result']
        
        # Extract detailed skin analysis from v1 API
        skin_type_data = result.get('skin_type', {})
        
        # Determine skin type from the API response
        if isinstance(skin_type_data, dict) and 'skin_type' in skin_type_data:
            skin_type_value = skin_type_data['skin_type']
            skin_type = self._map_skin_type_number(skin_type_value)
        else:
            skin_type = 'normal'
        
        # Extract age estimate (fallback to 25 if not available)
        skin_age = 25
        
        # Identify skin concerns from the detailed analysis
        concerns = self._identify_concerns_from_analysis(result)
        
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
        
        # Find skin type with highest score
        max_score = 0
        skin_type = 'normal'
        for stype, score in scores.items():
            if score > max_score:
                max_score = score
                skin_type = stype
        
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
    
    def _map_skin_type_number(self, skin_type_value):
        """Map Face++ skin type number to readable type"""
        skin_type_map = {
            0: 'dry',
            1: 'oily', 
            2: 'normal',
            3: 'combination'
        }
        return skin_type_map.get(skin_type_value, 'normal')
    
    def _identify_concerns_from_analysis(self, result):
        """Identify skin concerns from Face++ Skin Analyze API v1 detailed results"""
        concerns = []
        
        # Check specific skin issues from the detailed analysis
        if result.get('acne', {}).get('value', 0) > 0:
            concerns.append('acne')
        if result.get('blackhead', {}).get('value', 0) > 0:
            concerns.append('blackheads')
        if result.get('dark_circle', {}).get('value', 0) > 0:
            concerns.append('dark_circles')
        if result.get('skin_spot', {}).get('value', 0) > 0:
            concerns.append('dark_spots')
        if result.get('forehead_wrinkle', {}).get('value', 0) > 0 or result.get('eye_finelines', {}).get('value', 0) > 0:
            concerns.append('wrinkles')
        if result.get('pores_left_cheek', {}).get('value', 0) > 0 or result.get('pores_right_cheek', {}).get('value', 0) > 0:
            concerns.append('large_pores')
        
        return concerns if concerns else ['healthy_skin']
    
    def _try_detect_api_fallback(self, image_path_or_url):
        """Fallback to basic detect API when Skin Analyze API fails"""
        try:
            logging.info("Using Face++ detect API as fallback")
            detect_data = {
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'return_attributes': 'age,gender,skinstatus,beauty'
            }
            
            response = None
            if image_path_or_url.startswith('http'):
                detect_data['image_url'] = image_path_or_url
                response = requests.post(self.detect_url, data=detect_data)
            else:
                with open(image_path_or_url, 'rb') as image_file:
                    files = {'image_file': image_file}
                    response = requests.post(self.detect_url, data=detect_data, files=files)
            
            if response and response.status_code == 200:
                result = response.json()
                logging.info(f"Face++ detect API fallback response: {result}")
                return self._process_analysis_result(result)
            else:
                logging.error(f"Detect API fallback also failed: {response.status_code if response else 'No response'}")
                return self._get_fallback_analysis()
                
        except Exception as e:
            logging.error(f"Error in detect API fallback: {str(e)}")
            return self._get_fallback_analysis()
    
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
