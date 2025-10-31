# ============================================
# tests/test_api.py
# ============================================
import unittest
import json
from backend.app import app

class TestAPI(unittest.TestCase):
    """API tests"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_check(self):
        """Test health endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_prompt_api(self):
        """Test prompt endpoint"""
        response = self.app.post('/api/chrome-ai/prompt',
            json={'prompt': 'Hello, world!'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_summarize_api(self):
        """Test summarize endpoint"""
        response = self.app.post('/api/chrome-ai/summarize',
            json={'text': 'This is a test text.', 'length': 'short'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()


