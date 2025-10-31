# File: backend/api/chrome_ai.py
#Chrome AI API endpoints
#Handles Prompt, Summarizer, Translator, Writer, Proofreader, Rewriter APIs

import logging
from flask import Blueprint, request, jsonify
from typing import Dict, Any

from backend.utils.validators import validate_request
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create blueprint
chrome_ai_bp = Blueprint('chrome_ai', __name__)


# Prompt API endpoint
@chrome_ai_bp.route('/prompt', methods=['POST'])
def generate_prompt():
    """
    Generate text using Chrome Prompt API
    Supports on-device Gemini Nano processing
    """
    try:
        data = request.get_json()
        
        # Validate request
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt_text = data['prompt']
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 500)
        
        # Log request
        logger.info(f'Prompt API request: {len(prompt_text)} chars')
        
        # Response structure for client-side Chrome AI
        response = {
            'type': 'chrome_ai_prompt',
            'config': {
                'prompt': prompt_text,
                'temperature': temperature,
                'max_tokens': max_tokens,
                'use_nano': True
            },
            'metadata': {
                'model': 'gemini-nano',
                'processing': 'on-device',
                'privacy': 'local'
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Prompt API error: {str(e)}')
        return jsonify({'error': 'Prompt generation failed', 'details': str(e)}), 500


# Summarizer API endpoint
@chrome_ai_bp.route('/summarize', methods=['POST'])
def summarize_text():
    """
    Summarize text using Chrome Summarizer API
    On-device summarization with Gemini Nano
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text_content = data['text']
        summary_type = data.get('type', 'tldr')  # tldr, key-points, headline
        length = data.get('length', 'medium')  # short, medium, long
        
        logger.info(f'Summarizer API request: {len(text_content)} chars, type: {summary_type}')
        
        response = {
            'type': 'chrome_ai_summarizer',
            'config': {
                'text': text_content,
                'summary_type': summary_type,
                'length': length,
                'use_nano': True
            },
            'metadata': {
                'model': 'gemini-nano',
                'processing': 'on-device',
                'original_length': len(text_content)
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Summarizer API error: {str(e)}')
        return jsonify({'error': 'Summarization failed', 'details': str(e)}), 500


# Translator API endpoint
@chrome_ai_bp.route('/translate', methods=['POST'])
def translate_text():
    """
    Translate text using Chrome Translator API
    Supports offline translation with on-device models
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data or 'target_language' not in data:
            return jsonify({'error': 'Text and target_language are required'}), 400
        
        text_content = data['text']
        target_language = data['target_language']
        source_language = data.get('source_language', 'auto')
        
        logger.info(f'Translator API request: {source_language} -> {target_language}')
        
        response = {
            'type': 'chrome_ai_translator',
            'config': {
                'text': text_content,
                'source_language': source_language,
                'target_language': target_language,
                'use_nano': True
            },
            'metadata': {
                'model': 'gemini-nano',
                'processing': 'on-device',
                'offline_capable': True
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Translator API error: {str(e)}')
        return jsonify({'error': 'Translation failed', 'details': str(e)}), 500


# Writer API endpoint
@chrome_ai_bp.route('/write', methods=['POST'])
def write_content():
    """
    Generate written content using Chrome Writer API
    Creative writing with on-device AI assistance
    """
    try:
        data = request.get_json()
        
        if not data or 'context' not in data:
            return jsonify({'error': 'Context is required'}), 400
        
        context = data['context']
        tone = data.get('tone', 'professional')  # professional, casual, creative, technical
        length = data.get('length', 'medium')
        content_type = data.get('content_type', 'general')  # email, article, report
        
        logger.info(f'Writer API request: tone={tone}, type={content_type}')
        
        response = {
            'type': 'chrome_ai_writer',
            'config': {
                'context': context,
                'tone': tone,
                'length': length,
                'content_type': content_type,
                'use_nano': True
            },
            'metadata': {
                'model': 'gemini-nano',
                'processing': 'on-device',
                'privacy_mode': 'local'
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Writer API error: {str(e)}')
        return jsonify({'error': 'Content generation failed', 'details': str(e)}), 500


# Proofreader API endpoint
@chrome_ai_bp.route('/proofread', methods=['POST'])
def proofread_text():
    """
    Proofread and correct text using Chrome Proofreader API
    Grammar, spelling, and style checking
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text_content = data['text']
        check_grammar = data.get('check_grammar', True)
        check_spelling = data.get('check_spelling', True)
        check_style = data.get('check_style', True)
        
        logger.info(f'Proofreader API request: {len(text_content)} chars')
        
        response = {
            'type': 'chrome_ai_proofreader',
            'config': {
                'text': text_content,
                'check_grammar': check_grammar,
                'check_spelling': check_spelling,
                'check_style': check_style,
                'use_nano': True
            },
            'metadata': {
                'model': 'gemini-nano',
                'processing': 'on-device',
                'checks_enabled': {
                    'grammar': check_grammar,
                    'spelling': check_spelling,
                    'style': check_style
                }
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Proofreader API error: {str(e)}')
        return jsonify({'error': 'Proofreading failed', 'details': str(e)}), 500


# Rewriter API endpoint
@chrome_ai_bp.route('/rewrite', methods=['POST'])
def rewrite_text():
    """
    Rewrite text using Chrome Rewriter API
    Paraphrase, improve clarity, change tone
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text_content = data['text']
        rewrite_goal = data.get('goal', 'improve')  # improve, simplify, formalize, shorten
        target_tone = data.get('tone', 'neutral')
        
        logger.info(f'Rewriter API request: goal={rewrite_goal}')
        
        response = {
            'type': 'chrome_ai_rewriter',
            'config': {
                'text': text_content,
                'rewrite_goal': rewrite_goal,
                'target_tone': target_tone,
                'use_nano': True
            },
            'metadata': {
                'model': 'gemini-nano',
                'processing': 'on-device',
                'original_length': len(text_content)
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Rewriter API error: {str(e)}')
        return jsonify({'error': 'Rewriting failed', 'details': str(e)}), 500


# Batch processing endpoint
@chrome_ai_bp.route('/batch', methods=['POST'])
def batch_process():
    """
    Process multiple Chrome AI requests in batch
    Optimizes multi-operation workflows
    """
    try:
        data = request.get_json()
        
        if not data or 'operations' not in data:
            return jsonify({'error': 'Operations list is required'}), 400
        
        operations = data['operations']
        
        logger.info(f'Batch processing: {len(operations)} operations')
        
        results = []
        for op in operations:
            op_type = op.get('type')
            op_data = op.get('data', {})
            
            results.append({
                'type': op_type,
                'config': op_data,
                'use_nano': True
            })
        
        response = {
            'batch_id': f'batch_{len(operations)}',
            'operations': results,
            'metadata': {
                'total_operations': len(operations),
                'processing': 'on-device'
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Batch processing error: {str(e)}')
        return jsonify({'error': 'Batch processing failed', 'details': str(e)}), 500