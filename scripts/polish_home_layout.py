from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / 'index.html'
text = path.read_text(encoding='utf-8')

style = r'''<style id="salam-home-layout-polish">
/* Layout/card polish only: keep existing content, links and behaviour intact. */
@media screen {
  html, body { width: 100%; max-width: none; }
  body { overflow-x: hidden; }
  main { width: 100%; max-width: none; }

  .visual { width:100%; max-width:none; margin:0; border-radius:0; }
  .visual > img { display:block; width:100%; max-width:none; height:auto; }

  .wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer {
    width:min(1500px,calc(100% - 48px)); max-width:none; margin-left:auto; margin-right:auto;
  }

  /* Pull the three quick-link cards clear of the hero instead of covering it. */
  .quick {
    margin: 26px auto 42px !important;
    gap: 24px !important;
    padding: 24px !important;
    border-radius: 32px !important;
    box-shadow: 0 22px 55px rgba(31,49,92,.14) !important;
  }
  .quick a {
    min-height: 132px;
    padding: 28px 30px !important;
    border-radius: 24px !important;
    border: 1px solid #dce5f0 !important;
    box-shadow: 0 10px 28px rgba(31,48,88,.09);
  }
  .quick-icon { flex-basis:68px !important; height:68px !important; border-radius:20px !important; font-size:2rem !important; }
  .quick strong { font-size:1.35rem !important; line-height:1.2; }
  .quick span small { font-size:1rem !important; line-height:1.5 !important; margin-top:8px !important; }

  /* Upgrade all card families consistently. */
  .info-card,.tool,.faq details,.kind-note {
    border-radius: 28px !important;
    border: 1px solid #dce5f0 !important;
    box-shadow: 0 14px 36px rgba(31,48,88,.09) !important;
  }
  .info-card { padding:36px !important; min-height:245px; }
  .info-card .bigicon { font-size:3rem !important; }
  .info-card h3 { font-size:1.62rem !important; margin:18px 0 12px !important; }
  .info-card p { font-size:1.08rem !important; line-height:1.72 !important; }

  .grid { grid-template-columns:repeat(auto-fill,minmax(285px,1fr)) !important; gap:26px !important; }
  .tool { min-height:330px !important; padding:34px !important; }
  .tool .icon { font-size:3.35rem !important; }
  .tool h3 { font-size:1.52rem !important; }
  .tool p { font-size:1.06rem !important; line-height:1.68 !important; }
  .tool .tag { padding:11px 16px !important; border-radius:14px !important; }

  .faq details { padding:26px 30px !important; margin:18px 0 !important; }
  .kind-note { padding:34px !important; }

  .quick a:hover,.info-card:hover,.tool:hover {
    transform:translateY(-5px);
    box-shadow:0 22px 48px rgba(31,48,88,.15) !important;
  }
}

@media screen and (max-width:800px) {
  .wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer { width:calc(100% - 28px); }
  .quick { width:calc(100% - 28px) !important; margin:18px auto 30px !important; grid-template-columns:1fr !important; padding:14px !important; gap:14px !important; }
  .quick a { min-height:108px; padding:22px !important; }
  .grid { grid-template-columns:1fr !important; gap:18px !important; }
  .tool { min-height:270px !important; }
}
</style>'''

text = re.sub(r'<style id="salam-home-layout-polish">.*?</style>\s*', '', text, flags=re.S)
if '</head>' not in text:
    raise SystemExit('index.html has no </head>')
text = text.replace('</head>', style + '\n</head>', 1)
path.write_text(text, encoding='utf-8')
