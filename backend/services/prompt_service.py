
"""
backend/services/prompt_service.py
Prompt engineering and management service
"""

import logging
from typing import Dict, List, Any
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class PromptService:
    """Service for prompt engineering and management"""
    
    def __init__(self):
        self.prompt_templates = self._load_templates()
        self.prompt_history = []
    
    def _load_templates(self) -> Dict[str, str]:
        """Load prompt templates"""
        return {
            'summarization': 'Summarize the following text in {length} sentences:\n\n{text}',
            'translation': 'Translate the following text from {source} to {target}:\n\n{text}',
            'analysis': 'Analyze the following content and provide insights:\n\n{content}',
            'code_review': 'Review the following code and provide feedback:\n\n{code}',
            'creative_writing': 'Write a {type} about {topic} in a {tone} tone.',
        }
    
    def build_prompt(self, template_name: str, **kwargs) -> str:
        """Build prompt from template"""
        if template_name not in self.prompt_templates:
            raise ValueError(f'Template {template_name} not found')
        
        template = self.prompt_templates[template_name]
        return template.format(**kwargs)
    
    def chain_prompts(self, prompts: List[Dict[str, Any]]) -> List[str]:
        """Chain multiple prompts together"""
        chained = []
        context = ""
        
        for prompt_config in prompts:
            prompt_type = prompt_config.get('type')
            params = prompt_config.get('params', {})
            
            if context:
                params['context'] = context
            
            prompt = self.build_prompt(prompt_type, **params)
            chained.append(prompt)
            
            context = f"Previous: {prompt[:100]}..."
        
        return chained
    
    def save_prompt(self, prompt: str, metadata: Dict[str, Any]) -> str:
        """Save prompt to history"""
        prompt_id = f"prompt_{len(self.prompt_history)}"
        
        self.prompt_history.append({
            'id': prompt_id,
            'prompt': prompt,
            'metadata': metadata
        })
        
        logger.info(f'Prompt saved: {prompt_id}')
        return prompt_id
    
    def get_prompt_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get prompt history"""
        return self.prompt_history[-limit:]


