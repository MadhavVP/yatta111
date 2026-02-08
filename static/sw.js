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

    const title = data.title || 'Themis';
    const options = {
        body: data.body || 'New legislation may affect you',
        icon: '/static/icon.png',  // Uses your icon.png file
        badge: '/static/icon.png', // Can also use same icon for badge
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