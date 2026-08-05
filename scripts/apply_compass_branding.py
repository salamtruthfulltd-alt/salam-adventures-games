from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGO = "assets/compass-sen-support-logo.svg"
MARKER = "data-compass-hardwired-branding"

STYLE = """
<style data-compass-hardwired-branding>
.compass-brand-bar{width:min(1180px,calc(100% - 24px));margin:12px auto 18px;padding:12px 18px;background:#fff;border:1px solid #dfe8ef;border-radius:20px;box-shadow:0 8px 22px rgba(9,49,73,.08);display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;font-family:Arial,sans-serif}.compass-brand-logo{width:190px;max-width:42vw;height:auto;display:block}.compass-back-link{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:10px 18px;border:2px solid #0a98a8;border-radius:999px;color:#06365b;background:#fff;text-decoration:none;font-weight:800;font-size:16px}.compass-back-link:hover,.compass-back-link:focus{background:#eaf9fb;outline:3px solid rgba(10,152,168,.18)}.compass-copyright{width:min(1180px,calc(100% - 24px));margin:22px auto 12px;padding:14px;text-align:center;border-top:1px solid #dfe8ef;color:#31536a;font:700 13px/1.5 Arial,sans-serif;background:#fff;border-radius:16px}.compass-copyright .tagline{display:block;margin-top:4px;color:#6d3fb2;font-weight:700}@media print{.compass-back-link{display:none}.compass-brand-bar{box-shadow:none;border:none;margin:0 auto 10px}.compass-brand-logo{width:150px}.compass-copyright{box-shadow:none;border-radius:0;margin-top:12px}}@media(max-width:560px){.compass-brand-bar{justify-content:center;text-align:center}.compass-brand-logo{width:170px}.compass-back-link{width:100%}}
</style>
"""

HEADER = f"""
<header class="compass-brand-bar" {MARKER}>
  <img class="compass-brand-logo" src="{LOGO}" alt="Compass SEN Support — Guiding Every Step. Empowering Every Child.">
  <a class="compass-back-link" href="index.html" aria-label="Back to Games">← Back to Games</a>
</header>
"""

FOOTER = """
<footer class="compass-copyright" data-compass-hardwired-branding>
  © 2026 Compass SEN Support. All rights reserved.
  <span class="tagline">Guiding Every Step. Empowering Every Child.</span>
</footer>
"""

OLD_BRANDING = [
    (r"Salam Adventures", "Compass SEN Support"),
    (r"salamadventures\.com", "compasssensupport.vercel.app"),
    (r"https://salamtruthfulltd-alt\.github\.io/salam-adventures-games/(?:Salam%20Adventures\.png|salam\.png)", LOGO),
    (r"(?:\./)?addition images/logo\.png", LOGO),
    (r"/assets/salam-adventures-home\.png", LOGO),
]


def rebrand(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    for pattern, replacement in OLD_BRANDING:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Remove earlier injected Compass block before writing the canonical one.
    text = re.sub(r"<style data-compass-hardwired-branding>.*?</style>", "", text, flags=re.I | re.S)
    text = re.sub(r"<(?:header|footer)[^>]*data-compass-hardwired-branding[^>]*>.*?</(?:header|footer)>", "", text, flags=re.I | re.S)

    if "</head>" in text.lower():
        text = re.sub(r"</head>", STYLE + "\n</head>", text, count=1, flags=re.I)
    else:
        text = STYLE + text

    body_match = re.search(r"<body[^>]*>", text, flags=re.I)
    if body_match:
        insert_at = body_match.end()
        text = text[:insert_at] + "\n" + HEADER + text[insert_at:]
    else:
        text = HEADER + text

    if re.search(r"</body>", text, flags=re.I):
        text = re.sub(r"</body>", FOOTER + "\n</body>", text, count=1, flags=re.I)
    else:
        text += FOOTER

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        if rebrand(path):
            changed.append(str(path.relative_to(ROOT)))
    print(f"Branded {len(changed)} HTML files")
    for item in changed:
        print(item)


if __name__ == "__main__":
    main()
