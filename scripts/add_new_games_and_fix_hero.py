from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Replace any late hero-button override with a large, artwork-matching version.
s = re.sub(r'<style id="hero-button-final-tune">.*?</style>\s*', '', s, flags=re.S)
hero_css = '''<style id="hero-button-final-tune">
@media screen and (min-width:981px){
  .hero-actions{left:10.65%!important;bottom:6.4%!important;gap:22px!important;align-items:center!important}
  .hero-btn{height:88px!important;min-height:88px!important;padding:0 30px!important;border-radius:22px!important;font-size:1.28rem!important;line-height:1!important;box-shadow:0 14px 32px rgba(36,48,89,.20)!important;font-weight:900!important;white-space:nowrap!important}
  .hero-btn:first-child{width:320px!important;min-width:320px!important}
  .hero-btn:nth-child(2){width:290px!important;min-width:290px!important}
}
</style>'''
s = s.replace('</head>', hero_css + '\n</head>', 1)

new_games = [
    "['Light Chase Challenge','Light Chase Challenge.html','Games','✨']",
    "['Sound Safari','Sound Safari.html','Games','🦁']",
    "['Rocket Number Rescue','Rocket Number Rescue.html','Games','🚀']",
    "['Rainbow Reaction','Rainbow Reaction.html','Games','🌈']",
    "['Treasure Tap Quest','Treasure Tap Quest.html','Games','🗺️']",
    "['Memory Glow','Memory Glow.html','Games','🧠']",
    "['Shape Sprint','Shape Sprint.html','Games','🔷']",
    "['Star Jump Challenge','Star Jump Challenge.html','Games','⭐']",
    "['Pattern Power','Pattern Power.html','Games','🧩']",
    "['Magic Word Dash','Magic Word Dash.html','Games','📚']",
]

if "['Light Chase Challenge','Light Chase Challenge.html','Games','✨']" not in s:
    marker = "['Counting Animals Generator','Counting animals generator .html','Generators','🐘']"
    if marker not in s:
        raise SystemExit('Could not find tools array insertion marker')
    s = s.replace(marker, marker + ',' + ','.join(new_games), 1)

p.write_text(s, encoding='utf-8')

# Keep sitemap discoverable for the new pages.
sp = Path('sitemap.xml')
if sp.exists():
    sm = sp.read_text(encoding='utf-8')
    urls = [
        'Light%20Chase%20Challenge.html','Sound%20Safari.html','Rocket%20Number%20Rescue.html','Rainbow%20Reaction.html',
        'Treasure%20Tap%20Quest.html','Memory%20Glow.html','Shape%20Sprint.html','Star%20Jump%20Challenge.html','Pattern%20Power.html','Magic%20Word%20Dash.html'
    ]
    additions = ''.join(f'  <url><loc>https://www.salamadventures.com/{u}</loc></url>\n' for u in urls if u not in sm)
    if additions and '</urlset>' in sm:
        sm = sm.replace('</urlset>', additions + '</urlset>')
        sp.write_text(sm, encoding='utf-8')
