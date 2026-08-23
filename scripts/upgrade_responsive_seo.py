from pathlib import Path
from urllib.parse import quote
import re, json

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://www.salamadventures.com'

GAME_HINTS = ('game','count','math','memory','puzzle','bubble','shape','star','treasure','clash','racing','whack','balloon','sky','lion','emoji','phonics explorer','spellclimb','quick recall','division','addition','times tables','science')
EXCLUDE_HINTS = ('generator','worksheet','certificate','colouring','coloring','now and next','spot and circle','fine motor','literacy.html','index.html')

RESPONSIVE = r'''<style id="salam-responsive-2026">
/* Shared device compatibility: phone, tablet/iPad and desktop. */
html,body{max-width:100%;overflow-x:hidden}*{box-sizing:border-box}
img,svg,video{max-width:100%;height:auto}
canvas{max-width:100%!important;height:auto!important;touch-action:manipulation}
button,a,input,select,textarea{touch-action:manipulation}
@media (max-width:820px){
 body{min-width:0!important}
 button,a[role="button"],input,select{min-height:44px}
 canvas{width:100%!important}
}
</style>'''

GAME_SIZE = r'''<style id="salam-game-size-2026">
/* Larger game stage without changing game logic. */
@media (min-width:981px){
 .game-card,.game-container,.game-shell,.game-wrap,.play-area{width:min(1180px,94vw)!important;max-width:1180px!important;margin-left:auto!important;margin-right:auto!important}
 .game-card{padding:24px!important}
 #aquarium,.arena,.game-board,.board,#gameBoard,#game-board{min-height:520px!important}
}
@media (min-width:700px) and (max-width:980px){
 .game-card,.game-container,.game-shell,.game-wrap,.play-area{width:min(900px,94vw)!important;max-width:94vw!important;margin-left:auto!important;margin-right:auto!important}
 #aquarium,.arena,.game-board,.board,#gameBoard,#game-board{min-height:460px!important}
}
@media (max-width:699px){
 .game-card,.game-container,.game-shell,.game-wrap,.play-area{width:calc(100% - 20px)!important;max-width:none!important;margin:10px auto!important;padding:14px!important}
 #aquarium,.arena,.game-board,.board,#gameBoard,#game-board{width:100%!important;min-height:390px!important;height:auto;max-height:72vh}
}
</style>'''

def title_from(text, path):
    m = re.search(r'<title>(.*?)</title>', text, flags=re.I|re.S)
    if m:
        t = re.sub(r'\s+', ' ', m.group(1)).strip()
        return t.split('|')[0].strip() or path.stem
    return path.stem.replace('-', ' ').replace('_', ' ').strip()

def is_game(path):
    n = path.name.lower()
    if any(x in n for x in EXCLUDE_HINTS): return False
    return any(x in n for x in GAME_HINTS)

def description_for(name, game):
    if game:
        return f'Play {name}, a free child-friendly Salam Adventures learning game with interactive practice, clear goals and engaging play for children at home or in educational settings.'
    return f'Explore {name} on Salam Adventures, a free child-friendly learning resource for home and educational use, designed to support confident, positive learning.'

def canonical(path):
    if path.name.lower() == 'index.html': return SITE + '/'
    return SITE + '/' + quote(path.name)

def ensure_meta(text, path, game):
    name = title_from(text, path)
    desc = description_for(name, game)
    url = canonical(path)
    if not re.search(r'<meta[^>]+name=["\']viewport["\']', text, re.I):
        text = re.sub(r'(<head[^>]*>)', r'\1\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">', text, count=1, flags=re.I)
    if not re.search(r'<meta[^>]+name=["\']description["\']', text, re.I):
        text = re.sub(r'(</title>)', r'\1\n<meta name="description" content="'+desc.replace('"','&quot;')+'">', text, count=1, flags=re.I)
    if not re.search(r'<meta[^>]+name=["\']robots["\']', text, re.I):
        text = re.sub(r'(</title>)', r'\1\n<meta name="robots" content="index, follow, max-image-preview:large">', text, count=1, flags=re.I)
    if not re.search(r'<link[^>]+rel=["\']canonical["\']', text, re.I):
        text = re.sub(r'(</head>)', f'<link rel="canonical" href="{url}">\n\\1', text, count=1, flags=re.I)
    if 'data-salam-seo' not in text:
        schema = {"@context":"https://schema.org","@type":"VideoGame" if game else "LearningResource","name":name,"url":url,"description":desc,"isAccessibleForFree":True,"inLanguage":"en-GB","publisher":{"@type":"Organization","name":"Salam Adventures","url":SITE}}
        block = '<script type="application/ld+json" data-salam-seo>'+json.dumps(schema, ensure_ascii=False)+'</script>'
        text = re.sub(r'(</head>)', block+'\n\\1', text, count=1, flags=re.I)
    return text

def inject_style(text, style, style_id):
    text = re.sub(rf'<style id="{re.escape(style_id)}">.*?</style>\s*', '', text, flags=re.I|re.S)
    return re.sub(r'(</head>)', style+'\n\\1', text, count=1, flags=re.I)

changed=[]
for path in ROOT.glob('*.html'):
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '<html' not in text.lower() or '<head' not in text.lower():
        continue
    game = is_game(path)
    new = ensure_meta(text, path, game)
    new = inject_style(new, RESPONSIVE, 'salam-responsive-2026')
    if game:
        new = inject_style(new, GAME_SIZE, 'salam-game-size-2026')
    if path.name == 'index.html':
        home_style = '''<style id="salam-home-card-size-2026">\n@media(min-width:1100px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))!important}.tool{min-height:500px!important}.tool .icon{height:190px!important;font-size:6rem!important}}\n@media(min-width:700px) and (max-width:1099px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}.tool{min-height:460px!important}}\n</style>'''
        new = inject_style(new, home_style, 'salam-home-card-size-2026')
    if new != text:
        path.write_text(new, encoding='utf-8')
        changed.append(path.name)
print(f'Updated {len(changed)} HTML pages')
for n in changed: print(n)
