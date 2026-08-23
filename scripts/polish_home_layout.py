from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / 'index.html'
text = path.read_text(encoding='utf-8')

style = r'''<style id="salam-home-layout-polish">
/* Homepage polish only: preserve content, links and behaviour. */
@media screen {
  html, body { width:100%; max-width:none; }
  body { overflow-x:hidden; }
  main { width:100%; max-width:none; }

  .wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer {
    width:min(1500px,calc(100% - 48px)); max-width:none; margin-left:auto; margin-right:auto;
  }

  /* Hero action buttons: large enough to fully cover the buttons baked into the hero artwork. */
  .hero-actions {
    left:10.7% !important;
    bottom:3.2% !important;
    gap:16px !important;
    align-items:center;
  }
  .hero-btn {
    min-width:220px !important;
    min-height:66px !important;
    padding:18px 28px !important;
    border-radius:18px !important;
    justify-content:center;
    white-space:nowrap;
    font-size:1.18rem !important;
    line-height:1 !important;
    background:#fff !important;
    color:#17325c !important;
    border:2px solid #d9e4f0 !important;
    box-shadow:0 13px 30px rgba(29,48,86,.18) !important;
  }
  .hero-btn:first-child { border-color:#b9ddf6 !important; }
  .hero-btn:hover { transform:translateY(-3px) scale(1.02); box-shadow:0 17px 34px rgba(29,48,86,.22) !important; }
  .hero-btn.selected { color:#fff !important; background:linear-gradient(135deg,#7542ee,#5a32da) !important; border-color:transparent !important; }

  /* Keep quick links completely below the hero with breathing room. */
  .quick {
    width:min(1420px,calc(100% - 64px)) !important;
    margin:52px auto 64px !important;
    gap:26px !important;
    padding:26px !important;
    border:0 !important;
    border-radius:34px !important;
    background:linear-gradient(180deg,#ffffff,#f8fbff) !important;
    box-shadow:0 24px 60px rgba(31,49,92,.13) !important;
  }
  .quick a {
    position:relative;
    overflow:hidden;
    min-height:150px;
    padding:30px 30px !important;
    border-radius:28px !important;
    border:2px solid rgba(45,110,160,.10) !important;
    background:#fff !important;
    box-shadow:0 12px 28px rgba(31,48,88,.09) !important;
  }
  .quick a:after {
    content:'→';
    position:absolute;
    right:24px;
    top:50%;
    transform:translateY(-50%);
    width:42px;
    height:42px;
    display:grid;
    place-items:center;
    border-radius:50%;
    background:#fff;
    color:#183b67;
    font-size:1.35rem;
    font-weight:900;
    box-shadow:0 8px 20px rgba(31,48,88,.12);
  }
  .quick a:nth-child(1){background:linear-gradient(135deg,#eef9ff,#f7fcff) !important;border-color:#bfe5f8 !important}
  .quick a:nth-child(2){background:linear-gradient(135deg,#fff7e8,#fffdf6) !important;border-color:#f8dda4 !important}
  .quick a:nth-child(3){background:linear-gradient(135deg,#fff1f6,#fffafd) !important;border-color:#f4c7da !important}
  .quick-icon {
    flex:0 0 78px !important;
    height:78px !important;
    border-radius:24px !important;
    font-size:2.35rem !important;
    background:#fff !important;
    box-shadow:0 10px 24px rgba(31,48,88,.10) !important;
  }
  .quick strong { font-size:1.48rem !important; line-height:1.15; color:#10294a; }
  .quick span small { max-width:260px; font-size:1.02rem !important; line-height:1.55 !important; margin-top:9px !important; color:#617289 !important; }

  /* Playful information cards. */
  .welcome-grid,.parent-grid { gap:28px !important; }
  .info-card {
    position:relative;
    overflow:hidden;
    min-height:280px;
    padding:38px !important;
    border:2px solid rgba(47,115,163,.10) !important;
    border-top:0 !important;
    border-radius:30px !important;
    background:#fff !important;
    box-shadow:0 16px 38px rgba(31,48,88,.10) !important;
  }
  .info-card:before {
    content:'';
    position:absolute;
    width:150px;
    height:150px;
    border-radius:50%;
    right:-55px;
    top:-55px;
    background:rgba(145,215,245,.18);
  }
  .welcome-grid .info-card:nth-child(1){background:linear-gradient(145deg,#f2fbf6,#fff) !important;border-color:#cdebd7 !important}
  .welcome-grid .info-card:nth-child(2){background:linear-gradient(145deg,#fffaf0,#fff) !important;border-color:#f3dfb4 !important}
  .welcome-grid .info-card:nth-child(3){background:linear-gradient(145deg,#eef8ff,#fff) !important;border-color:#c7e4f7 !important}
  .parent-grid .info-card:nth-child(3n+1){background:linear-gradient(145deg,#eef9ff,#fff) !important;border-color:#c7e5f6 !important}
  .parent-grid .info-card:nth-child(3n+2){background:linear-gradient(145deg,#fff7e9,#fff) !important;border-color:#f1ddba !important}
  .parent-grid .info-card:nth-child(3n){background:linear-gradient(145deg,#fff2f6,#fff) !important;border-color:#f0ccd9 !important}
  .info-card .bigicon {
    position:relative;
    z-index:1;
    width:76px;
    height:76px;
    display:grid;
    place-items:center;
    border-radius:24px;
    background:#fff;
    font-size:2.7rem !important;
    box-shadow:0 10px 22px rgba(31,48,88,.10);
  }
  .info-card h3 { position:relative;z-index:1;font-size:1.68rem !important;margin:20px 0 12px !important; }
  .info-card p { position:relative;z-index:1;font-size:1.08rem !important;line-height:1.72 !important; }

  /* Activity cards: larger visual icon tiles and varied child-friendly pastel surfaces. */
  .grid { grid-template-columns:repeat(auto-fill,minmax(300px,1fr)) !important; gap:28px !important; }
  .tool {
    position:relative;
    min-height:360px !important;
    padding:34px !important;
    border:2px solid rgba(47,115,163,.10) !important;
    border-radius:30px !important;
    box-shadow:0 15px 36px rgba(31,48,88,.09) !important;
    background:linear-gradient(155deg,#fff,#f9fcff) !important;
  }
  .tool:before { height:8px !important; background:linear-gradient(90deg,#73c7ef,#9ee4d0) !important; }
  .tool:nth-child(4n+2):before { background:linear-gradient(90deg,#ffc96f,#ffad87) !important; }
  .tool:nth-child(4n+3):before { background:linear-gradient(90deg,#f6a9c8,#f9c6da) !important; }
  .tool:nth-child(4n):before { background:linear-gradient(90deg,#8fdac0,#b7ead6) !important; }
  .tool .icon {
    width:84px;
    height:84px;
    display:grid;
    place-items:center;
    border-radius:25px;
    background:linear-gradient(145deg,#eef8ff,#fff);
    border:1px solid #d8eaf5;
    font-size:3rem !important;
    box-shadow:0 11px 25px rgba(31,48,88,.10);
  }
  .tool:nth-child(4n+2) .icon { background:linear-gradient(145deg,#fff4df,#fff);border-color:#f3dfb7; }
  .tool:nth-child(4n+3) .icon { background:linear-gradient(145deg,#fff0f6,#fff);border-color:#f0cfdd; }
  .tool:nth-child(4n) .icon { background:linear-gradient(145deg,#eefaf5,#fff);border-color:#cee9dc; }
  .tool .eyebrow { margin-top:18px !important; }
  .tool h3 { font-size:1.58rem !important; margin:9px 0 11px !important; }
  .tool p { font-size:1.06rem !important; line-height:1.68 !important; }
  .tool .tag {
    padding:12px 17px !important;
    border-radius:15px !important;
    background:#fff !important;
    color:#214f78 !important;
    border:1px solid #d6e6f0;
    box-shadow:0 7px 18px rgba(31,48,88,.08);
  }

  .faq details,.kind-note {
    border-radius:26px !important;
    border:2px solid #e3eaf2 !important;
    box-shadow:0 13px 30px rgba(31,48,88,.07) !important;
    background:#fff !important;
  }
  .faq details { padding:26px 30px !important; margin:18px 0 !important; }
  .kind-note { padding:34px !important; }

  .quick a:hover,.info-card:hover,.tool:hover {
    transform:translateY(-7px) !important;
    box-shadow:0 24px 52px rgba(31,48,88,.15) !important;
  }
}

@media screen and (max-width:980px) {
  .hero-actions { display:none !important; }
}

@media screen and (max-width:800px) {
  .wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer { width:calc(100% - 28px); }
  .quick { width:calc(100% - 28px) !important; margin:24px auto 38px !important; grid-template-columns:1fr !important; padding:16px !important; gap:16px !important; }
  .quick a { min-height:118px; padding:22px !important; }
  .quick a:after { right:18px; }
  .quick-icon { flex-basis:64px !important; height:64px !important; }
  .grid { grid-template-columns:1fr !important; gap:20px !important; }
  .tool { min-height:300px !important; }
}
</style>'''

text = re.sub(r'<style id="salam-home-layout-polish">.*?</style>\s*', '', text, flags=re.S)
if '</head>' not in text:
    raise SystemExit('index.html has no </head>')
text = text.replace('</head>', style + '\n</head>', 1)
path.write_text(text, encoding='utf-8')
