const CACHE = 'chinu-ikesu-launcher-v1';
const FILES = [
  './', './index.html', './assets/css/launcher.css?v=1', './assets/js/launcher.js?v=1',
  './assets/launcher/chinu.png', './assets/launcher/doppel.png', './assets/launcher/umi.png',
  './assets/img/cast/que.webp', './apple-touch-icon.png', './favicon.png', './manifest.webmanifest'
];
const urls = new Set(FILES.map(path => new URL(path, self.registration.scope).href));
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  // The origin also hosts games. Never touch their caches or storage.
  event.waitUntil(caches.keys().then(keys => Promise.all(keys
    .filter(key => key.startsWith('chinu-ikesu-launcher-') && key !== CACHE)
    .map(key => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  // Only handle the exact portal assets, never game pages, APIs or credentials.
  if (event.request.method !== 'GET' || !urls.has(event.request.url)) return;
  event.respondWith(fetch(event.request).then(response => {
    if (response.ok) {
      const copy = response.clone();
      event.waitUntil(caches.open(CACHE).then(cache => cache.put(event.request, copy)).catch(() => {}));
    }
    return response;
  }).catch(() => caches.match(event.request).then(cached => cached || Response.error())));
});
