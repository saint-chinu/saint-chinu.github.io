if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./portal-sw.js').catch(error => {
      console.warn('Portal offline cache is unavailable.', error);
    });
  });
}
