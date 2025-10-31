// ============================================
// frontend/static/js/api_client.js
// API client for backend communication
// ============================================

class APIClient {
    constructor() {
        this.baseURL = window.location.origin;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }

    async request(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: this.headers
        };

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, options);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // Chrome AI APIs
    async promptAPI(prompt, temperature = 0.7, maxTokens = 500) {
        return this.request('/api/chrome-ai/prompt', 'POST', {
            prompt,
            temperature,
            max_tokens: maxTokens
        });
    }

    async summarizeAPI(text, type = 'tldr', length = 'medium') {
        return this.request('/api/chrome-ai/summarize', 'POST', {
            text,
            type,
            length
        });
    }

    async translateAPI(text, targetLanguage, sourceLanguage = 'auto') {
        return this.request('/api/chrome-ai/translate', 'POST', {
            text,
            target_language: targetLanguage,
            source_language: sourceLanguage
        });
    }

    async writeAPI(context, tone = 'professional', contentType = 'general') {
        return this.request('/api/chrome-ai/write', 'POST', {
            context,
            tone,
            content_type: contentType
        });
    }

    async proofreadAPI(text, checks = {}) {
        return this.request('/api/chrome-ai/proofread', 'POST', {
            text,
            check_grammar: checks.grammar !== false,
            check_spelling: checks.spelling !== false,
            check_style: checks.style !== false
        });
    }

    async rewriteAPI(text, goal = 'improve', tone = 'neutral') {
        return this.request('/api/chrome-ai/rewrite', 'POST', {
            text,
            goal,
            tone
        });
    }

    // Gemini Pro APIs
    async generateGemini(prompt, temperature = 0.7, maxTokens = 2048) {
        return this.request('/api/gemini/generate', 'POST', {
            prompt,
            temperature,
            max_tokens: maxTokens
        });
    }

    async analyzeDevOps(code, type) {
        return this.request('/api/gemini/analyze-devops', 'POST', {
            code,
            type
        });
    }

    async multiAgent(task, agents = ['analyst', 'writer', 'reviewer']) {
        return this.request('/api/gemini/multi-agent', 'POST', {
            task,
            agents
        });
    }

    // BigQuery APIs
    async optimizeSQL(query) {
        return this.request('/api/bigquery/optimize', 'POST', { query });
    }

    async getAnalytics() {
        return this.request('/api/bigquery/analytics', 'GET');
    }

    // Firebase APIs
    async saveData(collection, document, data) {
        return this.request('/api/firebase/data/save', 'POST', {
            collection,
            document,
            data
        });
    }

    async getData(collection, document) {
        return this.request('/api/firebase/data/get', 'POST', {
            collection,
            document
        });
    }

    // Health check
    async healthCheck() {
        return this.request('/health', 'GET');
    }
}

// Create global API client instance
const apiClient = new APIClient();


