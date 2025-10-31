# File: backend/app.py

#"""
#Main Flask application entry point
#Initializes all routes, services, and middleware
#"""

import os
import logging
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime

# Import configuration
from config.settings import settings

# Import API blueprints
from backend.api.chrome_ai import chrome_ai_bp
from backend.api.gemini import gemini_bp
from backend.api.firebase import firebase_bp
from backend.api.bigquery import bigquery_bp

# Import services
from backend.services.prompt_service import PromptService
from backend.services.summarizer_service import SummarizerService
from backend.services.translator_service import TranslatorService
from backend.services.writer_service import WriterService
from backend.services.proofreader_service import ProofreaderService
from backend.services.rewriter_service import RewriterService
from backend.services.sql_optimizer import SQLOptimizerService

# Import utilities
from backend.utils.logger import setup_logger
from backend.utils.validators import validate_request

# Initialize logger
logger = setup_logger(__name__)


def create_app():
    """Application factory pattern"""
    
    # Initialize Flask app
    app = Flask(
        __name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )
    
    # Configure app
    app.config['SECRET_KEY'] = settings.secret_key
    app.config['JSON_SORT_KEYS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size
    
    # Enable CORS
    CORS(app, origins=settings.cors_origins)
    
    # Register blueprints
    app.register_blueprint(chrome_ai_bp, url_prefix='/api/chrome-ai')
    app.register_blueprint(gemini_bp, url_prefix='/api/gemini')
    app.register_blueprint(firebase_bp, url_prefix='/api/firebase')
    app.register_blueprint(bigquery_bp, url_prefix='/api/bigquery')
    
    # Initialize services
    app.prompt_service = PromptService()
    app.summarizer_service = SummarizerService()
    app.translator_service = TranslatorService()
    app.writer_service = WriterService()
    app.proofreader_service = ProofreaderService()
    app.rewriter_service = RewriterService()
    app.sql_optimizer = SQLOptimizerService()
    
    # Root route - Main interface
    @app.route('/')
    def index():
        """Render main interface"""
        return render_template('index.html')
    
    # Dashboard route
    @app.route('/dashboard')
    def dashboard():
        """Render analytics dashboard"""
        return render_template('dashboard.html')
    
    # Analytics route
    @app.route('/analytics')
    def analytics():
        """Render analytics page"""
        return render_template('analytics.html')
    
    # Prompt Builder route
    @app.route('/prompt-builder')
    def prompt_builder():
        """Render prompt builder interface"""
        return render_template('prompt_builder.html')
    
    # SQL Optimizer route
    @app.route('/sql-optimizer')
    def sql_optimizer():
        """Render SQL optimizer tool"""
        return render_template('sql_optimizer.html')
    
    # DevOps Analyzer route
    @app.route('/devops-analyzer')
    def devops_analyzer():
        """Render DevOps analyzer"""
        return render_template('devops_analyzer.html')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """API health check"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'services': {
                'chrome_ai': 'available',
                'gemini_pro': 'available',
                'firebase': 'connected',
                'bigquery': 'connected'
            }
        })
    
    # API status endpoint
    @app.route('/api/status')
    def api_status():
        """Get API status and capabilities"""
        return jsonify({
            'apis': {
                'prompt': {'status': 'active', 'endpoint': '/api/chrome-ai/prompt'},
                'summarizer': {'status': 'active', 'endpoint': '/api/chrome-ai/summarize'},
                'translator': {'status': 'active', 'endpoint': '/api/chrome-ai/translate'},
                'writer': {'status': 'active', 'endpoint': '/api/chrome-ai/write'},
                'proofreader': {'status': 'active', 'endpoint': '/api/chrome-ai/proofread'},
                'rewriter': {'status': 'active', 'endpoint': '/api/chrome-ai/rewrite'},
                'gemini_pro': {'status': 'active', 'endpoint': '/api/gemini/generate'},
                'sql_optimizer': {'status': 'active', 'endpoint': '/api/bigquery/optimize'},
                'devops_analyzer': {'status': 'active', 'endpoint': '/api/gemini/analyze-devops'}
            },
            'features': {
                'offline_mode': True,
                'hybrid_ai': True,
                'multi_agent': True,
                'visualization': True
            }
        })
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        return jsonify({'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        return jsonify({'error': 'Not found', 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle internal server errors"""
        logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal server error', 'message': 'An error occurred'}), 500
    
    # Request logging middleware
    @app.before_request
    def log_request():
        """Log all incoming requests"""
        logger.info(f'{request.method} {request.path} - {request.remote_addr}')
    
    # Response headers middleware
    @app.after_request
    def add_security_headers(response):
        """Add security headers to responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    logger.info('NYRA application initialized successfully')
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    """Run the application"""
    logger.info(f'Starting NYRA on port {settings.port}')
    app.run(
        host='0.0.0.0',
        port=settings.port,
        debug=(settings.flask_env == 'development')
    )