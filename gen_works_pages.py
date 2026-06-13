#!/usr/bin/env python3
# works.json -> /works/<key>/index.html 정적 페이지 생성 (SEO용)
# 사용: python3 gen_works_pages.py   (works.json 수정 후 실행)
import json, os, html, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://skarte.kr"
STYLE = r"""@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css");
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Pretendard Variable",Pretendard,system-ui,sans-serif;background:#000;color:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.nav{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;
  padding:14px 6vw;background:rgba(0,0,0,.86);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.1)}
.brand{display:flex;align-items:center;gap:11px}
.brand .bt{display:flex;flex-direction:column;line-height:1.05}
.brand .bt b{font-size:17px;font-weight:800;letter-spacing:.01em}
.brand .bt small{font-size:9px;letter-spacing:.22em;color:#9a9a9a;text-transform:lowercase;text-align:center}
@font-face{font-family:'Paperlogy';font-weight:400;font-display:swap;src:url('/fonts/Paperlogy-400.woff2') format('woff2')}
.brandname{text-transform:none}
.topnav{display:flex;align-items:center;gap:22px;font-size:13px;letter-spacing:.08em}
.topnav a{color:#9a9a9a;transition:color .2s}
.topnav a:hover{color:#fff}
.worksbtn{font:inherit;cursor:pointer;background:none;border:0;color:#fff;letter-spacing:.08em;display:flex;align-items:center;gap:7px;padding:0}
.worksbtn .caret{font-size:10px;color:#9a9a9a;transition:transform .3s}
.worksbtn[aria-expanded="true"] .caret{transform:rotate(180deg)}
.pdim{position:fixed;inset:0;z-index:55;background:rgba(0,0,0,.5);opacity:0;visibility:hidden;transition:opacity .4s,visibility .4s}
.pdim.show{opacity:1;visibility:visible}
.wpanel{position:fixed;top:0;right:0;bottom:0;z-index:60;width:min(520px,92vw);background:#fff;color:#0a0a0a;
  transform:translateX(102%);transition:transform .55s cubic-bezier(.76,0,.18,1);display:flex;flex-direction:column;overflow-y:auto}
.wpanel.show{transform:none}
.wp-head{display:flex;justify-content:space-between;align-items:flex-start;padding:34px 34px 10px}
.wp-head small{font-size:10px;letter-spacing:.4em;text-transform:uppercase;color:#999;padding-top:14px}
.wclose{background:none;border:0;cursor:pointer;font-size:30px;line-height:1;color:#0a0a0a;padding:4px 8px;font-weight:300;transition:transform .3s}
.wclose:hover{transform:rotate(90deg)}
.wp-title{font-family:'Paperlogy',sans-serif;font-weight:400;font-size:clamp(34px,6.5vw,56px);line-height:.95;letter-spacing:.01em;padding:6px 34px 28px;text-transform:uppercase}
.wp-list{display:flex;flex-direction:column;padding:0 34px 50px}
.wp-row{display:flex;align-items:center;gap:16px;padding:20px 2px;border-top:1px solid #0a0a0a;color:#0a0a0a;text-decoration:none;position:relative}
.wp-row:last-child{border-bottom:1px solid #0a0a0a}
.wp-row i{font-style:normal;font-size:10px;letter-spacing:.1em;color:#999;align-self:flex-start;padding-top:4px;min-width:18px}
.wp-row strong{font-family:'Paperlogy',sans-serif;font-weight:400;font-size:clamp(17px,3.4vw,24px);letter-spacing:.01em;line-height:1.05;flex:1;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.wp-row strong .soon{font-style:normal;font-size:11px;letter-spacing:.18em;color:#999;vertical-align:super;margin-left:6px}
.wp-row:hover strong{transform:translateX(10px)}
.wp-thumb{width:74px;height:46px;flex-shrink:0;overflow:hidden;background:radial-gradient(ellipse 90% 80% at 30% 40%, rgba(255,255,255,.25), transparent 60%),linear-gradient(150deg,#202020,#000 60%,#1a1a1a)}
.wp-row .arr{flex-shrink:0;width:22px;height:22px;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.wp-row:hover .arr{transform:translate(4px,4px)}
.wp-row .arr path{stroke:#0a0a0a;stroke-width:1.6;fill:none}
.wp-row.cur strong{text-decoration:underline;text-underline-offset:5px}
.wp-row.cur i{color:#0a0a0a}
main{max-width:1180px;margin:0 auto;padding:54px 6vw 100px}
.crumb{font-size:12px;letter-spacing:.1em;color:#7a7a7a;margin-bottom:20px}
.crumb a:hover{color:#fff}
.eyebrow{font-size:13px;letter-spacing:.34em;color:#8a8a8a;margin-bottom:10px}
h1{font-size:clamp(34px,6vw,68px);font-weight:800;letter-spacing:.01em;margin-bottom:18px}
.intro{max-width:680px;color:#bcbcbc;font-size:15.5px;margin-bottom:46px}
.wc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(340px,100%),1fr));gap:20px}
.work-item{display:flex;flex-direction:column}
.vcard{position:relative;width:100%;aspect-ratio:16/9;background:#101010;border-radius:7px;overflow:hidden;cursor:pointer;display:block}
.vcard img{width:100%;height:100%;object-fit:cover;opacity:.86;transition:transform .5s,opacity .3s}
.vcard:hover img{transform:scale(1.04);opacity:1}
.vcard .play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:58px;height:58px;border-radius:50%;
  background:rgba(0,0,0,.55);border:1px solid rgba(255,255,255,.75)}
.vcard .play::after{content:"";position:absolute;left:55%;top:50%;transform:translate(-50%,-50%);
  border:9px solid transparent;border-left:15px solid #fff;border-right:0}
.vcard iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.wi-title{margin-top:13px;font-size:16px;font-weight:600}
.wi-parts{margin-top:5px;font-size:13px;color:#9a9a9a}
.soon{color:#888;letter-spacing:.2em;font-size:18px;padding:40px 0}
footer{border-top:1px solid rgba(255,255,255,.1);padding:40px 6vw;color:#8a8a8a;font-size:13px;text-align:center}
footer a{color:#cfcfcf}"""

LOGO_PATH = "M1,1 L1,360 L200,359 L200,113 L335,360 L480,360 L285,5 L276,1 Z M227,114 L332,114 L355,159 L252,159 Z M259,175 L364,175 L387,220 L284,220 Z M292,237 L397,237 L420,282 L317,282 Z M324,298 L429,298 L452,343 L349,343 Z"

def esc(s): return html.escape(s or "", quote=True)

def card(v):
    vid = v.get("id","")
    t = esc(v.get("title",""))
    parts = esc(v.get("parts","")).replace("\n","<br>")
    title_html = f'<h3 class="wi-title">{t}</h3>' if t else ''
    parts_html = f'<p class="wi-parts">{parts}</p>' if parts else ''
    return (f'<div class="work-item"><div class="vcard vthumb" data-id="{vid}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{t or "skARTe 작업"} 영상 썸네일" loading="lazy">'
            f'<span class="play"></span></div>{title_html}{parts_html}</div>')

def nav(cats, active):
    rows = "".join(
        f'<a class="wp-row{" cur" if c["key"]==active else ""}" href="/works/{c["key"]}">'
        f'<i>{str(i+1).zfill(2)}</i><strong>{esc(c["title"])}{" <em class=\"soon\">soon</em>" if c.get("soon") else ""}</strong>'
        f'<svg class="arr" viewBox="0 0 24 24"><path d="M5 5 L19 19 M19 8 V19 H8"/></svg></a>'
        for i,c in enumerate(cats))
    return f'''<header class="nav">
  <a class="brand" href="/" aria-label="skARTe 홈">
    <svg viewBox="0 0 481 361" width="30" aria-hidden="true"><path d="{LOGO_PATH}" fill="#fff" fill-rule="evenodd"/></svg>
    <span class="bt"><b>skARTe</b><small>skartefilms</small></span>
  </a>
  <nav class="topnav" aria-label="메뉴">
    <button id="wbtn" class="worksbtn" aria-expanded="false">WORKS <span class="caret">&#9662;</span></button>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </nav>
</header>
<div id="pdim" class="pdim"></div>
<aside id="wpanel" class="wpanel" aria-hidden="true" aria-label="작업 카테고리">
  <div class="wp-head"><small><span class="brandname">skARTe</span> &mdash; Works</small><button id="wclose" class="wclose" aria-label="닫기">&times;</button></div>
  <h2 class="wp-title"><span class="brandname">skARTe</span><br>Works</h2>
  <nav class="wp-list">{rows}</nav>
</aside>'''

def video_ld(cat):
    vids=cat.get("videos",[]) if not cat.get("soon") else []
    items=[]
    for v in vids:
        vid=v.get("id","")
        if not vid: continue
        obj={
          "@type":"VideoObject",
          "name":v.get("title") or f'skARTe {cat["title"]} 영상',
          "description":v.get("parts") or cat.get("desc") or f'skARTe {cat["title"]} 작업 영상',
          "thumbnailUrl":[f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"],
          "embedUrl":f"https://www.youtube.com/embed/{vid}",
          "contentUrl":f"https://youtu.be/{vid}",
          "publisher":{"@type":"Organization","name":"skARTe","logo":{"@type":"ImageObject","url":SITE+"/icon-512.png"}}
        }
        if v.get("date"): obj["uploadDate"]=v["date"]
        items.append(obj)
    if not items: return ""
    return '<script type="application/ld+json">'+json.dumps(items,ensure_ascii=False)+'</script>'

def contact_page(cats):
    url=SITE+"/contact"
    desc="skARTe(skartefilms) 문의 — 이메일 contact@skarte.kr · 인천광역시 연수구 먼우금로 194 728호. 영상 제작 문의 환영합니다."
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Contact","item":url}]}
    org={"@context":"https://schema.org","@type":"Organization","name":"skARTe","url":SITE+"/",
         "email":"contact@skarte.kr","logo":SITE+"/icon-512.png",
         "address":{"@type":"PostalAddress","streetAddress":"먼우금로 194 728호","addressLocality":"연수구","addressRegion":"인천광역시","addressCountry":"KR"},
         "contactPoint":{"@type":"ContactPoint","contactType":"customer service","email":"contact@skarte.kr","areaServed":"KR"}}
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Contact — skARTe | 영상 제작 문의</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:site_name" content="skARTe">
<meta property="og:title" content="Contact — skARTe">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
{STYLE}
.cinfo{{margin-top:10px;display:flex;flex-direction:column;gap:26px;max-width:640px}}
.cinfo .row .k{{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:#8a8a8a;margin-bottom:8px}}
.cinfo .row .v{{font-size:clamp(18px,2.4vw,24px);color:#fff}}
.cinfo .row .v a{{text-decoration:underline;text-underline-offset:4px}}
.cinfo .row .soonv{{color:#7a7a7a;font-size:16px;letter-spacing:.04em}}
</style>
</head>
<body>
{nav(cats,None)}
<main>
  <p class="crumb"><a href="/">Home</a> &nbsp;/&nbsp; Contact</p>
  <p class="eyebrow">CONTACT</p>
  <h1>Contact</h1>
  <p class="intro">영상 제작 문의를 환영합니다. 아래로 연락 주세요.</p>
  <div class="cinfo">
    <div class="row"><div class="k">Email</div><div class="v"><a href="mailto:contact@skarte.kr">contact@skarte.kr</a></div></div>
    <div class="row"><div class="k">Address</div><div class="v">인천광역시 연수구 먼우금로 194 728호</div></div>
    <div class="row"><div class="k">Instagram</div><div class="v soonv">추후 첨부 예정입니다.</div></div>
  </div>
</main>
<footer>
  <p>skARTe · skartefilms — 인천광역시 연수구 먼우금로 194 728호 · <a href="mailto:contact@skarte.kr">contact@skarte.kr</a></p>
  <p>© skARTe 2026</p>
</footer>
<script>
var wb=document.getElementById('wbtn'),wp=document.getElementById('wpanel'),pd=document.getElementById('pdim'),wc=document.getElementById('wclose');
function openP(){{wp.classList.add('show');pd.classList.add('show');wb.setAttribute('aria-expanded','true');wp.setAttribute('aria-hidden','false');}}
function closeP(){{wp.classList.remove('show');pd.classList.remove('show');wb.setAttribute('aria-expanded','false');wp.setAttribute('aria-hidden','true');}}
wb.addEventListener('click',function(){{wp.classList.contains('show')?closeP():openP();}});
pd.addEventListener('click',closeP);wc.addEventListener('click',closeP);
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeP();}});
</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(org,ensure_ascii=False)}</script>
</body>
</html>'''

def about_page(cats):
    url=SITE+"/about"
    desc="skARTe(skartefilms) 소개. 인천 기반 영상 제작사 — 자세한 소개는 추후 첨부 예정입니다."
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"About","item":url}]}
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About — skARTe | 인천 영상 제작사</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:site_name" content="skARTe">
<meta property="og:title" content="About — skARTe">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
{STYLE}
</style>
</head>
<body>
{nav(cats,None)}
<main>
  <p class="crumb"><a href="/">Home</a> &nbsp;/&nbsp; About</p>
  <p class="eyebrow">ABOUT</p>
  <h1>About</h1>
  <p class="intro">추후 첨부 예정입니다.</p>
</main>
<footer>
  <p>skARTe · skartefilms — 인천광역시 연수구 먼우금로 194 728호 · <a href="mailto:contact@skarte.kr">contact@skarte.kr</a></p>
  <p>© skARTe 2026</p>
</footer>
<script>
var wb=document.getElementById('wbtn'),wp=document.getElementById('wpanel'),pd=document.getElementById('pdim'),wc=document.getElementById('wclose');
function openP(){{wp.classList.add('show');pd.classList.add('show');wb.setAttribute('aria-expanded','true');wp.setAttribute('aria-hidden','false');}}
function closeP(){{wp.classList.remove('show');pd.classList.remove('show');wb.setAttribute('aria-expanded','false');wp.setAttribute('aria-hidden','true');}}
wb.addEventListener('click',function(){{wp.classList.contains('show')?closeP():openP();}});
pd.addEventListener('click',closeP);wc.addEventListener('click',closeP);
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeP();}});
</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
</body>
</html>'''

def page(cat, cats):
    key=cat["key"]; title=esc(cat["title"])
    desc = cat.get("desc") or f'skARTe(skartefilms)의 {cat["title"]} 영상 작업. 인천 기반 영상 제작사가 기획·촬영·편집한 {cat["title"]} 포트폴리오입니다.'
    desc = esc(desc)
    url=f'{SITE}/works/{key}'
    if cat.get("soon"):
        body = '<p class="soon">업로드 예정입니다.</p>'
    else:
        items=""
        items+="".join(card(v) for v in cat.get("videos",[]))
        body=f'<div class="wc-grid">{items}</div>'
    others=[c for c in cats]
    breadcrumb_ld={
      "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Works","item":SITE+"/#works"},
        {"@type":"ListItem","position":3,"name":cat["title"],"item":url}]}
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — skARTe 영상 작업 | 영상 제작사</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:site_name" content="skARTe">
<meta property="og:title" content="{title} — skARTe">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>
{STYLE}
</style>
</head>
<body>
{nav(cats,key)}
<main>
  <p class="crumb"><a href="/">Home</a> &nbsp;/&nbsp; <a href="/#works">Works</a> &nbsp;/&nbsp; {title}</p>
  <p class="eyebrow">WORKS</p>
  <h1>{title}</h1>
  <p class="intro">{desc}</p>
  {body}
</main>
<footer>
  <p>skARTe · skartefilms — 인천광역시 연수구 먼우금로 194 728호 · <a href="mailto:contact@skarte.kr">contact@skarte.kr</a></p>
  <p>© skARTe 2026</p>
</footer>
<script>
var wb=document.getElementById('wbtn'),wp=document.getElementById('wpanel'),pd=document.getElementById('pdim'),wc=document.getElementById('wclose');
function openP(){{wp.classList.add('show');pd.classList.add('show');wb.setAttribute('aria-expanded','true');wp.setAttribute('aria-hidden','false');}}
function closeP(){{wp.classList.remove('show');pd.classList.remove('show');wb.setAttribute('aria-expanded','false');wp.setAttribute('aria-hidden','true');}}
wb.addEventListener('click',function(){{wp.classList.contains('show')?closeP():openP();}});
pd.addEventListener('click',closeP);wc.addEventListener('click',closeP);
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeP();}});
document.querySelectorAll('.vthumb').forEach(function(v){{
  v.addEventListener('click',function(){{
    if(v.classList.contains('on'))return; v.classList.add('on');
    v.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+v.dataset.id+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
  }});
}});
</script>
<script type="application/ld+json">{json.dumps(breadcrumb_ld,ensure_ascii=False)}</script>
{video_ld(cat)}
</body>
</html>'''

def main():
    data=json.load(open(os.path.join(BASE,"works.json"),encoding="utf-8"))
    cats=data["categories"]
    wdir=os.path.join(BASE,"works")
    if os.path.isdir(wdir): shutil.rmtree(wdir)
    keys=[]
    for c in cats:
        d=os.path.join(wdir,c["key"]); os.makedirs(d,exist_ok=True)
        open(os.path.join(d,"index.html"),"w",encoding="utf-8").write(page(c,cats))
        keys.append(c["key"]); print("generated /works/"+c["key"])
    # sitemap 갱신
    adir=os.path.join(BASE,"about"); os.makedirs(adir,exist_ok=True)
    open(os.path.join(adir,"index.html"),"w",encoding="utf-8").write(about_page(cats)); print("generated /about")
    cdir=os.path.join(BASE,"contact"); os.makedirs(cdir,exist_ok=True)
    open(os.path.join(cdir,"index.html"),"w",encoding="utf-8").write(contact_page(cats)); print("generated /contact")
    urls=[SITE+"/", SITE+"/about", SITE+"/contact"]+[f"{SITE}/works/{k}" for k in keys]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for i,u in enumerate(urls):
        pr="1.0" if i==0 else "0.8"
        sm+=f'  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n'
    sm+='</urlset>\n'
    open(os.path.join(BASE,"sitemap.xml"),"w",encoding="utf-8").write(sm)
    print("sitemap.xml updated")

if __name__=="__main__":
    main()
