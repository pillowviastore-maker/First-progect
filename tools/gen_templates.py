"""Generate Pillowvia product + home templates, header/footer groups."""
import json
import re


def load_json(path):
    """Read a theme JSON file, ignoring the comment header Shopify adds."""
    return json.loads(re.sub(r"^\s*/\*.*?\*/", "", open(path).read(), flags=re.S))

HANDLE = "pillowvia-ergonomic-cervical-pillow"
PRODUCT_URL = f"shopify://products/{HANDLE}"
PARTNER_NOTE = ""
SHOWN_RATING = "4.8"
REVIEWS_TOTAL = "15,500+"
CUSTOMERS_TOTAL = "55,000+"

# Reviews (partner store, translated). (rating, title, text, author)
REVIEWS = [
    (5, "Worth every penny", "Worth every penny! My neck pain has decreased significantly since I started using this pillow.", "Andrea"),
    (4, "Customer service", "I ordered an extra pillowcase that didn't arrive at first, but customer support was very kind and reshipped it for free. Great service — 4 stars only because of the small initial hiccup.", "Giorgio"),
    (5, "Neck pain gone!", "I'm very happy with my pillow. Since I started using it, my neck pain has disappeared. I had swelling at the base of my neck and now it's gone. It's been fantastic, thank you! 👍", "Lucia"),
    (3, "Good, but it takes time", "The pillow is good, but it took me a few days to get used to it. I sleep better now, but it wasn't an immediate change.", "Luca"),
    (5, "No adjustment period", "I was afraid I'd have to put up with weeks of neck and shoulder pain to get used to it, but that wasn't the case. I fall asleep faster and almost never wake up with neck or back pain anymore. It really made a difference for me.", "Serena"),
    (5, "Happy with my purchase", "I'm really happy with my pillow. Thank you!", "Martina"),
    (5, "The best pillow for my husband", "Finally a pillow that really relieves neck pain. My husband had suffered for years: after a few days of use he told me it's the best pillow he's ever tried. He no longer has pain at night. It really makes a difference. We highly recommend it!", "Francesca"),
    (5, "No more stiffness", "I wake up without stiffness. 10/10", "Simone"),
    (5, "The best pillow I've tried", "No neck pain. I must have tried at least ten, including a water pillow. This is without a doubt the best pillow I've ever had.", "Davide"),
    (5, "Neck pain gone", "I suffered from neck pain for years, but this pillow has really made a difference. I wake up pain-free and finally rested!", "Laura"),
    (5, "I use it on the couch too", "I have back and neck problems and I use this pillow while reading or watching TV on the couch. It's memory foam and helps relieve the pain. I also use it for my back when sitting, and the pain goes away.", "Giuseppe"),
]
RATING_AVG = int(sum(r[0] for r in REVIEWS) * 10 // len(REVIEWS)) / 10
REVIEW_COUNT = len(REVIEWS)

COMMENTS = [
    ("Really great product. In two nights it relieved my neck pain — I recommend it, thank you ❤️", "Patrizia G."),
    ("I have it too and I'm very happy with it. Highly recommended for anyone with a stiff neck.", "Angela T."),
    ("It arrived two days ago and I have to say it's really great — I already feel relief and sleep all night without tossing and turning.", "Francesco B."),
    ("I've only used it for two nights and I already feel a difference, especially in my left shoulder, which is the worst.", "Antonietta S."),
    ("I confirm everything — I've been using it for a week and have no neck pain.", "Lucy T."),
    ("Excellent pillow, I recommend it: I bought it more than 6 months ago and it really delivers.", "Maria L."),
    ("I'm 50 and I used to wake up sore every morning. I tried at least six pillows and none of them helped. This one did — THANK YOU!", "Alessandra G."),
    ("I've been using it for weeks and I no longer wake up with a stiff neck. You can really feel the difference.", "Giovanna B."),
]

PAIN = [
    ("Neck Pain", "Bad posture strains your neck overnight.", "Keeps your neck aligned while you sleep."),
    ("Shoulder Tension", "Flat pillows push your shoulders into stiff positions.", "Side grooves let your shoulders rest naturally."),
    ("Back Discomfort", "Poor support adds pressure on your lower back.", "Supports natural spine alignment."),
    ("Restless Sleep", "Tossing and turning means poor support.", "Memory foam spreads pressure evenly."),
    ("Morning Headaches", "Neck tension builds up during the night.", "Better alignment, calmer wake-ups."),
    ("Nighttime Breathing", "A bad head position can affect breathing.", "Keeps your head in a better position for quieter sleep."),
]

FAQ = [
    ("Is a pillowcase included?", "<p>Yes — a soft, removable cover shaped to fit the pillow is included.</p>"),
    ("How do I clean it?", "<p>Machine wash the cover on gentle (max 86°F / 30°C). Wipe the foam with a damp cloth — don't machine wash it.</p>"),
    ("How do I pay?", "<p>Visa, Mastercard, Amex, Apple Pay, Google Pay and Shop Pay — all SSL-secured.</p>"),
    ("How long to get used to it?", "<p>Most people feel comfortable after 1–2 nights; some take up to 10.</p>"),
    ("Which side should I use?", "<p>Lower center for back sleepers, higher sides for side sleepers. Just rotate it.</p>"),
    ("Is it hypoallergenic?", "<p>Yes — latex-free memory foam with a breathable cover.</p>"),
    ("What if it's not right for me?", "<p>You have <strong>100 nights</strong> to try it. Not happy? Get a full refund. See our <a href=\"/policies/refund-policy\">Refund Policy</a>.</p>"),
    ("How long does delivery take?", "<p>Free US shipping. Processed in 1–3 business days, delivered in 7–15. Tracking sent by email.</p>"),
]


def comments_section():
    return {
        "type": "pv-comments",
        "blocks": {f"c{i}": {"type": "comment", "settings": {"text": t, "author": a}} for i, (t, a) in enumerate(COMMENTS)},
        "block_order": [f"c{i}" for i in range(len(COMMENTS))],
        "settings": {"heading": "What Our <em>Customers Say</em>", "note": "", "color_scheme": "scheme-1", "padding_top": 16, "padding_bottom": 16},
    }


def reviews_section(scheme="scheme-1"):
    return {
        "type": "pv-reviews",
        "blocks": {f"rv{i}": {"type": "review", "settings": {"rating": r, "title": t, "text": f"<p>{x}</p>", "author": a}} for i, (r, t, x, a) in enumerate(REVIEWS)},
        "block_order": [f"rv{i}" for i in range(len(REVIEWS))],
        "settings": {"eyebrow": "Customer stories", "heading": "What Customers <em>Are Saying</em>", "score": "", "source_note": PARTNER_NOTE,
                     "color_scheme": scheme, "padding_top": 24, "padding_bottom": 24},
    }


def strip_section():
    return {
        "type": "pv-photo-strip",
        "blocks": {f"ph{i}": {"type": "photo", "settings": {"image": f"shopify://shop_images/pv-customer-clean-{i}.jpg"}} for i in range(1, 6)},
        "block_order": [f"ph{i}" for i in range(1, 6)],
        "settings": {"heading": "<em>Real People.</em> Better Sleep.", "wave": True, "color_scheme": "scheme-1", "padding_top": 12, "padding_bottom": 16},
    }


EXPERTS = [
    ("pv-expert-1.jpg", "Well designed, well made, and good for both sleep quality and spinal health. I highly recommend it.", "Anna Maria Guerrini", "Physiotherapist"),
    ("pv-expert-2.jpg", "A good pillow can really improve posture and sleep. This one stands out for its smart design — I recommend it to my patients.", "Luca Romano", "Physiotherapist"),
    ("pv-expert-3.jpg", "I felt the difference from the very first night. I recommend it to anyone with neck pain or muscle tension.", "Chiara Bianchi", "Professional massage therapist"),
]


def experts_section():
    return {
        "type": "pv-experts",
        "blocks": {f"e{i}": {"type": "expert", "settings": {"image": f"shopify://shop_images/{img}", "quote": q, "name": n, "role": r}} for i, (img, q, n, r) in enumerate(EXPERTS)},
        "block_order": [f"e{i}" for i in range(len(EXPERTS))],
        "settings": {"heading": "Recommended by Experts", "color_scheme": "scheme-1", "padding_top": 16, "padding_bottom": 20},
    }


def faq_section():
    return {
        "type": "pv-faq",
        "blocks": {f"q{i}": {"type": "question", "settings": {"question": q, "answer": a}} for i, (q, a) in enumerate(FAQ)},
        "block_order": [f"q{i}" for i in range(len(FAQ))],
        "settings": {"heading": "Still Have Questions?", "link_label": "No? Try Pillowvia now", "link": "", "wave": True,
                     "color_scheme": "scheme-1", "padding_top": 12, "padding_bottom": 24},
    }


def accordion(title, body):
    return ('<div class="product__accordion accordion"><details><summary><div class="summary__title">'
            f'<h2 class="h4 accordion__title inline-richtext">{title}</h2></div>'
            '<svg aria-hidden="true" focusable="false" class="icon icon-caret" viewBox="0 0 10 6"><path fill="currentColor" fill-rule="evenodd" d="M9.354.646a.5.5 0 00-.708 0L5 4.293 1.354.646a.5.5 0 00-.708.708l4 4a.5.5 0 00.708 0l4-4a.5.5 0 000-.708z" clip-rule="evenodd"/></svg>'
            f'</summary><div class="accordion__content rte">{body}</div></details></div>')


def tab(title, content):
    return {"type": "collapsible_tab", "settings": {"heading": title, "icon": "none", "content": content}}


product = {
    "sections": {
        "main": {
            "type": "main-product",
            "blocks": {
                "title": {"type": "title"},
                "checklist": {"type": "custom_liquid", "settings": {"custom_liquid": '<ul class="pv-checklist"><li>All-night neck alignment</li><li>Neck relief and less snoring</li><li>Fits every sleeping position</li><li>Breathable, washable cover</li></ul>'}},
                "featured_review": {"type": "pv_featured_review"},
                "price": {"type": "price"},
                "dots": {"type": "custom_liquid", "settings": {"custom_liquid": '<p class="pv-dots"><span>In stock — ready to ship</span><span>Free US shipping</span></p>'}},
                "variant_picker": {"type": "variant_picker", "settings": {"picker_type": "button", "swatch_shape": "circle"}},
                "bundles": {"type": "pv_bundles", "settings": {"heading": "Bundle & save", "default_qty": "1", "show_option_2": True, "title_2": "2 Pillows — 34% OFF",
                                                          "sub_2": "Only $31.50 each", "badge_2": "Most popular", "price_2": "62.99",
                                                          "title_3": "Buy 2, Get 1 FREE", "sub_3": "3 pillows — just $25 each", "badge_3": "Best value", "price_3": "74.99"}},
                "buy_buttons": {"type": "buy_buttons", "settings": {"show_dynamic_checkout": True, "show_gift_card_recipient": False}},
                "trust": {"type": "icon-with-text", "settings": {"layout": "horizontal", "icon_1": "return", "heading_1": "100-Night Money-Back Guarantee",
                                                                  "icon_2": "lock", "heading_2": "Secure checkout", "icon_3": "none", "heading_3": ""}},
                "delivery": {"type": "pv_delivery", "settings": {"heading": "FREE shipping on all US orders", "text": "Order today — estimated delivery", "min_days": 8, "max_days": 18}},
                "quick_faq": {"type": "custom_liquid", "settings": {"custom_liquid": (
                    '<div class="pv-quick-faq"><p class="pv-quick-faq__title">Quick answers</p>'
                    '<details><summary>When will I get it?</summary><p>Free US shipping. Orders ship in 1–3 business days and usually arrive in 7–15 business days, with tracking by email.</p></details>'
                    '<details><summary>What if it\'s not right for me?</summary><p>Try it for 100 nights. Not happy? Email us and get a full refund — see our <a href="/policies/refund-policy">Refund Policy</a>.</p></details>'
                    '<details><summary>How long does it take to get used to?</summary><p>Most people feel comfortable after 1–2 nights; some need up to 10 nights to adjust.</p></details>'
                    '</div>')}},
                "description": {"type": "custom_liquid", "settings": {"custom_liquid": accordion("Description", "{{ product.description }}")}},
                "specs": tab("Specifications", "<ul><li><strong>Pillow:</strong> approx. 24\" × 16\" × 5.5\" (60 × 41 × 14 cm)</li><li><strong>Cover:</strong> approx. 25\" × 16\" (63 × 41 cm)</li><li><strong>Fill:</strong> 100% memory foam</li><li><strong>Cover:</strong> removable, washable, with zipper and breathable mesh sides</li></ul><p><em>Dimensions are approximate and may vary slightly.</em></p>"),
                "returns": tab("Returns & Refunds", "<p>We're sure you'll love your pillow. If for any reason you're not 100% satisfied, you can request an easy return within <strong>100 days of delivery</strong>. Just email us at <a href=\"mailto:pillowviastore@gmail.com\">pillowviastore@gmail.com</a> and our team will help you quickly.</p>"),
                "care": tab("Washing Instructions", "<p>Remove the cover and machine wash on a gentle cycle at <strong>86–104°F (30–40°C)</strong>. Let it air dry completely before putting it back on the pillow. The foam can be <strong>wiped clean with a damp cloth</strong>.</p>"),
            },
            "block_order": ["title", "checklist", "featured_review", "price", "dots", "variant_picker", "bundles", "buy_buttons", "trust", "delivery", "quick_faq", "description", "specs", "returns", "care"],
            "settings": {"enable_sticky_info": True, "color_scheme": "scheme-1", "media_position": "left", "gallery_layout": "thumbnail_slider",
                         "media_size": "large", "constrain_to_viewport": True, "media_fit": "contain", "image_zoom": "lightbox",
                         "mobile_thumbnails": "show", "hide_variants": True, "enable_video_looping": False, "padding_top": 16, "padding_bottom": 16,
                         "pv_rating_label": "Excellent", "pv_rating": SHOWN_RATING, "pv_review_count": "reviews",
                         "pv_review_text": "", "pv_review_author": REVIEWS[0][3], "pv_review_note": "Verified purchase"},
        },
        "comments": comments_section(),
        "pain": {
            "type": "pv-pain-accordion",
            "blocks": {f"p{i}": {"type": "item", "settings": {"title": t, "cause": c, "solution": s}} for i, (t, c, s) in enumerate(PAIN)},
            "block_order": [f"p{i}" for i in range(len(PAIN))],
            "settings": {"heading": "Here's Why the Pain Won't Go Away — <em>And What You Can Do</em>", "image": "shopify://shop_images/pv-benefits-black.jpg",
                         "layout": "image-left", "cause_label": "Cause:", "solution_label": "How Pillowvia helps:", "color_scheme": "scheme-1", "padding_top": 16, "padding_bottom": 20},
        },
        "guarantee": {
            "type": "pv-guarantee",
            "settings": {"style": "box", "badge": "pv-badge-100.svg", "badge_alt": "100-night trial", "heading": "Try It Risk-Free for 100 Nights",
                         "text": "<p>Sleep on it for <strong>100 nights</strong>. Not completely satisfied? <strong>We'll refund you.</strong></p>",
                         "button_label": "", "button_link": "", "color_scheme": "scheme-1", "padding_top": 16, "padding_bottom": 16},
        },
        "goodbye": {
            "type": "pv-media-text",
            "settings": {"heading": "Say Goodbye to <em>Neck Pain</em>", "subheading": "Do you wake up tired and tense?",
                         "text": "<p>Neck pain, stiff shoulders and broken sleep drain your energy before the day even starts.</p><p>Often the reason is simple: <strong>your pillow doesn't support your neck</strong>.</p>",
                         "button_label": "Wake up rested — without the pain", "button_link": "", "image": "shopify://shop_images/pv-neck-pain-morning.jpg",
                         "layout": "image-right", "card": True, "center_text": False, "color_scheme": "scheme-2", "padding_top": 20, "padding_bottom": 12},
        },
        "protect": {
            "type": "pv-media-text",
            "settings": {"heading": "Protect Your Neck With <em>Pillowvia</em>", "subheading": "",
                         "text": "<p>Ergonomic support keeps your neck in its natural position, <strong>reducing tension</strong> for more comfortable mornings.</p>",
                         "button_label": "", "button_link": "", "image": "shopify://shop_images/pv-why-choose.jpg",
                         "layout": "image-left", "card": True, "center_text": False, "color_scheme": "scheme-2", "padding_top": 12, "padding_bottom": 20},
        },
        "positions": {
            "type": "pv-image-cards",
            "blocks": {
                "c1": {"type": "card", "settings": {"title": "For side sleepers", "image": "shopify://shop_images/pv-sleep-side.jpg", "text": "<p>Raised sides keep your neck aligned.</p>"}},
                "c2": {"type": "card", "settings": {"title": "For stomach sleepers", "image": "shopify://shop_images/pv-sleep-stomach.jpg", "text": "<p>Low, gentle support for head and neck.</p>"}},
                "c3": {"type": "card", "settings": {"title": "For back sleepers", "image": "shopify://shop_images/pv-sleep-back.jpg", "text": "<p>Rest your head in the center for optimal comfort.</p>"}},
            },
            "block_order": ["c1", "c2", "c3"],
            "settings": {"heading": "Made for <em>Every Sleeping</em> Position", "color_scheme": "scheme-1", "padding_top": 20, "padding_bottom": 20},
        },
        "commitment": {
            "type": "pv-media-text",
            "settings": {"heading": "Our <em>Commitment</em> to Your Wellbeing", "subheading": "",
                         "text": "<p>Your wellbeing depends on how you sleep. That's why we created Pillowvia — an ergonomic solution designed to improve your rest naturally.</p><p><strong>Less time tossing and turning, more comfort while you rest.</strong></p>",
                         "button_label": "", "button_link": "", "image": "shopify://shop_images/pv-hero-family.jpg",
                         "layout": "image-right", "card": True, "center_text": False, "color_scheme": "scheme-2", "padding_top": 20, "padding_bottom": 20},
        },
        "how": {
            "type": "pv-how",
            "blocks": {
                "s1": {"type": "step", "settings": {"title": "Rest your neck in the contour", "text": "The curved edge fills the gap under your neck and keeps it in a natural line with your spine."}},
                "s2": {"type": "step", "settings": {"title": "Pick your height", "text": "Lower center for back sleepers, higher sides for side sleepers — just rotate the pillow."}},
                "s3": {"type": "step", "settings": {"title": "Let the memory foam adapt", "text": "The foam slowly shapes to you and spreads pressure evenly, so you can relax all night."}},
            },
            "block_order": ["s1", "s2", "s3"],
            "settings": {"heading": "How <em>Pillowvia</em> Works", "media_alt_match": "alignment", "color_scheme": "scheme-1", "padding_top": 20, "padding_bottom": 20},
        },
        "compare": {
            "type": "pv-comparison",
            "blocks": {f"r{i}": {"type": "row", "settings": {"feature": f, "brand": True, "other": o}} for i, (f, o) in enumerate([
                ("Ergonomic neck contour", False), ("Two heights in one pillow", False), ("Cutouts for shoulders & arms", False),
                ("Memory foam that adapts to you", False), ("Breathable mesh sides", False), ("Removable, washable cover", True),
                ("100-night money-back guarantee", False)])},
            "block_order": [f"r{i}" for i in range(7)],
            "settings": {"heading": "Pillowvia vs. <em>a Regular Pillow</em>", "subheading": "", "brand_label": "Pillowvia", "other_label": "Regular pillow",
                         "color_scheme": "scheme-1", "padding_top": 20, "padding_bottom": 24},
        },
        "faq": faq_section(),
        "strip": strip_section(),
        "jm_reviews": {"type": "pv-judgeme-carousel", "settings": {"heading": "What Our <em>Customers Say</em>", "min_rating": 4, "min_length": 40,
                                                                    "max_reviews": 10, "color_scheme": "scheme-1", "padding_top": 24, "padding_bottom": 16}},
    },
    "order": ["main", "comments", "pain", "guarantee", "goodbye", "protect", "how", "positions", "compare", "faq", "strip", "jm_reviews"],
}

index = {
    "sections": {
        "hero": {
            "type": "pv-hero",
            "settings": {"heading": "The relief your body has been asking for", "text": "Designed for natural neck alignment — this could be the last pillow you'll ever need.",
                         "button_label": "Feel the relief now", "button_link": PRODUCT_URL, "rating_text": "100-night money-back guarantee",
                         "image": "shopify://shop_images/pv-hero-family.jpg", "color_scheme": "scheme-1", "padding_top": 24, "padding_bottom": 20},
        },
        "bestsellers": {
            "type": "pv-product-cards",
            "blocks": {"p1": {"type": "product", "settings": {"product": HANDLE, "badge": "🏆 Best seller", "rating_text": "", "tagline": "Ergonomic memory-foam neck support"}}},
            "block_order": ["p1"],
            "settings": {"heading": "Our Best Sellers for Your Wellbeing", "text": "Sleep better, wake up without stiffness.",
                         "button_label": "Shop now", "color_scheme": "scheme-2", "padding_top": 20, "padding_bottom": 20},
        },
        "guarantee": {
            "type": "pv-guarantee",
            "settings": {"style": "centered", "badge": "pv-badge-100-round.svg", "badge_alt": "100-night trial", "heading": "Try It Risk-Free for 100 Nights",
                         "text": "<p>Try it at home for <strong>100 nights</strong>. If it doesn't make a difference for you, <strong>we'll refund you</strong> — no questions asked.</p>",
                         "button_label": "", "button_link": "", "color_scheme": "scheme-1", "padding_top": 24, "padding_bottom": 16},
        },
        "experts": experts_section(),
        "reviews_carousel": reviews_section("scheme-1"),
        "help": {
            "type": "pv-media-text",
            "settings": {"heading": "Need Help?", "subheading": "",
                         "text": "<p>Questions or a problem with your order? We reply within 24 hours.</p>",
                         "button_label": "Contact us", "button_link": "shopify://pages/contact", "image": "shopify://shop_images/pv-support-team.jpg",
                         "layout": "image-left", "card": False, "center_text": True, "color_scheme": "scheme-1", "padding_top": 16, "padding_bottom": 16},
        },
        "badges": {
            "type": "pv-badges",
            "blocks": {
                "b1": {"type": "badge", "settings": {"icon": "truck", "text": "Tracked & secure delivery"}},
                "b2": {"type": "badge", "settings": {"icon": "box", "text": "Easy, fast returns"}},
                "b3": {"type": "badge", "settings": {"icon": "check_mark", "text": "Satisfied or refunded"}},
                "b4": {"type": "badge", "settings": {"icon": "chat_bubble", "text": "Friendly support"}},
            },
            "block_order": ["b1", "b2", "b3", "b4"],
            "settings": {"color_scheme": "scheme-1", "padding_top": 20, "padding_bottom": 16},
        },
    },
    "order": ["hero", "bestsellers", "guarantee", "experts", "reviews_carousel", "help", "badges"],
}

product["sections"].pop("commitment", None)
# Keep app sections added in the theme editor (e.g. Judge.me widget)
_prev = load_json("templates/product.json")
for _k in _prev.get("order", []):
    _v = _prev["sections"].get(_k, {})
    _app = any(str(b.get("type", "")).startswith("shopify://apps/") for b in _v.get("blocks", {}).values())
    if _k not in product["sections"] and _app:
        product["sections"][_k] = _v
        product["order"].append(_k)
json.dump(product, open("templates/product.json", "w"), indent=2, ensure_ascii=False)
json.dump(index, open("templates/index.json", "w"), indent=2, ensure_ascii=False)

# Header
h = load_json("sections/header-group.json")
ab = h["sections"]["announcement-bar"]
ab["settings"].update({"color_scheme": "scheme-3", "auto_rotate": True, "change_slides_speed": 5, "show_line_separator": False})
ab["blocks"] = {
    "a1": {"type": "announcement", "settings": {"text": "SALE — 50% OFF + FREE US SHIPPING", "link": PRODUCT_URL}},
    "a2": {"type": "announcement", "settings": {"text": "BUY 2 GET 1 FREE — LIMITED TIME!", "link": PRODUCT_URL}},
}
ab["block_order"] = ["a1", "a2"]
h["sections"]["header"]["settings"].update({"logo_position": "middle-left", "mobile_logo_position": "center", "menu_type_desktop": "dropdown",
                                            "show_line_separator": False, "sticky_header_type": "on-scroll-up", "padding_top": 8, "padding_bottom": 8,
                                            "enable_country_selector": False, "enable_language_selector": False})
json.dump(h, open("sections/header-group.json", "w"), indent=2, ensure_ascii=False)

# Footer
f = load_json("sections/footer-group.json")
fs = f["sections"]["footer"]
fs["settings"].update({"color_scheme": "scheme-3", "newsletter_enable": True, "newsletter_heading": "Join the Pillowvia club",
                       "enable_follow_on_shop": False, "show_social": True, "enable_country_selector": False, "enable_language_selector": False,
                       "payment_enable": True, "show_policy": True, "padding_top": 16, "padding_bottom": 24})
fs["blocks"] = {
    "logo": {"type": "image", "settings": {"image": "shopify://shop_images/pv-logo-white.png", "image_width": 190, "alignment": ""}},
    "support": {"type": "text", "settings": {"heading": "Customer support", "subtext": "<p>Fast, friendly support. We reply to every message within 24 hours on business days.</p><p>📧 <strong>pillowviastore@gmail.com</strong></p>"}},
    "help": {"type": "link_list", "settings": {"heading": "Need help?", "menu": "footer"}},
}
fs["block_order"] = ["logo", "support", "help"]
json.dump(f, open("sections/footer-group.json", "w"), indent=2, ensure_ascii=False)

s = load_json("config/settings_data.json")
s["presets"]["Dawn"].update({"body_scale": 105, "heading_scale": 105, "type_header_font": "inter_n7", "type_body_font": "inter_n4"})
json.dump(s, open("config/settings_data.json", "w"), indent=2)
print("ok", RATING_AVG, REVIEW_COUNT)
