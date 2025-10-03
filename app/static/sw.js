// Service Worker para TEA Edition
const CACHE_NAME = 'tea-edition-v1';
const urlsToCache = [
  '/tea/',
  '/tea/nino/',
  '/tea/padres/',
  '/static/css/style.css',
  '/static/js/app.js'
];

// Instalar Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Cache abierto');
        return cache.addAll(urlsToCache);
      })
  );
});

// Interceptar requests
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - devolver respuesta
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

// Notificaciones push
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : '¡Es hora de aprender!',
    icon: '/static/img/icon-192.png',
    badge: '/static/img/badge-72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'Ir a la app',
        icon: '/static/img/checkmark.png'
      },
      {
        action: 'close',
        title: 'Cerrar',
        icon: '/static/img/xmark.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('TEA Learning', options)
  );
});





