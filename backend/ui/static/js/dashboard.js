// Dashboard JavaScript
const API_BASE = window.location.origin;

// Load opportunities
async function loadOpportunities() {
    try {
        const response = await fetch(`${API_BASE}/api/ml/opportunities`);
        const data = await response.json();

        // Update stats
        document.getElementById('opp-count').textContent = data.count || 0;
        document.getElementById('last-scan').textContent = new Date(data.timestamp).toLocaleString();

        // Calculate total profit
        const totalProfit = data.opportunities.reduce((sum, opp) => {
            const profit = (opp.predicted_price - opp.price) * opp.quantity;
            return sum + profit;
        }, 0);
        document.getElementById('total-profit').textContent = formatGold(totalProfit);

        // Render table
        const tbody = document.getElementById('opportunities-tbody');
        tbody.innerHTML = '';

        data.opportunities.slice(0, 20).forEach(opp => {
            const profit = (opp.predicted_price - opp.price) * opp.quantity;
            const roi = ((opp.predicted_price - opp.price) / opp.price * 100).toFixed(1);

            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${opp.item_id}</td>
                <td>${formatGold(opp.price)}</td>
                <td>${formatGold(opp.predicted_price)}</td>
                <td class="profit">${formatGold(profit)}</td>
                <td class="roi">${roi}%</td>
                <td>${opp.quantity}</td>
            `;
        });
    } catch (error) {
        console.error('Error loading opportunities:', error);
        document.getElementById('opportunities-tbody').innerHTML =
            '<tr><td colspan="6" class="error">Error loading data. Is the server running?</td></tr>';
    }
}

// Load AI groups count
async function loadGroupsCount() {
    try {
        const response = await fetch(`${API_BASE}/static/data/groups/ai_groups.json`);
        const data = await response.json();
        document.getElementById('group-count').textContent = data.num_groups || 0;
    } catch (error) {
        document.getElementById('group-count').textContent = '0';
    }
}

// Load news predictions
async function loadNews() {
    try {
        const response = await fetch(`${API_BASE}/static/data/news/news_analysis.json`);
        const data = await response.json();

        const container = document.getElementById('news-alerts');
        container.innerHTML = '';

        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.slice(0, 5).forEach(rec => {
                const alert = document.createElement('div');
                alert.className = `alert alert-${rec.action.toLowerCase()}`;
                alert.innerHTML = `
                    <strong>${rec.action}: ${rec.category}</strong><br>
                    ${rec.strategy}<br>
                    <em>Expected ${rec.expected_roi || rec.expected_loss_avoided} - ${rec.timeline}</em>
                `;
                container.appendChild(alert);
            });
        } else {
            container.innerHTML = '<p class="text-muted">No news predictions available.</p>';
        }
    } catch (error) {
        document.getElementById('news-alerts').innerHTML = '<p class="text-muted">News analysis not available.</p>';
    }
}

// Format copper to gold
function formatGold(copper) {
    const gold = Math.floor(copper / 10000);
    const silver = Math.floor((copper % 10000) / 100);
    const copperRem = copper % 100;

    if (gold > 0) {
        return `${gold.toLocaleString()}g ${silver}s ${copperRem}c`;
    } else if (silver > 0) {
        return `${silver}s ${copperRem}c`;
    } else {
        return `${copperRem}c`;
    }
}

// Refresh button
function refreshOpportunities() {
    loadOpportunities();
    loadGroupsCount();
    loadNews();
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadOpportunities();
    loadGroupsCount();
    loadNews();

    // Auto-refresh every 5 minutes
    setInterval(refreshOpportunities, 300000);
});
