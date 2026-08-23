from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / 'index.html'
text = path.read_text(encoding='utf-8')

style = r'''<style id="salam-home-layout-polish">
/* Homepage visual polish only: preserve content, links and behaviour. */
@media screen {
  html,body{width:100%;max-width:none}body{overflow-x:hidden}main{width:100%;max-width:none}
  .wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer{width:min(1500px,calc(100% - 48px));max-width:none;margin-left:auto;margin-right:auto}

  /* Match the live buttons to the two buttons baked into the hero artwork. */
  .hero-actions{left:10.7%!important;bottom:8%!important;gap:20px!important;align-items:center}
  .hero-btn{min-height:90px!important;padding:24px 34px!important;border-radius:22px!important;justify-content:center;white-space:nowrap;font-size:1.3rem!important;line-height:1!important;background:#fff!important;color:#17325c!important;border:2px solid #d9e4f0!important;box-shadow:0 14px 32px rgba(29,48,86,.2)!important}
  .hero-btn:first-child{min-width:320px!important;border-color:#b9ddf6!important}
  .hero-btn:nth-child(2){min-width:290px!important}
  .hero-btn:hover{transform:translateY(-3px) scale(1.015);box-shadow:0 18px 36px rgba(29,48,86,.24)!important}
  .hero-btn.selected{color:#fff!important;background:linear-gradient(135deg,#7542ee,#5a32da)!important;border-color:transparent!important}

  /* Quick cards below hero. */
  .quick{width:min(1440px,calc(100% - 64px))!important;margin:56px auto 68px!important;gap:28px!important;padding:28px!important;border:0!important;border-radius:36px!important;background:linear-gradient(180deg,#fff,#f7fbff)!important;box-shadow:0 24px 64px rgba(31,49,92,.13)!important}
  .quick a{position:relative;overflow:hidden;min-height:190px;padding:28px 78px 28px 28px!important;border-radius:30px!important;border:2px solid rgba(45,110,160,.1)!important;background:#fff!important;box-shadow:0 14px 34px rgba(31,48,88,.1)!important;align-items:center!important}
  .quick a:after{content:'→';position:absolute;right:24px;top:50%;transform:translateY(-50%);width:48px;height:48px;display:grid;place-items:center;border-radius:50%;background:#fff;color:#183b67;font-size:1.5rem;font-weight:900;box-shadow:0 8px 22px rgba(31,48,88,.13)}
  .quick a:nth-child(1){background:linear-gradient(135deg,#e9f8ff,#f8fdff)!important;border-color:#bfe5f8!important}.quick a:nth-child(2){background:linear-gradient(135deg,#fff3d9,#fffdf7)!important;border-color:#f6d694!important}.quick a:nth-child(3){background:linear-gradient(135deg,#ffeaf3,#fff9fc)!important;border-color:#efbfd3!important}
  .quick-icon{flex:0 0 112px!important;height:112px!important;border-radius:30px!important;font-size:4rem!important;background:rgba(255,255,255,.94)!important;box-shadow:0 13px 30px rgba(31,48,88,.12)!important;border:1px solid rgba(255,255,255,.8)!important}
  .quick strong{font-size:1.62rem!important;line-height:1.15;color:#10294a}.quick span small{max-width:290px;font-size:1.08rem!important;line-height:1.5!important;margin-top:10px!important;color:#617289!important}

  /* Welcome / parent cards: much larger illustrated visual tile. */
  .welcome-grid,.parent-grid{gap:30px!important}
  .info-card{position:relative;overflow:hidden;min-height:330px;padding:34px 38px 38px!important;border:2px solid rgba(47,115,163,.1)!important;border-top:0!important;border-radius:32px!important;background:#fff!important;box-shadow:0 17px 42px rgba(31,48,88,.1)!important}
  .info-card:before{content:'';position:absolute;width:190px;height:190px;border-radius:50%;right:-65px;top:-65px;background:rgba(145,215,245,.2)}
  .welcome-grid .info-card:nth-child(1){background:linear-gradient(150deg,#eaf9f0,#fff)!important;border-color:#c7e9d3!important}.welcome-grid .info-card:nth-child(2){background:linear-gradient(150deg,#fff6dc,#fff)!important;border-color:#f3db9f!important}.welcome-grid .info-card:nth-child(3){background:linear-gradient(150deg,#e8f6ff,#fff)!important;border-color:#bfe1f6!important}
  .parent-grid .info-card:nth-child(3n+1){background:linear-gradient(150deg,#e9f8ff,#fff)!important;border-color:#c1e4f6!important}.parent-grid .info-card:nth-child(3n+2){background:linear-gradient(150deg,#fff4dc,#fff)!important;border-color:#f1d9a8!important}.parent-grid .info-card:nth-child(3n){background:linear-gradient(150deg,#ffeaf2,#fff)!important;border-color:#edc3d2!important}
  .info-card .bigicon{position:relative;z-index:1;width:100%;height:132px;display:grid;place-items:center;border-radius:27px;background:rgba(255,255,255,.88);font-size:5rem!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.9),0 12px 26px rgba(31,48,88,.09);margin-bottom:22px}
  .info-card h3{position:relative;z-index:1;font-size:1.72rem!important;margin:0 0 12px!important}.info-card p{position:relative;z-index:1;font-size:1.09rem!important;line-height:1.72!important}

  /* Activity cards: turn the tiny icon into a proper large visual panel. */
  .grid{grid-template-columns:repeat(auto-fill,minmax(310px,1fr))!important;gap:30px!important}
  .tool{position:relative;min-height:430px!important;padding:24px 30px 32px!important;border:2px solid rgba(47,115,163,.1)!important;border-radius:32px!important;box-shadow:0 16px 40px rgba(31,48,88,.1)!important;background:linear-gradient(155deg,#fff,#f9fcff)!important}
  .tool:before{height:8px!important;background:linear-gradient(90deg,#70c9ef,#9be7d1)!important}.tool:nth-child(4n+2):before{background:linear-gradient(90deg,#ffc766,#ff9f7e)!important}.tool:nth-child(4n+3):before{background:linear-gradient(90deg,#f29fc1,#f8c0d7)!important}.tool:nth-child(4n):before{background:linear-gradient(90deg,#78d2b5,#b2ead6)!important}
  .tool .icon{width:100%;height:158px;display:grid;place-items:center;border-radius:27px;background:linear-gradient(145deg,#e8f6ff,#fff);border:1px solid #cfe6f4;font-size:5.4rem!important;box-shadow:0 13px 30px rgba(31,48,88,.11);margin:4px 0 18px!important;line-height:1}
  .tool:nth-child(4n+2) .icon{background:linear-gradient(145deg,#fff0cf,#fff);border-color:#efd49e}.tool:nth-child(4n+3) .icon{background:linear-gradient(145deg,#ffe6f1,#fff);border-color:#edbfd1}.tool:nth-child(4n) .icon{background:linear-gradient(145deg,#e8f8f1,#fff);border-color:#c5e6d8}
  .tool .eyebrow{margin-top:2px!important}.tool h3{font-size:1.62rem!important;margin:9px 0 11px!important}.tool p{font-size:1.07rem!important;line-height:1.66!important}.tool .tag{padding:13px 18px!important;border-radius:16px!important;background:#fff!important;color:#214f78!important;border:1px solid #d6e6f0;box-shadow:0 7px 18px rgba(31,48,88,.08)}

  .faq details,.kind-note{border-radius:27px!important;border:2px solid #e3eaf2!important;box-shadow:0 13px 30px rgba(31,48,88,.07)!important;background:#fff!important}.faq details{padding:26px 30px!important;margin:18px 0!important}.kind-note{padding:34px!important}
  .quick a:hover,.info-card:hover,.tool:hover{transform:translateY(-7px)!important;box-shadow:0 25px 54px rgba(31,48,88,.16)!important}
}
@media screen and (max-width:980px){.hero-actions{display:none!important}}
@media screen and (max-width:800px){.wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer{width:calc(100% - 28px)}.quick{width:calc(100% - 28px)!important;margin:24px auto 40px!important;grid-template-columns:1fr!important;padding:16px!important;gap:16px!important}.quick a{min-height:145px;padding:20px 68px 20px 20px!important}.quick-icon{flex-basis:86px!important;height:86px!important;font-size:3rem!important}.grid{grid-template-columns:1fr!important;gap:20px!important}.tool{min-height:390px!important}.tool .icon{height:140px;font-size:4.6rem!important}.info-card .bigicon{height:118px;font-size:4.4rem!important}}
</style>'''

text = re.sub(r'<style id="salam-home-layout-polish">.*?</style>\s*', '', text, flags=re.S)
if '</head>' not in text:
    raise SystemExit('index.html has no </head>')
text = text.replace('</head>', style + '\n</head>', 1)
path.write_text(text, encoding='utf-8')
