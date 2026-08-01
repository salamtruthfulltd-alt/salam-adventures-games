from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://www.salamadventures.com"
SKIP = {"404.html"}

CATEGORY_WORDS = {
    "math": "maths skills, number confidence and problem solving",
    "count": "early counting, number recognition and quantity skills",
    "phon": "phonics, letter sounds and early reading confidence",
    "spell": "spelling, vocabulary and word recognition",
    "grammar": "grammar, sentence building and literacy confidence",
    "word": "vocabulary, reading and visual scanning",
    "memory": "working memory, concentration and recall",
    "attention": "attention, visual focus and concentration",
    "fine motor": "fine motor control, pencil readiness and coordination",
    "emotion": "emotional literacy, feelings recognition and communication",
    "now": "visual routines, transitions and everyday independence",
    "colour": "creativity, colour recognition and fine motor practice",
    "shape": "shape recognition, matching and early geometry",
    "science": "curiosity, observation and early science learning",
    "generator": "personalised printable learning practice",
}


def clean_title(path: Path, text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, flags=re.I | re.S)
    title = html.unescape(re.sub(r"\s+", " ", match.group(1)).strip()) if match else path.stem
    title = re.sub(r"\s*[|\-–—:]\s*Salam Adventures.*$", "", title, flags=re.I)
    title = re.sub(r"\s+", " ", title).strip(" |-–—:")
    return title or path.stem.replace("-", " ").title()


def learning_focus(title: str) -> str:
    lower = title.lower()
    for key, value in CATEGORY_WORDS.items():
        if key in lower:
            return value
    if any(word in lower for word in ("game", "climb", "catch", "racing", "puzzle", "bubbles")):
        return "playful learning, confidence, attention and problem solving"
    return "engaging practice, confidence and independent learning"


def description(title: str) -> str:
    focus = learning_focus(title)
    return (
        f"Try {title}, a free child-friendly Salam Adventures activity supporting {focus}. "
        "Designed for short, positive learning sessions at home or in educational settings."
    )


def category(title: str) -> str:
    lower = title.lower()
    if any(x in lower for x in ("math", "count", "number", "division", "addition", "times", "clock")):
        return "Mathematics"
    if any(x in lower for x in ("phon", "spell", "word", "grammar", "abc", "literacy")):
        return "Literacy"
    if any(x in lower for x in ("emotion", "now", "sen", "motor", "attention", "focus")):
        return "SEND Support"
    if any(x in lower for x in ("colour", "comic", "monster", "music", "xylophone", "certificate")):
        return "Creative Learning"
    return "Educational Game"


def replace_or_add_meta(text: str, name: str, value: str, *, prop: bool = False) -> str:
    attr = "property" if prop else "name"
    pattern = rf'<meta\s+{attr}=["\']{re.escape(name)}["\'][^>]*>'
    tag = f'<meta {attr}="{name}" content="{html.escape(value, quote=True)}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace("</head>", tag + "\n</head>", 1)


def add_or_replace_canonical(text: str, url: str) -> str:
    tag = f'<link rel="canonical" href="{html.escape(url, quote=True)}">'
    pattern = r'<link\s+rel=["\']canonical["\'][^>]*>'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace("</head>", tag + "\n</head>", 1)


def seo_page(path: Path, text: str) -> str:
    title = clean_title(path, text)
    is_home = path.name == "index.html"
    seo_title = (
        "Free Learning Games, SEN Activities & Worksheet Generators | Salam Adventures"
        if is_home
        else f"{title} | Free Learning Activity for Children | Salam Adventures"
    )
    seo_desc = (
        "Explore free child-friendly learning games, printable worksheet generators and SEN-supportive activities for literacy, maths, communication, creativity and everyday skills."
        if is_home
        else description(title)
    )
    rel = "" if is_home else quote(path.name)
    canonical = DOMAIN + ("/" if is_home else f"/{rel}")
    text = re.sub(r"<title>.*?</title>", f"<title>{html.escape(seo_title)}</title>", text, count=1, flags=re.I | re.S)
    text = replace_or_add_meta(text, "description", seo_desc)
    text = replace_or_add_meta(text, "robots", "index, follow, max-image-preview:large")
    text = replace_or_add_meta(text, "og:title", seo_title, prop=True)
    text = replace_or_add_meta(text, "og:description", seo_desc, prop=True)
    text = replace_or_add_meta(text, "og:type", "website", prop=True)
    text = replace_or_add_meta(text, "og:url", canonical, prop=True)
    text = replace_or_add_meta(text, "og:site_name", "Salam Adventures", prop=True)
    text = replace_or_add_meta(text, "twitter:card", "summary_large_image")
    text = add_or_replace_canonical(text, canonical)

    schema_type = "WebSite" if is_home else "LearningResource"
    schema = (
        '<script type="application/ld+json">'
        + '{'
        + f'"@context":"https://schema.org","@type":"{schema_type}",'
        + f'"name":{title!r},"url":{canonical!r},"description":{seo_desc!r},'
        + '"provider":{"@type":"Organization","name":"Salam Adventures","url":"https://www.salamadventures.com"},'
        + ('' if is_home else f'"educationalUse":"Practice","learningResourceType":{category(title)!r},"isAccessibleForFree":true,')
        + '"inLanguage":"en-GB"}'
        + '</script>'
    ).replace("'", '"')
    text = re.sub(r'<script type="application/ld\+json" data-salam-seo>.*?</script>', "", text, flags=re.I | re.S)
    schema = schema.replace('<script type="application/ld+json">', '<script type="application/ld+json" data-salam-seo>')
    text = text.replace("</head>", schema + "\n</head>", 1)
    return text


def upgrade_home(text: str) -> str:
    extra_css = """
.tool p{color:var(--muted);line-height:1.52;font-size:.92rem;margin:0 0 16px}.tool{min-height:235px}.eyebrow{color:var(--purple);font-size:.78rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase}.welcome{padding:50px 22px;background:linear-gradient(180deg,#fff,#f7f4ff)}.welcome-grid,.parent-grid{max-width:1180px;margin:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.welcome-card,.parent-card{border:1px solid var(--line);border-radius:22px;padding:24px;background:#fff;box-shadow:0 10px 28px rgba(43,45,90,.07)}.welcome-card h3,.parent-card h3{margin:12px 0 8px}.welcome-card p,.parent-card p{color:var(--muted);line-height:1.65;margin:0}.parents-intro{text-align:center;max-width:820px;margin:0 auto 28px}.parents-intro h2{font-size:clamp(2rem,4vw,3rem);margin:8px 0}.parents-intro p{color:var(--muted);line-height:1.7}.kind-note{max-width:1180px;margin:22px auto 0;padding:22px;border-radius:20px;background:#fff8df;border:1px solid #f2d986;line-height:1.65}.faq{padding:52px 22px;background:#fafcff}.faq .wrap{max-width:980px}.faq details{background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:12px 0}.faq summary{font-weight:900;cursor:pointer}.faq p{color:var(--muted);line-height:1.65}.footer-links{display:flex;gap:18px;flex-wrap:wrap;margin-top:15px}.footer-links a{color:#fff}@media(max-width:800px){.welcome-grid,.parent-grid{grid-template-columns:1fr}.tool{min-height:215px}}
"""
    text = text.replace("</style>", extra_css + "</style>", 1)
    welcome = """
<section class="welcome" aria-labelledby="welcome-title"><div class="parents-intro"><span class="eyebrow">A welcoming place to learn</span><h2 id="welcome-title">Small steps, bright moments and learning that feels good</h2><p>Salam Adventures gives children room to practise, explore and create without pressure. Choose a quick game, make a personalised worksheet or follow your child’s interests at their own pace.</p></div><div class="welcome-grid"><article class="welcome-card"><span aria-hidden="true">🌱</span><h3>Start where your child is</h3><p>There is no single right starting point. Pick an activity that feels achievable today and build confidence one small success at a time.</p></article><article class="welcome-card"><span aria-hidden="true">💛</span><h3>Celebrate effort</h3><p>Notice curiosity, persistence and trying again. A calm five-minute activity can be more valuable than a long session that feels difficult.</p></article><article class="welcome-card"><span aria-hidden="true">✨</span><h3>Follow their spark</h3><p>Children often learn best through favourite themes, movement, colour, sound and repetition. Let interest lead the way.</p></article></div></section>
"""
    text = text.replace('<section id="tools"', welcome + '<section id="tools"', 1)
    old_parents = re.compile(r'<section id="parents".*?</section>', re.I | re.S)
    new_parents = """
<section id="parents" class="parents"><div class="parents-intro"><span class="eyebrow">For parents and carers</span><h2>Supportive ideas for calmer, happier learning</h2><p>You know your child best. Use these activities flexibly, keep expectations kind and stop before learning becomes overwhelming.</p></div><div class="parent-grid"><article class="parent-card"><h3>Keep sessions short</h3><p>Five or ten positive minutes can build more confidence than pushing through tiredness. Finish while the activity still feels successful.</p></article><article class="parent-card"><h3>Offer choice and control</h3><p>Let your child choose between two activities, select colours or decide whether to print or play. Small choices can reduce anxiety.</p></article><article class="parent-card"><h3>Make breaks part of learning</h3><p>Movement, quiet time, a drink or sensory support are not interruptions. They help children regulate and return ready to learn.</p></article><article class="parent-card"><h3>Model without taking over</h3><p>Show one example, think aloud and then give space. Gentle prompts support independence better than correcting every step.</p></article><article class="parent-card"><h3>Repeat without apology</h3><p>Repetition builds familiarity and security. Returning to a favourite activity is valuable practice, not going backwards.</p></article><article class="parent-card"><h3>Notice the whole child</h3><p>Learning includes communication, confidence, creativity, emotional regulation and everyday independence—not only right answers.</p></article></div><div class="kind-note"><strong>A gentle reminder:</strong> activities on Salam Adventures are educational resources, not assessments or medical advice. Adapt them to your child, offer supervision where needed and seek professional guidance when you have concerns about development or wellbeing.</div><div id="about" class="kind-note"><h2>About Salam Adventures</h2><p>Salam Adventures is a free family learning space where faith, imagination and education come together. It was created to make useful activities easier to find and to help children feel capable, included and excited to learn.</p></div></section>
<section class="faq" aria-labelledby="faq-title"><div class="wrap"><span class="eyebrow">Helpful answers</span><h2 id="faq-title">Questions parents often ask</h2><details><summary>Are the games and generators free?</summary><p>Yes. Activities are available for personal and educational use unless a page clearly states otherwise.</p></details><details><summary>Are the resources suitable for children with additional needs?</summary><p>Many activities use clear visuals, repetition, adjustable levels and short tasks that may support a wide range of learners. Every child is different, so choose and adapt resources based on individual needs.</p></details><details><summary>How long should a child use an activity?</summary><p>There is no fixed time. A short, positive session is often best. Watch for signs of tiredness or frustration and offer a break.</p></details><details><summary>Can teachers and home educators use the worksheets?</summary><p>Yes, the resources may be used for personal teaching and educational practice. They must not be resold or republished as another product.</p></details></div></section>
"""
    text = old_parents.sub(new_parents, text, count=1)
    text = text.replace('<strong>Salam Adventures</strong><p class="small">', '<strong>Salam Adventures</strong><div class="footer-links"><a href="#tools">Activities</a><a href="#parents">Parent guidance</a><a href="#about">About</a><a href="mailto:hello@salamadventures.com">Contact</a></div><p class="small">', 1)

    desc_fn = """
function descriptionFor(x){const n=x[0].toLowerCase(),c=x[2];if(n.includes('phon'))return 'Build letter-sound awareness and early reading confidence through clear, playful practice.';if(n.includes('spell')||n.includes('word')||n.includes('grammar')||c==='Literacy')return 'Support vocabulary, spelling, reading and language confidence with an engaging child-friendly activity.';if(n.includes('count')||n.includes('number'))return 'Practise counting, number recognition and quantity skills in a visual, approachable way.';if(c==='Maths')return 'Strengthen maths confidence, calculation and problem-solving skills through interactive practice.';if(c==='Generators')return 'Create a personalised printable worksheet with adjustable content for home or educational use.';if(c==='Attention')return 'Encourage visual attention, working memory, concentration and careful observation.';if(c==='Communication')return 'Support understanding, vocabulary and everyday communication through clear visual learning.';if(c==='SEN')return 'A flexible visual activity designed to support confidence, routines, regulation or everyday learning.';if(c==='Creative')return 'Make, imagine and express ideas while developing creativity and fine motor confidence.';if(c==='Science')return 'Explore early science ideas through curiosity, observation and child-friendly discovery.';return 'A free child-friendly game supporting confidence, coordination, attention and learning through play.'}
"""
    text = text.replace("const aliases=", desc_fn + "const aliases=", 1)
    text = text.replace("(`${x[0]} ${x[2]}`.toLowerCase().includes(q))", "(`${x[0]} ${x[2]} ${descriptionFor(x)}`.toLowerCase().includes(q))")
    old_card = "`<a class=\"tool\" href=\"${encodeURI(x[1])}\"><span class=\"icon\">${x[3]}</span><h3>${x[0]}</h3><span class=\"tag\">${x[2]} →</span></a>`"
    new_card = "`<a class=\"tool\" href=\"${encodeURI(x[1])}\" aria-label=\"Open ${x[0]}\"><span class=\"icon\">${x[3]}</span><span class=\"eyebrow\">${x[2]}</span><h3>${x[0]}</h3><p>${descriptionFor(x)}</p><span class=\"tag\">Open activity →</span></a>`"
    text = text.replace(old_card, new_card)
    text = text.replace("<h2>All games and generators</h2><p>Choose a category above or search the complete Salam Adventures collection.</p>", "<span class=\"eyebrow\">Free learning library</span><h2>Games, generators and activities for growing minds</h2><p>Search by skill or explore the full collection. Every card now explains what the activity supports before you open it.</p>")
    return text


def write_support_files(pages: list[Path]) -> None:
    urls = [DOMAIN + "/"]
    urls.extend(DOMAIN + "/" + quote(p.name) for p in pages if p.name != "index.html")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join(f"  <url><loc>{html.escape(url)}</loc><changefreq>{'weekly' if url.endswith('/') else 'monthly'}</changefreq></url>" for url in urls)
    sitemap += "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://www.salamadventures.com/sitemap.xml\n", encoding="utf-8")


def main() -> None:
    pages = sorted(p for p in ROOT.glob("*.html") if p.name not in SKIP)
    for path in pages:
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.name == "index.html":
            text = upgrade_home(text)
        text = seo_page(path, text)
        path.write_text(text, encoding="utf-8")
    write_support_files(pages)


if __name__ == "__main__":
    main()
