self.addEventListener('install', e => {
  e.waitUntil(
    caches.open('tarot-pwa').then(cache => {
      return cache.addAll([
        '/',
        '/manifest.json',
        '/app-icon-192.png',
        '/app-icon-512.png'
      ]);
    })
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(response => {
      return response || fetch(e.request);
    })
  );
});