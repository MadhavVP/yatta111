// Themis Legislative Alert Service Worker
// Handles push notifications

self.addEventListener('push', function (event) {
    console.log('Push notification received');

    let data;
    try {
        data = event.data.json();
    } catch (e) {
        data = {
            title: 'Legislative Alert',
            body: event.data.text()
        };
    }

    const title = data.title || 'Themis Legislative Alert';
    const options = {
        body: data.body || 'New legislation may affect you',
        icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="60" width="80" height="8" fill="%23CBAE51"/><rect x="45" y="20" width="10" height="48" fill="%232F3F5E"/><circle cx="35" cy="40" r="8" fill="%23B04467"/><circle cx="65" cy="40" r="8" fill="%23B04467"/></svg>',
        badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="60" width="80" height="8" fill="%23CBAE51"/></svg>',
        vibrate: [200, 100, 200],
        tag: 'themis-legislation',
        data: data.data || {},
        requireInteraction: false
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', function (event) {
    console.log('Notification clicked');

    event.notification.close();

    const url = event.notification.data.url || '/';

    event.waitUntil(
        clients.openWindow(url)
    );
});

self.addEventListener('activate', function (event) {
    console.log('Service worker activated');
    event.waitUntil(clients.claim());
});