// const staticCacheName = 'site-static-v1.0.2';
// const dynamicCacheName = 'site-dynamic-v1.0.2';
// const assets = [
//   '/',
//   '/static/css/style.css',
//   '/static/js/app.js',
//   '/static/js/chart-js.js',
//   '/static/manifest.json',
//   '/error',
//   'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css',
//   'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css',
//   'https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js',
//   'https://cdn.jsdelivr.net/npm/chart.js',
//   'https://fonts.googleapis.com/icon?family=Material+Icons'
// ];
// install event
self.addEventListener('install', evt => {
    // console.log('service worker has been installed');
    // evt.waitUntil(
    //     caches.open(staticCacheName).then( cache => {
    //         console.log('Caching shell assets');
    //         cache.addAll(assets);
    //     })
    //     );
  });

  // activate event
self.addEventListener('activate', evt => {
  //console.log('service worker activated');
  // evt.waitUntil(
  //   caches.keys().then(keys => {
  //     //console.log(keys);
  //     return Promise.all(keys
  //       .filter(key => key !== staticCacheName && key !== dynamicCacheName)
  //       .map(key => caches.delete(key))
  //     );
  //   })
  // );
});

// fetch event
self.addEventListener('fetch', evt => {
  // if(evt.request.url.indexOf('about') > -1){
  //   console.log('TRUE');
  // } else {
  //   console.log('FALSE');
  // };
  //console.log('fetch event', evt);
  // evt.respondWith(
  //   caches.match(evt.request).then(cacheRes => {
  //     return cacheRes || fetch(evt.request).then(fetchRes => {
  //       return caches.open(dynamicCacheName).then(cache => {
  //         cache.put(evt.request.url, fetchRes.clone());
  //         // check cached items size
  //         limitCacheSize(dynamicCacheName, 15);
  //         return fetchRes;
  //       })
  //     });
  //   }).catch(() => {
  //     caches.match('/error');
  //     // if(evt.request.url.indexOf('.html') > -1){
  //     //   return caches.match('/pages/fallback.html');
  //     // } 
  //   })
  // );
});
  // self.addEventListener('fetch', evt => {
  //   //console.log('fetch event', evt);
  //   evt.respondWith(
  //     // caches.match(evt.request).then(cacheRes => {
  //     //   return cacheRes || fetch(evt.request);
  //     // })
  //     caches.match(evt.request).then(cacheRes => {
  //       return cacheRes || fetch(evt.request).then(async fetchRes => {
  //         const cache = await caches.open(dynamicCacheName);
  //         cache.put(evt.request.url, fetchRes.clone());
  //         // check cached items size
  //         limitCacheSize(dynamicCacheName, 15);
  //         return fetchRes;
  //       });
  //     }).catch(() => {
  //       caches.match('/error');
  //       // if(evt.request.url.indexOf('.html') > -1){
  //       //   return caches.match('/error');
  //       // } 
  //     })
  //   );
  // });