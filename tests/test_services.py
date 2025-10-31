# ============================================
# tests/test_services.py
# ============================================
import unittest
from backend.utils.validators import validate_email, validate_sql_query

class TestServices(unittest.TestCase):
    """Service tests"""
    
    def test_email_validation(self):
        """Test email validation"""
        self.assertTrue(validate_email('test@example.com'))
        self.assertFalse(validate_email('invalid-email'))
    
    def test_sql_validation(self):
        """Test SQL validation"""
        valid, msg = validate_sql_query('SELECT * FROM users')
        self.assertTrue(valid)
        
        valid, msg = validate_sql_query('DROP TABLE users')
        self.assertFalse(valid)

if __name__ == '__main__':
    unittest.main()


