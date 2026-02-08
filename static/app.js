// publicVapidKey is fetched from /api/vapid-key endpoint below

async function registerServiceWorker() {
    const register = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
    });
    return register;
}

async function subscribeUser() {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = 'Requesting permission...';

    if (!('serviceWorker' in navigator)) {
        statusDiv.textContent = 'Service Worker not supported.';
        return;
    }

    try {
        // 1. Get VAPID Key from server
        const response = await fetch('/api/vapid-key');
        const data = await response.json();
        const publicKey = data.publicKey;
        console.log("Fetcher VAPID Key:", publicKey); // Debug log

        if (!publicKey) {
            throw new Error("No public key returned from server.");
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

        // 4. Send Subscription to Server
        const interests = Array.from(document.querySelectorAll('input[name="interest"]:checked'))
            .map(cb => cb.value);

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

        statusDiv.textContent = 'Subscribed successfully!';
    } catch (err) {
        console.error(err);
        statusDiv.textContent = 'Error subscribing: ' + err.message;
    }
}

// Boilerplate to convert VAPID key
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

document.getElementById('notifyBtn').addEventListener('click', subscribeUser);
