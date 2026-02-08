self.addEventListener('push', function (event) {
    const data = event.data.text();
    console.log('Push received:', data);

    self.registration.showNotification('Legislative Alert', {
        body: data,
        icon: 'http://image.ibb.co/frYOFd/tmlogo.png' // Placeholder icon
    });
});
