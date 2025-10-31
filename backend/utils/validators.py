"""
backend/utils/validators.py
Request validation utilities
"""

from typing import Dict, Any, List
from flask import Request


def validate_request(request: Request, required_fields: List[str]) -> tuple[bool, str]:
    """Validate request has required fields"""
    
    data = request.get_json()
    
    if not data:
        return False, 'Request body is required'
    
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f'Missing required fields: {", ".join(missing_fields)}'
    
    return True, 'Valid'


def validate_sql_query(query: str) -> tuple[bool, str]:
    """Validate SQL query"""
    
    if not query or len(query.strip()) == 0:
        return False, 'Query cannot be empty'
    
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER']
    query_upper = query.upper()
    
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False, f'Dangerous keyword detected: {keyword}'
    
    return True, 'Valid'


def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    
    if not api_key or len(api_key) < 20:
        return False
    
    return True