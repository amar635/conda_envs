const staticCacheName = 'site-static';
const assets = [

  '/static/css/bootstrap.css',
  '/static/js/app.js',
  '/static/manifest.json',
  '/static/css/style.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js',

  'https://fonts.googleapis.com/icon?family=Material+Icons',
  "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.4/font/bootstrap-icons.css"
];



self.addEventListener('install', evt => {
    //console.log('service worker installed');
    evt.waitUntil(
      caches.open(staticCacheName).then(cache => {
        console.log('caching shell assets');
        cache.addAll(assets);
      })
    );
  });
  
// //   // activate event
  self.addEventListener('activate', evt => {
    console.log('service worker activated');
  });

  self.addEventListener('fetch', evt => {
    console.log('service worker fetch event',evt);
  });