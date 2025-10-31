"""
backend/services/summarizer_service.py
Text summarization service
"""


class SummarizerService:
    """Service for text summarization"""
    
    def __init__(self):
        self.summaries_cache = {}
    
    def summarize(self, text: str, length: str = 'medium') -> Dict[str, Any]:
        """Summarize text"""
        
        # Calculate target length
        length_map = {
            'short': 2,
            'medium': 5,
            'long': 10
        }
        target_sentences = length_map.get(length, 5)
        
        # Create summarization config
        config = {
            'original_length': len(text),
            'target_sentences': target_sentences,
            'compression_ratio': 0.3 if length == 'short' else 0.5 if length == 'medium' else 0.7
        }
        
        logger.info(f'Summarization request: {config["original_length"]} chars -> {target_sentences} sentences')
        
        return {
            'config': config,
            'processing': 'on-device',
            'cache_key': hash(text)
        }
    
    def extract_key_points(self, text: str, num_points: int = 5) -> List[str]:
        """Extract key points from text"""
        sentences = text.split('.')
        
        # Simple extraction (would use AI in production)
        key_points = []
        for sentence in sentences[:num_points]:
            if len(sentence.strip()) > 20:
                key_points.append(sentence.strip())
        
        return key_points
    
    def generate_headline(self, text: str) -> str:
        """Generate headline from text"""
        words = text.split()[:10]
        headline = ' '.join(words)
        return headline if len(headline) > 0 else 'Untitled'


