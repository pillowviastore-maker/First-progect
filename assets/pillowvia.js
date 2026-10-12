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

  function initBundles(root) {
    if (root.dataset.pvReady) return;
    root.dataset.pvReady = '1';
    var qty = root.querySelector('[data-pv-qty]');
    var section = root.closest('section') || document;
    function apply() {
      var checked = root.querySelector('input[type=radio]:checked');
      if (!checked) return;
      qty.value = checked.value;
      section.querySelectorAll('.pv-atc-price').forEach(function (el) { el.textContent = checked.dataset.total; });
    }
    root.addEventListener('change', apply);
    apply();
  }

  function init(scope) {
    (scope || document).querySelectorAll('[data-pv-bundles]').forEach(initBundles);
    (scope || document).querySelectorAll('[data-pv-carousel]').forEach(initCarousel);
    (scope || document).querySelectorAll('[data-pv-clamp]').forEach(initClamp);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); });
  else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
})();
