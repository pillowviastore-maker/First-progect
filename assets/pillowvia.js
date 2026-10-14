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
    function advance() {
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      track.scrollTo({ left: atEnd ? 0 : track.scrollLeft + step(), behavior: 'smooth' });
    }
    if (next) next.addEventListener('click', advance);

    // Autoplay: move every 4s, pause while the visitor interacts or the carousel is off screen.
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var paused = false, visible = false;
    ['mouseenter', 'touchstart', 'focusin'].forEach(function (ev) { root.addEventListener(ev, function () { paused = true; }, { passive: true }); });
    ['mouseleave', 'touchend', 'focusout'].forEach(function (ev) { root.addEventListener(ev, function () { setTimeout(function () { paused = false; }, 2500); }, { passive: true }); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) { visible = entries[0].isIntersecting; }).observe(root);
    } else { visible = true; }
    setInterval(function () { if (!paused && visible && !document.hidden) advance(); }, 4000);
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

    function bundleQty() {
      var checked = root.querySelector('input[name^="pv-bundle-"]:checked');
      return checked ? parseInt(checked.value, 10) || 1 : 1;
    }

    function multiColorActive() {
      return !!colors && bundleQty() >= 2;
    }

    // Only the rows for the chosen number of pillows count
    function activeRows() {
      var n = bundleQty();
      return Array.prototype.filter.call(colors.querySelectorAll('[data-pv-color-row]'), function (row) {
        return parseInt(row.dataset.n, 10) <= n;
      });
    }

    var picker = (root.closest('.product__info-container') || document).querySelector('variant-selects');

    function syncColors() {
      if (!colors) return;
      var on = multiColorActive();
      colors.hidden = !on;
      var n = bundleQty();
      colors.querySelectorAll('[data-pv-color-row]').forEach(function (row) { row.hidden = parseInt(row.dataset.n, 10) > n; });
      if (on) {
        colors.classList.remove('is-open');
        void colors.offsetWidth;
        colors.classList.add('is-open');
      }
      if (picker) picker.classList.toggle('pv-picker-hidden', on);
      syncQuickPay();
    }

    // Express buttons (Shop Pay / Apple Pay / Google Pay) buy a single variant,
    // so hide them while the customer is mixing colors in a bundle.
    function syncQuickPay() {
      var mixed = false;
      if (multiColorActive()) {
        var seen = {};
        activeRows().forEach(function (row) { var el = row.querySelector('input:checked'); if (el) seen[el.value] = 1; });
        mixed = Object.keys(seen).length > 1;
      }
      section.classList.toggle('pv-no-quickpay', mixed);
    }

    // When a 2- or 3-pillow bundle is chosen, add each color as its own cart line
    // so customers can mix colors. Dawn builds FormData synchronously in its
    // submit handler, so we swap the inputs in the capture phase and restore after.
    if (form && colors) {
      document.addEventListener('submit', function (e) {
        if (e.target !== form || !multiColorActive()) return;
        var counts = {};
        activeRows().forEach(function (row) {
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
      else if (e.target.closest && e.target.closest('[data-pv-colors]')) syncQuickPay();
    });
    apply();
    syncColors();
  }

  var REVEAL = '.pv-section-title, .pv-card-frame, .pv-split__media, .pv-split__content, .pv-photo-card, .pv-comment, .pv-review, .pv-acc, .pv-expert, .pv-guarantee, .pv-hero__content, .pv-hero__media, .pv-product-card, .pv-badge, .pv-strip';
  var revealObserver = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('pv-in'); revealObserver.unobserve(en.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }) : null;

  function initReveal(scope) {
    if (!revealObserver || window.Shopify && Shopify.designMode) return;
    (scope || document).querySelectorAll(REVEAL).forEach(function (el, i) {
      if (el.classList.contains('pv-reveal')) return;
      el.classList.add('pv-reveal');
      el.style.transitionDelay = Math.min((i % 4) * 80, 240) + 'ms';
      revealObserver.observe(el);
    });
  }

  // "Add my FREE pillow" button in the cart: adds the missing pillows and refreshes the cart.
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-pv-add-bundle]');
    if (!btn) return;
    btn.setAttribute('aria-busy', 'true');
    var drawer = document.querySelector('cart-drawer');
    var body = { items: [{ id: Number(btn.dataset.variant), quantity: Number(btn.dataset.qty) }] };
    if (drawer) { body.sections = ['cart-drawer', 'cart-icon-bubble']; body.sections_url = window.location.pathname; }
    fetch(window.Shopify && Shopify.routes ? Shopify.routes.root + 'cart/add.js' : '/cart/add.js', {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(body)
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (drawer && res.sections && document.querySelector('.drawer__inner') && !document.querySelector('.cart__footer')) { drawer.renderContents(res); }
      else { window.location.reload(); }
    }).catch(function () { window.location.href = '/cart'; });
  });

  // Judge.me: keep the full review list collapsed under the carousel button
  function initJudgeme() {
    var btn = document.querySelector('[data-pv-jm-toggle]');
    var widget = document.querySelector('.jdgm-review-widget, .jdgm-widget.jdgm-review-widget');
    var section = widget && widget.closest('.shopify-section');
    if (!btn) return;
    if (!section) { btn.hidden = true; return; }
    if (window.Shopify && Shopify.designMode) return;
    section.classList.add('pv-jm-collapsed');
    btn.addEventListener('click', function () {
      var open = section.classList.toggle('pv-jm-collapsed') === false;
      btn.setAttribute('aria-expanded', open);
      btn.textContent = open ? 'Hide reviews' : btn.dataset.label;
      if (open) section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    btn.dataset.label = btn.textContent;
  }

  function init(scope) {
    initReveal(scope);
    if (!scope) initJudgeme();
    (scope || document).querySelectorAll('[data-pv-bundles]').forEach(initBundles);
    (scope || document).querySelectorAll('[data-pv-carousel]').forEach(initCarousel);
    (scope || document).querySelectorAll('[data-pv-clamp]').forEach(initClamp);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { init(); });
  else init();
  document.addEventListener('shopify:section:load', function (e) { init(e.target); });
})();
