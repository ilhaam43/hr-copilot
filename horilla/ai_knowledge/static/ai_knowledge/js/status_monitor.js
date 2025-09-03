/**
 * AI Knowledge Status Monitor
 * Real-time monitoring untuk status dokumen dan training
 */

class AIKnowledgeStatusMonitor {
    constructor() {
        this.refreshInterval = 30000; // 30 seconds
        this.intervalId = null;
        this.isMonitoring = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.startMonitoring();
    }

    bindEvents() {
        // Auto-start monitoring jika ada dokumen processing
        if (document.querySelector('.spinner-border')) {
            this.startMonitoring();
        }

        // Manual refresh button
        const refreshBtn = document.getElementById('refresh-status');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshStatus());
        }

        // Toggle monitoring
        const toggleBtn = document.getElementById('toggle-monitoring');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleMonitoring());
        }
    }

    startMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        this.intervalId = setInterval(() => {
            this.refreshStatus();
        }, this.refreshInterval);
        
        this.updateMonitoringUI(true);
        console.log('🔄 Status monitoring started');
    }

    stopMonitoring() {
        if (!this.isMonitoring) return;
        
        this.isMonitoring = false;
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        this.updateMonitoringUI(false);
        console.log('⏹️ Status monitoring stopped');
    }

    toggleMonitoring() {
        if (this.isMonitoring) {
            this.stopMonitoring();
        } else {
            this.startMonitoring();
        }
    }

    async refreshStatus() {
        try {
            // Update document status
            await this.updateDocumentStatus();
            
            // Update processing logs
            await this.updateProcessingLogs();
            
            // Update dashboard stats
            await this.updateDashboardStats();
            
            this.updateLastRefresh();
            
        } catch (error) {
            console.error('❌ Error refreshing status:', error);
            this.showNotification('Error updating status', 'error');
        }
    }

    async updateDocumentStatus() {
        const response = await fetch('/ai-knowledge/api/document-status/');
        if (!response.ok) throw new Error('Failed to fetch document status');
        
        const documents = await response.json();
        
        documents.forEach(doc => {
            this.updateDocumentCard(doc);
        });
        
        // Stop monitoring jika tidak ada dokumen processing
        const hasProcessing = documents.some(doc => doc.status === 'processing');
        if (!hasProcessing && this.isMonitoring) {
            this.stopMonitoring();
        }
    }

    updateDocumentCard(doc) {
        const card = document.querySelector(`[data-document-id="${doc.id}"]`);
        if (!card) return;
        
        // Update status badge
        const statusBadge = card.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `badge status-badge status-${doc.status}`;
            statusBadge.textContent = this.getStatusText(doc.status);
        }
        
        // Update progress bar
        const progressBar = card.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = `${doc.progress || 0}%`;
            progressBar.setAttribute('aria-valuenow', doc.progress || 0);
        }
        
        // Update spinner visibility
        const spinner = card.querySelector('.spinner-border');
        if (spinner) {
            spinner.style.display = doc.status === 'processing' ? 'inline-block' : 'none';
        }
        
        // Update timestamp
        const timestamp = card.querySelector('.last-updated');
        if (timestamp) {
            timestamp.textContent = `Updated: ${new Date(doc.updated_at).toLocaleTimeString()}`;
        }
    }

    async updateProcessingLogs() {
        const logsContainer = document.getElementById('recent-logs');
        if (!logsContainer) return;
        
        const response = await fetch('/ai-knowledge/processing-logs/?format=json&limit=5');
        if (!response.ok) return;
        
        const logs = await response.json();
        
        logsContainer.innerHTML = logs.map(log => `
            <div class="log-entry log-${log.level}">
                <span class="log-icon">${this.getLogIcon(log.level)}</span>
                <span class="log-time">${new Date(log.created_at).toLocaleTimeString()}</span>
                <span class="log-message">${log.message}</span>
            </div>
        `).join('');
    }

    async updateDashboardStats() {
        const statsContainer = document.getElementById('dashboard-stats');
        if (!statsContainer) return;
        
        const response = await fetch('/ai-knowledge/api/dashboard-stats/');
        if (!response.ok) return;
        
        const stats = await response.json();
        
        // Update stat cards
        this.updateStatCard('total-documents', stats.total_documents);
        this.updateStatCard('processed-documents', stats.processed_documents);
        this.updateStatCard('pending-documents', stats.pending_documents);
        this.updateStatCard('failed-documents', stats.failed_documents);
    }

    updateStatCard(cardId, value) {
        const card = document.getElementById(cardId);
        if (card) {
            const valueElement = card.querySelector('.stat-value');
            if (valueElement) {
                valueElement.textContent = value;
            }
        }
    }

    updateMonitoringUI(isActive) {
        const toggleBtn = document.getElementById('toggle-monitoring');
        if (toggleBtn) {
            toggleBtn.textContent = isActive ? '⏹️ Stop Monitoring' : '▶️ Start Monitoring';
            toggleBtn.className = `btn ${isActive ? 'btn-warning' : 'btn-success'} btn-sm`;
        }
        
        const statusIndicator = document.getElementById('monitoring-status');
        if (statusIndicator) {
            statusIndicator.innerHTML = isActive 
                ? '<span class="text-success">🟢 Monitoring Active</span>'
                : '<span class="text-muted">⚫ Monitoring Inactive</span>';
        }
    }

    updateLastRefresh() {
        const lastRefreshElement = document.getElementById('last-refresh');
        if (lastRefreshElement) {
            lastRefreshElement.textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        }
    }

    getStatusText(status) {
        const statusMap = {
            'pending': 'Pending',
            'processing': 'Processing',
            'completed': 'Completed',
            'approved': 'Approved',
            'failed': 'Failed',
            'error': 'Error'
        };
        return statusMap[status] || status;
    }

    getLogIcon(level) {
        const iconMap = {
            'success': '✅',
            'error': '❌',
            'warning': '⚠️',
            'info': 'ℹ️'
        };
        return iconMap[level] || '📝';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Public methods for external use
    getMonitoringStatus() {
        return {
            isActive: this.isMonitoring,
            interval: this.refreshInterval,
            lastRefresh: new Date().toISOString()
        };
    }

    setRefreshInterval(seconds) {
        this.refreshInterval = seconds * 1000;
        if (this.isMonitoring) {
            this.stopMonitoring();
            this.startMonitoring();
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    window.aiKnowledgeMonitor = new AIKnowledgeStatusMonitor();
    
    // Add monitoring controls to dashboard if not exists
    const dashboardControls = document.getElementById('dashboard-controls');
    if (dashboardControls) {
        dashboardControls.innerHTML += `
            <div class="monitoring-controls mt-3">
                <button id="refresh-status" class="btn btn-primary btn-sm me-2">
                    🔄 Refresh Now
                </button>
                <button id="toggle-monitoring" class="btn btn-success btn-sm me-2">
                    ▶️ Start Monitoring
                </button>
                <span id="monitoring-status" class="text-muted">
                    ⚫ Monitoring Inactive
                </span>
                <div class="mt-2">
                    <small id="last-refresh" class="text-muted"></small>
                </div>
            </div>
        `;
        
        // Re-bind events after adding controls
        window.aiKnowledgeMonitor.bindEvents();
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIKnowledgeStatusMonitor;
}