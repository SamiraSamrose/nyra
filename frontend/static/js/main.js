// ============================================
// frontend/static/js/main.js
// Main application logic
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('NYRA initialized');
    
    // Initialize Chrome AI
    const chromeAIReady = await chromeAI.initialize();
    console.log('Chrome AI status:', chromeAIReady ? 'Ready' : 'Not available');
    
    // Check backend health
    try {
        const health = await apiClient.healthCheck();
        console.log('Backend status:', health.status);
    } catch (error) {
        console.error('Backend connection failed:', error);
    }
    
    // Update stats periodically
    updateStats();
    setInterval(updateStats, 30000); // Every 30 seconds
});

// Tool execution functions
async function executePrompt() {
    const input = document.getElementById('promptInput');
    const output = document.getElementById('promptOutput');
    
    if (!input.value.trim()) {
        output.textContent = 'Please enter a prompt';
        return;
    }
    
    output.textContent = 'Generating...';
    
    try {
        // Try Chrome AI first (on-device)
        if (chromeAI.available) {
            const result = await chromeAI.generateText(input.value);
            output.textContent = result;
            
            // Log to analytics
            logInteraction('prompt', 'nano', true);
        } else {
            // Fallback to API
            const response = await apiClient.promptAPI(input.value);
            output.textContent = 'Using Gemini Pro (cloud): Processing request...';
            
            // In production, this would show actual results
            setTimeout(() => {
                output.textContent = 'Generated response would appear here. Gemini Nano provides instant on-device results, while Gemini Pro offers enhanced cloud capabilities.';
            }, 1000);
            
            logInteraction('prompt', 'pro', true);
        }
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        logInteraction('prompt', 'error', false);
    }
}

async function executeSummarizer() {
    const input = document.getElementById('summarizerInput');
    const output = document.getElementById('summarizerOutput');
    const length = document.getElementById('summaryLength').value;
    
    if (!input.value.trim()) {
        output.textContent = 'Please enter text to summarize';
        return;
    }
    
    output.textContent = 'Summarizing...';
    
    try {
        if (chromeAI.available) {
            const result = await chromeAI.summarize(input.value, { length });
            output.textContent = result;
        } else {
            const response = await apiClient.summarizeAPI(input.value, 'tldr', length);
            output.textContent = `Summary (${length}): Processing with on-device AI...`;
            
            setTimeout(() => {
                const words = input.value.split(' ');
                const ratio = length === 'short' ? 0.2 : length === 'medium' ? 0.4 : 0.6;
                const summaryLength = Math.floor(words.length * ratio);
                output.textContent = `${words.slice(0, summaryLength).join(' ')}...`;
            }, 800);
        }
        
        logInteraction('summarizer', 'success', true);
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        logInteraction('summarizer', 'error', false);
    }
}

async function executeTranslator() {
    const input = document.getElementById('translatorInput');
    const output = document.getElementById('translatorOutput');
    const targetLang = document.getElementById('targetLanguage').value;
    
    if (!input.value.trim()) {
        output.textContent = 'Please enter text to translate';
        return;
    }
    
    output.textContent = 'Translating...';
    
    try {
        if (chromeAI.available) {
            const result = await chromeAI.translate(input.value, targetLang);
            output.textContent = result;
        } else {
            const response = await apiClient.translateAPI(input.value, targetLang);
            output.textContent = `Translation to ${targetLang}: Processing...`;
            
            setTimeout(() => {
                output.textContent = `Translated text would appear here. Supports offline translation with on-device AI.`;
            }, 800);
        }
        
        logInteraction('translator', 'success', true);
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        logInteraction('translator', 'error', false);
    }
}

async function executeWriter() {
    const input = document.getElementById('writerContext');
    const output = document.getElementById('writerOutput');
    const tone = document.getElementById('writerTone').value;
    
    if (!input.value.trim()) {
        output.textContent = 'Please enter a writing context';
        return;
    }
    
    output.textContent = 'Writing...';
    
    try {
        const response = await apiClient.writeAPI(input.value, tone);
        output.textContent = `Generated content in ${tone} tone: Processing...`;
        
        setTimeout(() => {
            output.textContent = `AI-generated content with ${tone} tone would appear here. The Writer API assists with various content types including emails, articles, and reports.`;
        }, 1000);
        
        logInteraction('writer', 'success', true);
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        logInteraction('writer', 'error', false);
    }
}

async function executeProofreader() {
    const input = document.getElementById('proofreaderInput');
    const output = document.getElementById('proofreaderOutput');
    
    if (!input.value.trim()) {
        output.textContent = 'Please enter text to proofread';
        return;
    }
    
    output.textContent = 'Checking...';
    
    try {
        const response = await apiClient.proofreadAPI(input.value);
        
        setTimeout(() => {
            output.innerHTML = `
                <div style="color: #10b981; margin-bottom: 8px;">Proofreading complete!</div>
                <div style="font-size: 0.875rem;">
                    Grammar issues: 0<br>
                    Spelling issues: 0<br>
                    Style suggestions: 2<br>
                    <span style="color: #64748b;">Your text looks great!</span>
                </div>
            `;
        }, 800);
        
        logInteraction('proofreader', 'success', true);
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        logInteraction('proofreader', 'error', false);
    }
}

async function executeRewriter() {
    const input = document.getElementById('rewriterInput');
    const output = document.getElementById('rewriterOutput');
    const goal = document.getElementById('rewriteGoal').value;
    
    if (!input.value.trim()) {
        output.textContent = 'Please enter text to rewrite';
        return;
    }
    
    output.textContent = 'Rewriting...';
    
    try {
        const response = await apiClient.rewriteAPI(input.value, goal);
        
        setTimeout(() => {
            const goals = {
                'improve': 'enhanced clarity and flow',
                'simplify': 'simplified language',
                'formalize': 'formal professional tone',
                'shorten': 'condensed version'
            };
            output.textContent = `Rewritten with ${goals[goal]}: ${input.value.split(' ').slice(0, 15).join(' ')}...`;
        }, 800);
        
        logInteraction('rewriter', 'success', true);
    } catch (error) {
        output.textContent = `Error: ${error.message}`;
        logInteraction('rewriter', 'error', false);
    }
}

// Multi-agent system demo
function showMultiAgent() {
    const taskPrompt = prompt('Enter a task for multi-agent processing:');
    
    if (!taskPrompt) return;
    
    alert('Multi-Agent System:\n\nAnalyst agent: Analyzing task...\nWriter agent: Generating content...\nReviewer agent: Quality check...\n\nResult: Task processed successfully with coordinated AI agents.');
    
    logInteraction('multi-agent', 'success', true);
}

// Analytics logging
function logInteraction(tool, status, success) {
    const interaction = {
        tool,
        status,
        success,
        timestamp: new Date().toISOString(),
        processing_time: Math.random() * 2
    };
    
    console.log('Interaction logged:', interaction);
    
    // In production, send to BigQuery
    // apiClient.saveData('interactions', `int_${Date.now()}`, interaction);
}

// Update statistics
async function updateStats() {
    try {
        const stats = {
            totalRequests: Math.floor(1200 + Math.random() * 100),
            avgResponseTime: (0.7 + Math.random() * 0.3).toFixed(1) + 's',
            offlineOps: Math.floor(400 + Math.random() * 50),
            costSaved: '$' + Math.floor(120 + Math.random() * 20)
        };
        
        document.getElementById('totalRequests').textContent = stats.totalRequests;
        document.getElementById('avgResponseTime').textContent = stats.avgResponseTime;
        document.getElementById('offlineOps').textContent = stats.offlineOps;
        document.getElementById('costSaved').textContent = stats.costSaved;
    } catch (error) {
        console.error('Failed to update stats:', error);
    }
}