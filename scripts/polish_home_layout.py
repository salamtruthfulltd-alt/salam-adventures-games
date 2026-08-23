from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / 'index.html'
text = path.read_text(encoding='utf-8')

style = r'''<style id="salam-home-layout-polish">
/* Desktop layout polish only: keep all existing content, links and behaviour intact. */
@media screen {
  html, body { width: 100%; max-width: none; }
  body { overflow-x: hidden; }
  main { width: 100%; max-width: none; }

  /* Hero/banner should span the browser, while preserving its aspect ratio. */
  .visual {
    width: 100%;
    max-width: none;
    margin: 0;
    border-radius: 0;
  }
  .visual > img {
    display: block;
    width: 100%;
    max-width: none;
    height: auto;
  }

  /* Full-width section backgrounds with a generous centred reading width. */
  .library, .welcome, .parents, .faq, footer { width: 100%; }
  .wrap,
  .welcome-grid,
  .parent-grid,
  .parents-intro,
  .kind-note,
  .faq .wrap,
  .footer {
    width: min(1500px, calc(100% - 48px));
    max-width: none;
    margin-left: auto;
    margin-right: auto;
  }

  /* Make the activity area feel substantial without stretching cards awkwardly. */
  .grid { grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
  .tool { min-height: 220px; }
}

@media screen and (max-width: 800px) {
  .wrap,
  .welcome-grid,
  .parent-grid,
  .parents-intro,
  .kind-note,
  .faq .wrap,
  .footer {
    width: calc(100% - 28px);
  }
  .grid { grid-template-columns: 1fr; gap: 14px; }
}
</style>'''

text = re.sub(r'<style id="salam-home-layout-polish">.*?</style>\s*', '', text, flags=re.S)
if '</head>' not in text:
    raise SystemExit('index.html has no </head>')
text = text.replace('</head>', style + '\n</head>', 1)
path.write_text(text, encoding='utf-8')
