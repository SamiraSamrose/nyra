# ============================================
# backend/models/user.py
# ============================================
from datetime import datetime

class User:
    """User model"""
    
    def __init__(self, uid, email, created_at=None):
        self.uid = uid
        self.email = email
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            'uid': self.uid,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        return User(
            uid=data.get('uid'),
            email=data.get('email'),
            created_at=datetime.fromisoformat(data.get('created_at'))
        )


