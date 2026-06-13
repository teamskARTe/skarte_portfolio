import re
src=open('gen_works_pages.py').read()

# 1) page()의 CSS 블록을 STYLE 상수로 추출
m=re.search(r'<style>\n(@import.*?)\n</style>', src, re.S)
css=m.group(1)
css_plain=css.replace('{{','{').replace('}}','}')
# 상수 삽입 (SITE 정의 다음)
src=src.replace('LOGO_PATH = ', 'STYLE = r"""'+css_plain+'"""\n\nLOGO_PATH = ', 1)
# page()의 인라인 CSS를 {STYLE}로 교체
src=src.replace('<style>\n'+css+'\n</style>', '<style>\n{STYLE}\n</style>')

# 2) nav()에 About 링크 추가
src=src.replace(
  '<button id="wbtn" class="worksbtn" aria-expanded="false">WORKS <span class="caret">&#9662;</span></button>\n    <a href="/#contact">Contact</a>',
  '<button id="wbtn" class="worksbtn" aria-expanded="false">WORKS <span class="caret">&#9662;</span></button>\n    <a href="/about">About</a>\n    <a href="/#contact">Contact</a>')

# 3) about_page() 함수 추가 (page 정의 앞)
about_fn = '''def about_page(cats):
    url=SITE+"/about"
    desc="skARTe(skartefilms) 소개. 인천 기반 영상 제작사 — 자세한 소개는 추후 첨부 예정입니다."
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"About","item":url}]}
    return f\\'\\'\\'<!DOCTYPE html>
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
.intro{{{{max-width:680px;color:#bcbcbc;font-size:16px}}}}
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
function openP(){{{{wp.classList.add('show');pd.classList.add('show');wb.setAttribute('aria-expanded','true');wp.setAttribute('aria-hidden','false');}}}}
function closeP(){{{{wp.classList.remove('show');pd.classList.remove('show');wb.setAttribute('aria-expanded','false');wp.setAttribute('aria-hidden','true');}}}}
wb.addEventListener('click',function(){{{{wp.classList.contains('show')?closeP():openP();}}}});
pd.addEventListener('click',closeP);wc.addEventListener('click',closeP);
document.addEventListener('keydown',function(e){{{{if(e.key==='Escape')closeP();}}}});
</script>
<script type="application/ld+json">{json.dumps(bc,ensure_ascii=False)}</script>
</body>
</html>\\'\\'\\'

def page(cat, cats):'''
src=src.replace('def page(cat, cats):', about_fn, 1)

# 4) main(): about 페이지 생성 + sitemap 포함
src=src.replace(
  'urls=[SITE+"/"]+[f"{SITE}/works/{k}" for k in keys]',
  'open(os.path.join(BASE,"about"),"w") if False else None\n'
  '    adir=os.path.join(BASE,"about"); os.makedirs(adir,exist_ok=True)\n'
  '    open(os.path.join(adir,"index.html"),"w",encoding="utf-8").write(about_page(cats)); print("generated /about")\n'
  '    urls=[SITE+"/", SITE+"/about"]+[f"{SITE}/works/{k}" for k in keys]')

open('gen_works_pages.py','w').write(src)
print('generator: about page + nav link added')
