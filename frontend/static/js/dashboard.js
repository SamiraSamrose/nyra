// ============================================
// frontend/static/js/dashboard.js
// Dashboard specific functionality
// ============================================

const DASHBOARD_API = window.location.origin;

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/dashboard') {
        initializeDashboard();
    } else if (window.location.pathname === '/analytics') {
        initializeAnalytics();
    }
});

// Initialize dashboard
function initializeDashboard() {
    console.log('Dashboard initializing...');
    
    // Update metrics
    updateDashboardMetrics();
    setInterval(updateDashboardMetrics, 10000);
    
    // Initialize charts if Chart.js is available
    if (typeof Chart !== 'undefined') {
        initializeOperationsChart();
        initializeDistributionChart();
        initializeAPIUsageChart();
    }
    
    // Update activity feed
    updateActivityFeed();
    setInterval(updateActivityFeed, 15000);
}

// Update dashboard metrics
function updateDashboardMetrics() {
    const metrics = {
        onDeviceOps: Math.floor(850 + Math.random() * 20),
        avgLatency: (0.6 + Math.random() * 0.15).toFixed(2) + 's',
        privacyScore: '98%',
        hybridSync: Math.floor(320 + Math.random() * 10)
    };
    
    const elements = {
        onDeviceOps: document.getElementById('onDeviceOps'),
        avgLatency: document.getElementById('avgLatency'),
        privacyScore: document.getElementById('privacyScore'),
        hybridSync: document.getElementById('hybridSync')
    };
    
    if (elements.onDeviceOps) elements.onDeviceOps.textContent = metrics.onDeviceOps;
    if (elements.avgLatency) elements.avgLatency.textContent = metrics.avgLatency;
    if (elements.privacyScore) elements.privacyScore.textContent = metrics.privacyScore;
    if (elements.hybridSync) elements.hybridSync.textContent = metrics.hybridSync;
}

// Initialize operations chart
function initializeOperationsChart() {
    const canvas = document.getElementById('operationsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
            datasets: [{
                label: 'On-Device (Nano)',
                data: [45, 52, 68, 82, 95, 88, 76],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Cloud (Pro)',
                data: [15, 18, 22, 28, 32, 29, 25],
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: { padding: 10, font: { size: 12 } }
                },
                title: { display: false }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { color: '#e2e8f0' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// Initialize distribution chart
function initializeDistributionChart() {
    const canvas = document.getElementById('distributionChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['On-Device', 'Cloud', 'Hybrid'],
            datasets: [{
                data: [65, 25, 10],
                backgroundColor: ['#3b82f6', '#8b5cf6', '#10b981'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { 
                    position: 'bottom',
                    labels: { padding: 10, font: { size: 12 } }
                }
            }
        }
    });
}

// Initialize API usage chart
function initializeAPIUsageChart() {
    const canvas = document.getElementById('apiUsageChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Prompt', 'Summarizer', 'Translator', 'Writer', 'Proofreader', 'Rewriter'],
            datasets: [{
                label: 'API Calls',
                data: [245, 189, 156, 123, 98, 87],
                backgroundColor: [
                    '#3b82f6', '#10b981', '#f59e0b', 
                    '#8b5cf6', '#ef4444', '#06b6d4'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { color: '#e2e8f0' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// Update activity feed
function updateActivityFeed() {
    const feed = document.getElementById('activityFeed');
    if (!feed) return;
    
    const activities = [
        { type: 'nano', title: 'Prompt API - On-device processing', time: getRandomTime() },
        { type: 'pro', title: 'DevOps Analyzer - Cloud enhancement', time: getRandomTime() },
        { type: 'nano', title: 'Translator - Offline translation', time: getRandomTime() },
        { type: 'hybrid', title: 'Multi-Agent Task - Hybrid processing', time: getRandomTime() },
        { type: 'nano', title: 'Summarizer - Local summarization', time: getRandomTime() }
    ];
    
    feed.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-dot ${activity.type}"></div>
            <div class="activity-content">
                <div class="activity-title">${activity.title}</div>
                <div class="activity-time">${activity.time}</div>
            </div>
        </div>
    `).join('');
}

// Get random time
function getRandomTime() {
    const minutes = Math.floor(Math.random() * 60) + 1;
    return minutes < 60 ? `${minutes} minutes ago` : '1 hour ago';
}


