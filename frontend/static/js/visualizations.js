// ============================================
// frontend/static/js/visualizations.js
// Advanced visualizations for analytics
// ============================================

// Initialize analytics
function initializeAnalytics() {
    console.log('Analytics initializing...');
    
    if (typeof Chart !== 'undefined') {
        initializePerformanceChart();
        initializeCostChart();
        initializeEfficiencyRadar();
    }
    
    if (typeof d3 !== 'undefined') {
        initializeFlowDiagram();
        initializeHeatmap();
    }
    
    // Fetch real analytics data
    fetchAnalyticsData();
}

// Initialize performance chart
function initializePerformanceChart() {
    const canvas = document.getElementById('performanceChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Response Time (ms)',
                data: [650, 720, 680, 590, 640, 710, 675],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { 
                y: { 
                    beginAtZero: true,
                    grid: { color: '#e2e8f0' }
                }
            }
        }
    });
}

// Initialize cost chart
function initializeCostChart() {
    const canvas = document.getElementById('costChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'On-Device Savings',
                data: [285, 312, 298, 352],
                backgroundColor: '#10b981'
            }, {
                label: 'Cloud Costs',
                data: [18, 22, 21, 28],
                backgroundColor: '#ef4444'
            }]
        },
        options: {
            responsive: true,
            plugins: { 
                legend: { 
                    position: 'bottom',
                    labels: { padding: 10 }
                } 
            },
            scales: { 
                y: { 
                    beginAtZero: true,
                    stacked: false
                } 
            }
        }
    });
}

// Initialize efficiency radar
function initializeEfficiencyRadar() {
    const canvas = document.getElementById('efficiencyRadar');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Speed', 'Accuracy', 'Privacy', 'Cost', 'Offline'],
            datasets: [{
                label: 'NYRA Performance',
                data: [95, 98, 100, 92, 85],
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.2)',
                pointBackgroundColor: '#8b5cf6',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#8b5cf6'
            }]
        },
        options: {
            responsive: true,
            scales: { 
                r: { 
                    beginAtZero: true, 
                    max: 100,
                    ticks: { stepSize: 20 }
                } 
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// Initialize flow diagram with D3
function initializeFlowDiagram() {
    const container = document.getElementById('flowDiagram');
    if (!container || typeof d3 === 'undefined') return;
    
    // Clear existing
    container.innerHTML = '';
    
    const width = container.offsetWidth;
    const height = 300;
    
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
    
    const nodes = [
        { id: 1, x: width * 0.2, y: height / 2, label: 'User\nInput', color: '#3b82f6' },
        { id: 2, x: width * 0.45, y: height * 0.3, label: 'Gemini\nNano', color: '#10b981' },
        { id: 3, x: width * 0.45, y: height * 0.7, label: 'Gemini\nPro', color: '#8b5cf6' },
        { id: 4, x: width * 0.8, y: height / 2, label: 'Result', color: '#f59e0b' }
    ];
    
    const links = [
        { from: nodes[0], to: nodes[1] },
        { from: nodes[0], to: nodes[2] },
        { from: nodes[1], to: nodes[3] },
        { from: nodes[2], to: nodes[3] }
    ];
    
    // Draw links
    svg.selectAll('line')
        .data(links)
        .enter()
        .append('line')
        .attr('x1', d => d.from.x)
        .attr('y1', d => d.from.y)
        .attr('x2', d => d.to.x)
        .attr('y2', d => d.to.y)
        .attr('stroke', '#cbd5e1')
        .attr('stroke-width', 2);
    
    // Draw nodes
    svg.selectAll('circle')
        .data(nodes)
        .enter()
        .append('circle')
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)
        .attr('r', 35)
        .attr('fill', d => d.color)
        .attr('stroke', 'white')
        .attr('stroke-width', 3);
    
    // Draw labels
    svg.selectAll('text')
        .data(nodes)
        .enter()
        .append('text')
        .attr('x', d => d.x)
        .attr('y', d => d.y + 5)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('font-size', '12px')
        .attr('font-weight', '600')
        .each(function(d) {
            const lines = d.label.split('\n');
            const text = d3.select(this);
            lines.forEach((line, i) => {
                text.append('tspan')
                    .attr('x', d.x)
                    .attr('dy', i === 0 ? 0 : 14)
                    .text(line);
            });
        });
}

// Initialize heatmap with D3
function initializeHeatmap() {
    const container = document.getElementById('heatmap');
    if (!container || typeof d3 === 'undefined') return;
    
    // Clear existing
    container.innerHTML = '';
    
    const width = container.offsetWidth;
    const height = 200;
    
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
    
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const hours = 24;
    
    const cellWidth = width / hours;
    const cellHeight = height / days.length;
    
    const data = [];
    days.forEach((day, dayIdx) => {
        for (let hour = 0; hour < hours; hour++) {
            data.push({
                day: dayIdx,
                hour: hour,
                value: Math.random() * 100
            });
        }
    });
    
    // Color scale
    const colorScale = d3.scaleLinear()
        .domain([0, 100])
        .range(['#dbeafe', '#1e40af']);
    
    // Draw cells
    svg.selectAll('rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => d.hour * cellWidth)
        .attr('y', d => d.day * cellHeight)
        .attr('width', cellWidth - 1)
        .attr('height', cellHeight - 1)
        .attr('fill', d => colorScale(d.value))
        .attr('rx', 2);
    
    // Add day labels
    svg.selectAll('.day-label')
        .data(days)
        .enter()
        .append('text')
        .attr('x', -5)
        .attr('y', (d, i) => i * cellHeight + cellHeight / 2 + 5)
        .attr('text-anchor', 'end')
        .attr('font-size', '10px')
        .attr('fill', '#64748b')
        .text(d => d);
}

// Fetch analytics data from backend
async function fetchAnalyticsData() {
    try {
        const response = await fetch(`${DASHBOARD_API}/api/bigquery/analytics`);
        const data = await response.json();
        
        if (data.success && data.data) {
            console.log('Analytics data loaded:', data.data.length, 'records');
            // Update charts with real data if needed
        }
    } catch (error) {
        console.error('Failed to fetch analytics:', error);
    }
}

// Refresh analytics
function refreshAnalytics() {
    console.log('Refreshing analytics...');
    
    // Reinitialize all charts
    if (typeof Chart !== 'undefined') {
        Chart.helpers.each(Chart.instances, (instance) => {
            instance.destroy();
        });
    }
    
    initializeAnalytics();
}

// Make functions globally available
window.refreshAnalytics = refreshAnalytics;
window.initializeAnalytics = initializeAnalytics;
window.initializeDashboard = initializeDashboard;