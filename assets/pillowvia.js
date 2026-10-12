/* Pillowvia: carousels and "read more" toggles. */
(function () {
  function initCarousel(root) {
    if (root.dataset.pvReady) return;
    root.dataset.pvReady = '1';
    var track = root.querySelector('.pv-carousel__track');
    if (!track) return;
    function step() {
      var card = track.firstElementChild;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 16;
      return card ? card.getBoundingClientRect().width + gap : track.clientWidth;
    }
    var prev = root.querySelector('[data-pv-prev]');
    var next = root.querySelector('[data-pv-next]');
    if (prev) prev.addEventListener('click', function () {
      var atStart = track.scrollLeft <= 4;
      track.scrollTo({ left: atStart ? track.scrollWidth : track.scrollLeft - step(), behavior: 'smooth' });
    });
    if (next) next.addEventListener('click', function () {
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      track.scrollTo({ left: atEnd ? 0 : track.scrollLeft + step(), behavior: 'smooth' });
    });
  }

  function initClamp(el) {
    if (el.dataset.pvReady) return;
    el.dataset.pvReady = '1';
    var btn = el.parentElement.querySelector('[data-pv-more]');
    if (!btn) return;
    if (el.scrollHeight > el.clientHeight + 2) btn.hidden = false;
    btn.addEventListener('click', function () {
      var open = el.classList.toggle('is-open');
      btn.textContent = open ? 'Read less' : 'Read more';
    });
  }

  function init(scope) {
    (scope || document).querySelectorAll('[data-pv-carousel]').forEach(initCarousel);
    (scope || document).querySelectorAll('[data-pv-clamp]').forEach(initClamp);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); });
  else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
})();
