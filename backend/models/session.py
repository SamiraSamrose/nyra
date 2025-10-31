# ============================================
# backend/models/session.py
# ============================================
from datetime import datetime
import uuid

class Session:
    """Session model"""
    
    def __init__(self, user_id, session_id=None, created_at=None):
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.last_activity = datetime.utcnow()
    
    def to_dict(self):
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat()
        }
    
    @staticmethod
    def from_dict(data):
        session = Session(
            user_id=data.get('user_id'),
            session_id=data.get('session_id'),
            created_at=datetime.fromisoformat(data.get('created_at'))
        )
        session.last_activity = datetime.fromisoformat(data.get('last_activity'))
        return session


