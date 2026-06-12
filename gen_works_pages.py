#!/usr/bin/env python3
# works.json -> /works/<key>/index.html 정적 페이지 생성 (SEO용)
# 사용: python3 gen_works_pages.py   (works.json 수정 후 실행)
import json, os, html, re, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://skarte.kr"
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

def playlist_card(pl):
    return (f'<div class="work-item"><a class="vcard pl" href="https://www.youtube.com/playlist?list={pl}" '
            f'target="_blank" rel="noopener"><span class="pl-label">Playlist<br><em>전체 보기 &rarr;</em></span></a></div>')

def nav(cats, active):
    links = "".join(
        f'<a href="/works/{c["key"]}"{" aria-current=\"page\"" if c["key"]==active else ""}>{esc(c["title"])}</a>'
        for c in cats)
    return f'''<header class="nav">
  <a class="brand" href="/" aria-label="skARTe 홈">
    <svg viewBox="0 0 481 361" width="30" aria-hidden="true"><path d="{LOGO_PATH}" fill="#fff" fill-rule="evenodd"/></svg>
    <span class="bt"><b>skARTe</b><small>skartefilms</small></span>
  </a>
  <nav class="catnav" aria-label="작업 카테고리">{links}<a href="/#contact">Contact</a></nav>
</header>'''

def page(cat, cats):
    key=cat["key"]; title=esc(cat["title"])
    desc = cat.get("desc") or f'skARTe(skartefilms)의 {cat["title"]} 영상 작업. 인천 기반 영상 제작사가 기획·촬영·편집한 {cat["title"]} 포트폴리오입니다.'
    desc = esc(desc)
    url=f'{SITE}/works/{key}'
    if cat.get("soon"):
        body = '<p class="soon">업로드 예정입니다.</p>'
    else:
        items=""
        if cat.get("playlist"): items+=playlist_card(cat["playlist"])
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
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.css");
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Pretendard Variable",Pretendard,system-ui,sans-serif;background:#000;color:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.nav{{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;
  padding:14px 6vw;background:rgba(0,0,0,.86);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.1)}}
.brand{{display:flex;align-items:center;gap:11px}}
.brand .bt{{display:flex;flex-direction:column;line-height:1.05}}
.brand .bt b{{font-size:17px;font-weight:800;letter-spacing:.01em}}
.brand .bt small{{font-size:9px;letter-spacing:.22em;color:#9a9a9a;text-transform:lowercase;text-align:center}}
.catnav{{display:flex;gap:18px;flex-wrap:wrap;font-size:13px;letter-spacing:.06em}}
.catnav a{{color:#9a9a9a;padding:4px 0;transition:color .2s}}
.catnav a:hover,.catnav a[aria-current]{{color:#fff}}
main{{max-width:1180px;margin:0 auto;padding:54px 6vw 100px}}
.crumb{{font-size:12px;letter-spacing:.1em;color:#7a7a7a;margin-bottom:20px}}
.crumb a:hover{{color:#fff}}
.eyebrow{{font-size:13px;letter-spacing:.34em;color:#8a8a8a;margin-bottom:10px}}
h1{{font-size:clamp(34px,6vw,68px);font-weight:800;letter-spacing:.01em;margin-bottom:18px}}
.intro{{max-width:680px;color:#bcbcbc;font-size:15.5px;margin-bottom:46px}}
.wc-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(340px,100%),1fr));gap:20px}}
.work-item{{display:flex;flex-direction:column}}
.vcard{{position:relative;width:100%;aspect-ratio:16/9;background:#101010;border-radius:7px;overflow:hidden;cursor:pointer;display:block}}
.vcard img{{width:100%;height:100%;object-fit:cover;opacity:.86;transition:transform .5s,opacity .3s}}
.vcard:hover img{{transform:scale(1.04);opacity:1}}
.vcard .play{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:58px;height:58px;border-radius:50%;
  background:rgba(0,0,0,.55);border:1px solid rgba(255,255,255,.75)}}
.vcard .play::after{{content:"";position:absolute;left:55%;top:50%;transform:translate(-50%,-50%);
  border:9px solid transparent;border-left:15px solid #fff;border-right:0}}
.vcard iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.vcard.pl{{display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#191919,#0a0a0a);border:1px solid #2b2b2b}}
.vcard.pl .pl-label{{text-align:center;font-size:18px;font-weight:700;letter-spacing:.08em;line-height:1.7}}
.vcard.pl .pl-label em{{font-style:normal;font-size:13px;color:#9a9a9a;font-weight:500}}
.wi-title{{margin-top:13px;font-size:16px;font-weight:600}}
.wi-parts{{margin-top:5px;font-size:13px;color:#9a9a9a}}
.soon{{color:#888;letter-spacing:.2em;font-size:18px;padding:40px 0}}
footer{{border-top:1px solid rgba(255,255,255,.1);padding:40px 6vw;color:#8a8a8a;font-size:13px;text-align:center}}
footer a{{color:#cfcfcf}}
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
document.querySelectorAll('.vthumb').forEach(function(v){{
  v.addEventListener('click',function(){{
    if(v.classList.contains('on'))return; v.classList.add('on');
    v.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+v.dataset.id+'?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
  }});
}});
</script>
<script type="application/ld+json">{json.dumps(breadcrumb_ld,ensure_ascii=False)}</script>
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
    urls=[SITE+"/"]+[f"{SITE}/works/{k}" for k in keys]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for i,u in enumerate(urls):
        pr="1.0" if i==0 else "0.8"
        sm+=f'  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>\n'
    sm+='</urlset>\n'
    open(os.path.join(BASE,"sitemap.xml"),"w",encoding="utf-8").write(sm)
    print("sitemap.xml updated")

if __name__=="__main__":
    main()
