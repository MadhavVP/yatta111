// ==========================================
// THEMIS LEGISLATIVE ALERTS
// Notification & Bill Display System
// ==========================================

// ==========================================
// NOTIFICATION SUBSCRIPTION
// ==========================================

async function subscribeUser() {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = 'Requesting notification permission...';

    if (!('serviceWorker' in navigator)) {
        statusDiv.textContent = 'Push notifications are not supported in this browser.';
        return;
    }

    try {
        // 1. Get VAPID Key from server
        const response = await fetch('/api/vapid-key');
        const data = await response.json();
        const publicKey = data.publicKey;

        if (!publicKey) {
            throw new Error("VAPID key not configured on server.");
        }

        // 2. Register Service Worker
        const registration = await navigator.serviceWorker.register('/sw.js', {
            scope: '/'
        });

        await navigator.serviceWorker.ready;

        // 3. Subscribe to Push Manager
        const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(publicKey)
        });

        // 4. Get selected interests
        const interests = Array.from(document.querySelectorAll('input[name="interest"]:checked'))
            .map(cb => cb.value);

        if (interests.length === 0) {
            statusDiv.textContent = 'Please select at least one interest area.';
            return;
        }

        // 5. Send subscription to server
        await fetch('/api/subscribe', {
            method: 'POST',
            body: JSON.stringify({
                subscription: subscription,
                interests: interests
            }),
            headers: {
                'content-type': 'application/json'
            }
        });

        statusDiv.textContent = 'Successfully subscribed to legislative alerts.';

    } catch (err) {
        console.error('Subscription error:', err);
        statusDiv.textContent = 'Error: ' + err.message;
    }
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

// ==========================================
// BILL DISPLAY
// ==========================================

async function loadBills() {
    const container = document.getElementById('bills-container');
    const loading = document.getElementById('loading');

    try {
        const response = await fetch('/api/feed');
        const bills = await response.json();

        loading.style.display = 'none';
        container.innerHTML = '';

        if (!bills || bills.length === 0) {
            container.innerHTML = '<div class="no-bills">No legislation found. Check back soon.</div>';
            return;
        }

        bills.forEach(bill => {
            const card = createBillCard(bill);
            container.appendChild(card);
        });

        console.log(`Loaded ${bills.length} bills`);

    } catch (error) {
        console.error('Error loading bills:', error);
        loading.style.display = 'none';
        container.innerHTML = '<div class="error">Unable to load legislation. Please try again later.</div>';
    }
}

function createBillCard(bill) {
    const card = document.createElement('div');
    card.className = 'bill-card';

    card.innerHTML = `
        <div class="bill-header">
            <h3 class="bill-title">${escapeHtml(bill.title || 'Untitled Legislation')}</h3>
            <span class="bill-id">${escapeHtml(bill.id || 'BILL')}</span>
        </div>
        
        <div class="bill-summary">
            ${escapeHtml(bill.summary || 'Summary not available.')}
        </div>
        
        ${bill.tags && bill.tags.length > 0 ? `
            <div class="bill-tags">
                ${bill.tags.map(tag => `<span class="tag">${escapeHtml(formatTag(tag))}</span>`).join('')}
            </div>
        ` : ''}
        
        <div class="bill-footer">
            <span class="bill-state">${escapeHtml(bill.state || 'IN')}</span>
            ${bill.url ? `
                <a href="${escapeHtml(bill.url)}" target="_blank" rel="noopener noreferrer" class="bill-link">
                    View Full Text
                </a>
            ` : ''}
        </div>
    `;

    return card;
}

function formatTag(tag) {
    return tag
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener('DOMContentLoaded', function () {
    // Load bills
    loadBills();

    // Set up notification button
    const notifyBtn = document.getElementById('notifyBtn');
    if (notifyBtn) {
        notifyBtn.addEventListener('click', subscribeUser);
    }

    // Reload bills every 5 minutes
    setInterval(loadBills, 5 * 60 * 1000);
});