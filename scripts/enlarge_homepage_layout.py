from pathlib import Path
import re

p = Path(__file__).resolve().parents[1] / 'index.html'
text = p.read_text(encoding='utf-8')

# Remove any previous homepage sizing override added by this helper.
text = re.sub(r'\n?<style id="salam-homepage-sizing">.*?</style>\n?', '\n', text, flags=re.S)

style = r'''<style id="salam-homepage-sizing">
/* Larger, easier-to-read homepage sizing without changing content or behaviour */
@media screen and (min-width: 981px){
  .welcome,.library,.parents,.faq{padding:78px 34px!important;}
  .wrap,.welcome-grid,.parent-grid,.parents-intro,.kind-note,.faq .wrap,.footer{
    width:min(1540px,calc(100% - 36px))!important;
  }
  .parents-intro{max-width:1120px!important;margin-bottom:42px!important;}
  .parents-intro h2,.head h2{font-size:clamp(2.7rem,4.6vw,4.35rem)!important;line-height:1.08!important;}
  .parents-intro p,.head p{font-size:1.22rem!important;line-height:1.72!important;}
  .eyebrow{font-size:.95rem!important;}
  .welcome-grid,.parent-grid{gap:28px!important;}
  .welcome-card,.parent-card{padding:34px!important;border-radius:28px!important;min-height:220px;}
  .welcome-card h3,.parent-card h3{font-size:1.55rem!important;margin:16px 0 11px!important;}
  .welcome-card p,.parent-card p{font-size:1.08rem!important;line-height:1.68!important;}
  .welcome-card>span{font-size:2.25rem;}
  .head{margin-bottom:34px!important;}
  .controls{gap:18px!important;margin-bottom:34px!important;}
  .search{padding:19px 21px!important;font-size:1.08rem!important;}
  .filter{padding:13px 18px!important;font-size:1rem!important;}
  .grid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))!important;gap:25px!important;}
  .tool{padding:29px!important;min-height:285px!important;border-radius:26px!important;}
  .icon{font-size:3rem!important;}
  .tool h3{font-size:1.42rem!important;line-height:1.3!important;margin:15px 0 10px!important;}
  .tool p{font-size:1.05rem!important;line-height:1.62!important;margin-bottom:20px!important;}
  .tag{font-size:1rem!important;}
  #count{font-size:1.1rem;}
  .kind-note{padding:30px!important;font-size:1.08rem!important;}
  .kind-note h2{font-size:2rem;}
  .faq .wrap{max-width:1280px!important;}
  .faq #faq-title{font-size:clamp(2.5rem,4vw,3.8rem);margin:10px 0 28px;}
  .faq details{padding:24px 26px!important;margin:16px 0!important;border-radius:20px!important;}
  .faq summary{font-size:1.18rem!important;}
  .faq p{font-size:1.06rem!important;}
  footer{padding:48px 34px!important;}
  .footer{font-size:1.08rem;}
  .small{font-size:1rem!important;}
}
@media screen and (min-width: 1400px){
  .grid{grid-template-columns:repeat(4,minmax(0,1fr))!important;}
}
</style>'''

text = text.replace('</head>', style + '\n</head>', 1)
p.write_text(text, encoding='utf-8')
