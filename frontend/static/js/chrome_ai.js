// ============================================
// frontend/static/js/chrome_ai.js
// Chrome AI integration for on-device processing
// ============================================

class ChromeAI {
    constructor() {
        this.available = this.checkAvailability();
        this.nano = null;
    }

    checkAvailability() {
        return typeof window.ai !== 'undefined';
    }

    async initialize() {
        if (!this.available) {
            console.warn('Chrome AI not available');
            return false;
        }

        try {
            if (window.ai && window.ai.canCreateTextSession) {
                const status = await window.ai.canCreateTextSession();
                this.nano = status === 'readily' ? window.ai : null;
                return this.nano !== null;
            }
            return false;
        } catch (error) {
            console.error('Chrome AI initialization failed:', error);
            return false;
        }
    }

    async generateText(prompt, options = {}) {
        if (!this.nano) {
            throw new Error('Chrome AI not initialized');
        }

        try {
            const session = await this.nano.createTextSession({
                temperature: options.temperature || 0.7,
                topK: options.topK || 40
            });

            const result = await session.prompt(prompt);
            session.destroy();
            
            return result;
        } catch (error) {
            console.error('Text generation failed:', error);
            throw error;
        }
    }

    async summarize(text, options = {}) {
        if (!window.ai || !window.ai.summarizer) {
            throw new Error('Summarizer API not available');
        }

        try {
            const summarizer = await window.ai.summarizer.create({
                type: options.type || 'tldr',
                length: options.length || 'medium'
            });

            const summary = await summarizer.summarize(text);
            summarizer.destroy();
            
            return summary;
        } catch (error) {
            console.error('Summarization failed:', error);
            throw error;
        }
    }

    async translate(text, targetLanguage, options = {}) {
        if (!window.ai || !window.ai.translator) {
            throw new Error('Translator API not available');
        }

        try {
            const translator = await window.ai.translator.create({
                sourceLanguage: options.sourceLanguage || 'auto',
                targetLanguage: targetLanguage
            });

            const translation = await translator.translate(text);
            translator.destroy();
            
            return translation;
        } catch (error) {
            console.error('Translation failed:', error);
            throw error;
        }
    }
}

// Create global Chrome AI instance
const chromeAI = new ChromeAI();


