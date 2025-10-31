#"""
#Firebase API endpoints - backend/api/firebase.py
#Authentication, Firestore database, and Firebase AI Extensions
#"""

import logging
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask import Blueprint, request, jsonify
from datetime import datetime

from config.settings import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize Firebase
try:
    cred = credentials.Certificate(settings.firebase_config_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info('Firebase initialized successfully')
except Exception as e:
    logger.error(f'Firebase initialization error: {str(e)}')
    db = None

# Create blueprint
firebase_bp = Blueprint('firebase', __name__)


# User authentication endpoint
@firebase_bp.route('/auth/verify', methods=['POST'])
def verify_token():
    """Verify Firebase authentication token"""
    try:
        data = request.get_json()
        
        if not data or 'id_token' not in data:
            return jsonify({'error': 'ID token is required'}), 400
        
        id_token = data['id_token']
        
        # Verify token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        
        logger.info(f'Token verified for user: {uid}')
        
        return jsonify({
            'verified': True,
            'uid': uid,
            'email': decoded_token.get('email'),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f'Token verification error: {str(e)}')
        return jsonify({'error': 'Token verification failed', 'details': str(e)}), 401


# Save user data endpoint
@firebase_bp.route('/data/save', methods=['POST'])
def save_data():
    """Save user data to Firestore"""
    try:
        if db is None:
            return jsonify({'error': 'Firestore not initialized'}), 500
        
        data = request.get_json()
        
        if not data or 'collection' not in data or 'document' not in data:
            return jsonify({'error': 'Collection and document are required'}), 400
        
        collection_name = data['collection']
        document_id = data['document']
        document_data = data.get('data', {})
        
        # Add timestamp
        document_data['updated_at'] = firestore.SERVER_TIMESTAMP
        
        # Save to Firestore
        doc_ref = db.collection(collection_name).document(document_id)
        doc_ref.set(document_data, merge=True)
        
        logger.info(f'Data saved: {collection_name}/{document_id}')
        
        return jsonify({
            'success': True,
            'collection': collection_name,
            'document': document_id,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f'Data save error: {str(e)}')
        return jsonify({'error': 'Data save failed', 'details': str(e)}), 500


# Retrieve user data endpoint
@firebase_bp.route('/data/get', methods=['POST'])
def get_data():
    """Retrieve user data from Firestore"""
    try:
        if db is None:
            return jsonify({'error': 'Firestore not initialized'}), 500
        
        data = request.get_json()
        
        if not data or 'collection' not in data or 'document' not in data:
            return jsonify({'error': 'Collection and document are required'}), 400
        
        collection_name = data['collection']
        document_id = data['document']
        
        # Retrieve from Firestore
        doc_ref = db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        
        if doc.exists:
            logger.info(f'Data retrieved: {collection_name}/{document_id}')
            return jsonify({
                'success': True,
                'data': doc.to_dict(),
                'document': document_id
            }), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
        
    except Exception as e:
        logger.error(f'Data retrieval error: {str(e)}')
        return jsonify({'error': 'Data retrieval failed', 'details': str(e)}), 500


# Query data endpoint
@firebase_bp.route('/data/query', methods=['POST'])
def query_data():
    """Query Firestore data with filters"""
    try:
        if db is None:
            return jsonify({'error': 'Firestore not initialized'}), 500
        
        data = request.get_json()
        
        if not data or 'collection' not in data:
            return jsonify({'error': 'Collection is required'}), 400
        
        collection_name = data['collection']
        filters = data.get('filters', [])
        limit = data.get('limit', 100)
        
        # Build query
        query = db.collection(collection_name)
        
        for f in filters:
            field = f.get('field')
            operator = f.get('operator', '==')
            value = f.get('value')
            query = query.where(field, operator, value)
        
        # Execute query
        results = query.limit(limit).stream()
        
        documents = []
        for doc in results:
            documents.append({
                'id': doc.id,
                'data': doc.to_dict()
            })
        
        logger.info(f'Query executed: {collection_name}, found {len(documents)} documents')
        
        return jsonify({
            'success': True,
            'collection': collection_name,
            'results': documents,
            'count': len(documents)
        }), 200
        
    except Exception as e:
        logger.error(f'Query error: {str(e)}')
        return jsonify({'error': 'Query failed', 'details': str(e)}), 500

