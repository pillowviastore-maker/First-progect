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
      var checked = root.querySelector('input[name^="pv-bundle-"]:checked');
      if (!checked) return;
      qty.value = checked.value;
      section.querySelectorAll('.pv-atc-price').forEach(function (el) { el.textContent = checked.dataset.total; });
    }
    var colors = root.querySelector('[data-pv-colors]');
    var form = document.getElementById(root.dataset.formId);

    function multiColorActive() {
      var checked = root.querySelector('input[name^="pv-bundle-"]:checked');
      return colors && checked && checked.value === '3';
    }

    function syncColors() {
      if (!colors) return;
      colors.hidden = !multiColorActive();
    }

    // When the free-pillow bundle is chosen, add each pillow as its own cart line
    // so customers can mix colors. Dawn builds FormData synchronously in its
    // submit handler, so we swap the inputs in the capture phase and restore after.
    if (form && colors) {
      document.addEventListener('submit', function (e) {
        if (e.target !== form || !multiColorActive()) return;
        var counts = {};
        colors.querySelectorAll('[data-pv-color-row]').forEach(function (row) {
          var pick = row.querySelector('input:checked');
          if (pick) counts[pick.value] = (counts[pick.value] || 0) + 1;
        });
        var ids = Object.keys(counts);
        if (!ids.length) return;
        var disabled = [];
        form.querySelectorAll('input[name="id"]').forEach(function (el) { if (!el.disabled) { el.disabled = true; disabled.push(el); } });
        if (!qty.disabled) { qty.disabled = true; disabled.push(qty); }
        var added = ids.map(function (id, i) {
          var wrap = document.createElement('div');
          wrap.hidden = true;
          wrap.innerHTML = '<input name="items[' + i + '][id]" value="' + id + '"><input name="items[' + i + '][quantity]" value="' + counts[id] + '">';
          form.appendChild(wrap);
          return wrap;
        });
        setTimeout(function () {
          added.forEach(function (w) { w.remove(); });
          disabled.forEach(function (el) { el.disabled = false; });
        }, 0);
      }, true);
    }

    root.addEventListener('change', function (e) {
      if (e.target.name && e.target.name.indexOf('pv-bundle-') === 0) { apply(); syncColors(); }
    });
    apply();
    syncColors();
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
