# Pillowvia Shopify theme

Online store theme for **Pillowvia**, based on Shopify's [Dawn](https://github.com/Shopify/dawn) theme (v16).

## Connect to Shopify

1. In Shopify admin open **Online Store → Themes**.
2. Click **Add theme → Connect from GitHub**.
3. Choose this repository and the branch `claude/shopify-store-integration-7c9xli`.
4. Click **Customize** on the new theme to preview it, then **Publish** when ready.

Every push to the branch updates the connected theme automatically.

## What's custom

- `config/settings_data.json` — brand colors (white / `#EEEFF3` / navy `#303D66`), Inter font, rounded buttons and cards.
- `templates/product.json` — long-form product page: benefits, trust badges, problems & solutions,
  sleep positions, comparison table, 100-night guarantee, FAQ and an app slot for reviews.
- `templates/index.json` — homepage built around the featured pillow.
- New sections (all editable in the theme editor):
  - `sections/pv-problems.liquid` — problem / cause / solution cards
  - `sections/pv-image-cards.liquid` — image cards (sleep positions)
  - `sections/pv-comparison.liquid` — "us vs. them" table
  - `sections/pv-guarantee.liquid` — guarantee badge with text
  - `sections/pv-badges.liquid` — trust badge strip
- `assets/pillowvia.css` — styles for the sections above.
