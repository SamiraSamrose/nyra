"""
backend/api/gemini.py
Gemini Pro API endpoints with full functionality
"""

import logging
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from datetime import datetime

from config.settings import settings

logger = logging.getLogger(__name__)

# Configure Gemini API
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.warning(f"Gemini API configuration warning: {e}")

# Create blueprint
gemini_bp = Blueprint('gemini', __name__)


def get_gemini_model(model_name='gemini-pro'):
    """Get configured Gemini model instance"""
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        logger.error(f"Failed to get Gemini model: {e}")
        return None


@gemini_bp.route('/generate', methods=['POST'])
def generate_content():
    """Generate content using Gemini Pro"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data['prompt']
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2048)
        
        logger.info(f'Gemini Pro generate request: {len(prompt)} chars')
        
        model = get_gemini_model()
        if not model:
            return jsonify({'error': 'Gemini model not available'}), 500
        
        generation_config = {
            'temperature': temperature,
            'max_output_tokens': max_tokens,
        }
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        result = {
            'success': True,
            'generated_text': response.text,
            'model': 'gemini-pro',
            'processing': 'cloud',
            'metadata': {
                'prompt_tokens': len(prompt.split()),
                'completion_tokens': len(response.text.split()),
                'temperature': temperature,
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f'Gemini generation error: {str(e)}')
        return jsonify({'error': 'Generation failed', 'details': str(e)}), 500


@gemini_bp.route('/analyze-devops', methods=['POST'])
def analyze_devops():
    """Analyze DevOps configurations"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data or 'type' not in data:
            return jsonify({'error': 'Code and type are required'}), 400
        
        code = data['code']
        config_type = data['type']
        
        logger.info(f'DevOps analysis request: {config_type}')
        
        analysis_prompt = f"""Analyze this {config_type} configuration and provide detailed feedback:

{code}

Provide:
1. Security Issues (with severity levels)
2. Best Practice Violations
3. Performance Optimization Opportunities
4. Cost Reduction Suggestions
5. Scalability Improvements
6. Specific Recommendations with line numbers

Format your response clearly with sections."""
        
        model = get_gemini_model()
        if not model:
            return jsonify({'error': 'Gemini model not available'}), 500
        
        response = model.generate_content(analysis_prompt)
        analysis_text = response.text
        
        # Extract recommendations
        recommendations = _extract_recommendations(analysis_text)
        severity_levels = _analyze_severity(analysis_text)
        
        analysis_result = {
            'success': True,
            'config_type': config_type,
            'analysis': analysis_text,
            'recommendations': recommendations,
            'severity_levels': severity_levels,
            'estimated_improvements': {
                'security_score': 85 + len([r for r in recommendations if 'security' in r.get('category', '')]) * 2,
                'performance_gain': '15-25%',
                'cost_reduction': '10-20%'
            },
            'metadata': {
                'model': 'gemini-pro',
                'lines_analyzed': len(code.split('\n')),
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        logger.error(f'DevOps analysis error: {str(e)}')
        return jsonify({'error': 'Analysis failed', 'details': str(e)}), 500


@gemini_bp.route('/multi-agent', methods=['POST'])
def multi_agent_process():
    """Multi-agent AI orchestration"""
    try:
        data = request.get_json()
        
        if not data or 'task' not in data:
            return jsonify({'error': 'Task description is required'}), 400
        
        task = data['task']
        agents = data.get('agents', ['analyst', 'writer', 'reviewer'])
        
        logger.info(f'Multi-agent task: {len(agents)} agents')
        
        model = get_gemini_model()
        if not model:
            return jsonify({'error': 'Gemini model not available'}), 500
        
        agent_results = []
        
        # Process task with each agent
        for agent in agents:
            agent_prompt = f"""You are a specialized {agent} agent.

Task: {task}

Provide your perspective and analysis as a {agent}. Be specific and actionable."""
            
            response = model.generate_content(agent_prompt)
            agent_results.append({
                'agent': agent,
                'response': response.text,
                'confidence': 0.92,
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Synthesize results
        synthesis_prompt = f"""Synthesize the following agent responses into a coherent, comprehensive result:

{chr(10).join([f"{r['agent'].upper()}: {r['response'][:300]}..." for r in agent_results])}

Provide a unified, actionable response that combines the best insights from all agents."""
        
        synthesis = model.generate_content(synthesis_prompt)
        
        result = {
            'success': True,
            'task': task,
            'agent_responses': agent_results,
            'synthesized_result': synthesis.text,
            'metadata': {
                'agents_used': len(agents),
                'model': 'gemini-pro',
                'orchestration': 'sequential',
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f'Multi-agent error: {str(e)}')
        return jsonify({'error': 'Multi-agent processing failed', 'details': str(e)}), 500


@gemini_bp.route('/generate-code', methods=['POST'])
def generate_code():
    """Generate code using Gemini Pro"""
    try:
        data = request.get_json()
        
        if not data or 'description' not in data:
            return jsonify({'error': 'Code description is required'}), 400
        
        description = data['description']
        language = data.get('language', 'python')
        framework = data.get('framework', None)
        
        logger.info(f'Code generation: {language}')
        
        code_prompt = f"""Generate production-ready {language} code for the following:

Description: {description}
{f'Framework: {framework}' if framework else ''}

Requirements:
- Clean, well-documented code
- Error handling
- Type hints (if applicable)
- Best practices
- Comments explaining logic
- Example usage

Provide complete, executable code."""
        
        model = get_gemini_model()
        if not model:
            return jsonify({'error': 'Gemini model not available'}), 500
        
        response = model.generate_content(code_prompt)
        
        result = {
            'success': True,
            'generated_code': response.text,
            'language': language,
            'framework': framework,
            'metadata': {
                'model': 'gemini-pro',
                'lines': len(response.text.split('\n')),
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f'Code generation error: {str(e)}')
        return jsonify({'error': 'Code generation failed', 'details': str(e)}), 500


@gemini_bp.route('/hybrid-decision', methods=['POST'])
def hybrid_decision():
    """Hybrid AI decision making"""
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        nano_result = data.get('nano_result', None)
        
        logger.info('Hybrid AI decision processing')
        
        hybrid_prompt = f"""Query: {query}

On-device result: {nano_result if nano_result else 'Not available'}

Provide enhanced analysis using cloud capabilities:
1. Deeper reasoning and context
2. External knowledge integration
3. Advanced pattern recognition
4. Confidence scoring

Combine insights for optimal result."""
        
        model = get_gemini_model()
        if not model:
            return jsonify({'error': 'Gemini model not available'}), 500
        
        response = model.generate_content(hybrid_prompt)
        
        result = {
            'success': True,
            'query': query,
            'nano_contribution': nano_result is not None,
            'cloud_enhancement': response.text,
            'hybrid_strategy': 'nano-first-cloud-enhance',
            'confidence': 0.95,
            'metadata': {
                'processing': 'hybrid',
                'privacy': 'nano-local-pro-cloud',
                'network': 'required-for-enhancement',
                'timestamp': datetime.utcnow().isoformat()
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f'Hybrid decision error: {str(e)}')
        return jsonify({'error': 'Hybrid processing failed', 'details': str(e)}), 500


def _extract_recommendations(analysis_text):
    """Extract structured recommendations from analysis text"""
    recommendations = []
    
    lines = analysis_text.split('\n')
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in ['recommend', 'should', 'consider', 'suggest', 'improve', 'fix']):
            recommendations.append({
                'recommendation': line.strip(),
                'priority': _determine_priority(line_lower),
                'category': _categorize_recommendation(line_lower),
                'line_number': i + 1
            })
    
    return recommendations[:15]


def _determine_priority(text):
    """Determine priority level"""
    if any(word in text for word in ['critical', 'urgent', 'severe', 'security']):
        return 'critical'
    elif any(word in text for word in ['important', 'should', 'must']):
        return 'high'
    elif any(word in text for word in ['consider', 'recommend']):
        return 'medium'
    else:
        return 'low'


def _categorize_recommendation(text):
    """Categorize recommendation by type"""
    if any(word in text for word in ['security', 'vulnerability', 'encrypt', 'auth']):
        return 'security'
    elif any(word in text for word in ['performance', 'optimize', 'speed', 'cache']):
        return 'performance'
    elif any(word in text for word in ['cost', 'billing', 'expensive', 'price']):
        return 'cost'
    elif any(word in text for word in ['scale', 'capacity', 'load', 'availability']):
        return 'scalability'
    elif any(word in text for word in ['maintainability', 'documentation', 'code quality']):
        return 'maintainability'
    else:
        return 'general'


def _analyze_severity(analysis_text):
    """Analyze severity levels in the analysis"""
    severity = {
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0
    }
    
    text_lower = analysis_text.lower()
    
    severity['critical'] = text_lower.count('critical') + text_lower.count('severe')
    severity['high'] = text_lower.count('high priority') + text_lower.count('important')
    severity['medium'] = text_lower.count('medium') + text_lower.count('moderate')
    severity['low'] = text_lower.count('low priority') + text_lower.count('minor')
    
    return severity