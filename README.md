# SKARTE — Vercel 배포 가이드

완전 **정적 사이트**입니다. 폰트·로고는 HTML에 base64로 내장되어 있고, 영상은 YouTube 임베드라 **빌드 과정이 없습니다**. 그대로 올리면 끝.

> 참조하신 openviral은 Next.js + Hono + Supabase 풀스택이지만, SKARTE는 DB·API·로그인이 없어 그 스택이 필요 없습니다. Vercel/도메인 컨벤션(www→apex 리다이렉트)만 동일하게 맞춰 두었습니다.

## 폴더 구조
```
skarte-deploy/
├─ index.html        # 메인 (인트로: 로고가 위로 퇴장하는 버전)
├─ nav/index.html    # /nav 경로 (인트로: 로고가 상단바로 날아가 안착하는 버전)
├─ vercel.json       # 정적 설정 + www→apex 리다이렉트 + 보안 헤더
├─ robots.txt
└─ sitemap.xml
```

## 배포 방법 (셋 중 하나)

### A. 가장 간단 — 드래그&드롭
1. https://vercel.com/new 접속 → 로그인
2. 이 `skarte-deploy` 폴더(또는 zip)를 그대로 업로드
3. Framework Preset은 **Other**, Build Command 비움, Output Directory `.`(현재 폴더)
4. Deploy

### B. CLI
```bash
npm i -g vercel
cd skarte-deploy
vercel          # 미리보기 배포
vercel --prod   # 프로덕션 배포
```

### C. Git 연동 (권장 — 이후 push만 하면 자동 배포)
1. 이 폴더를 GitHub 저장소로 올림
2. Vercel → New Project → 저장소 Import
3. Framework Preset **Other**, Build Command 비움, Output Directory 비움(루트)
4. Deploy

## 커스텀 도메인 연결
1. Vercel → 프로젝트 → **Settings → Domains**에서 `skarte.kr` 추가
2. 도메인 등록기관(예: 가비아)에서 안내된 A/CNAME 레코드 설정
3. `www.skarte.kr`로 들어와도 `vercel.json`이 `skarte.kr`로 301 리다이렉트합니다
   - **다른 도메인을 쓸 경우** `vercel.json`의 `www.skarte.kr` / `https://skarte.kr` 두 값과 `robots.txt`·`sitemap.xml`·`index.html`의 메타 URL을 실제 도메인으로 바꿔 주세요.

## 자주 바꾸는 것

### 인트로 버전 교체
- 기본은 "위로 퇴장" 버전이 메인(`index.html`)입니다.
- "상단바로 날아가는" 버전을 메인으로 쓰려면 `nav/index.html`을 `index.html`로 복사해 덮어쓰면 됩니다.

### 대표영상 / 카테고리 영상 교체
`index.html`(과 `nav/index.html`) 안에서:
- **히어로(SKARTE 쇼릴)**: `<section class="hero">`의 `.video-bg iframe` `src`에 있는 유튜브 ID
- **카테고리 대표영상**: 각 `<section class="video-section ws" id="w-...">`의 `iframe data-src` 유튜브 ID
- **서브페이지 전체 목록**: `<script>` 안의 `const WORKS = { ... }` 객체에서 카테고리별 `videos` 배열 / `playlist` 값 수정

> 두 파일(`index.html`, `nav/index.html`)은 인트로 마무리 부분만 다르고 나머지는 동일하므로, 영상을 바꿀 땐 두 파일 모두 같은 곳을 고쳐야 합니다.

## 참고
- 작업 미리보기 환경에서는 유튜브 도메인 접근이 막혀 썸네일/영상이 비어 보였지만, 실제 배포 환경에서는 정상 재생됩니다.
- 영상이 많은 카테고리도 썸네일만 먼저 로드하고 클릭 시 재생하므로 초기 로딩이 가볍습니다.

---

## 콘텐츠 관리 (Works 어드민)

사이트는 루트의 `works.json`을 읽어 Works(카테고리·영상)를 렌더링합니다. 코드 수정 없이 이 파일만 바꾸면 됩니다.

### 어드민 페이지
- 주소: `/admin` (배포 후 `https://skarte.kr/admin`)
- 기능: 카테고리 추가/삭제/순서변경/이름·soon 설정, 재생목록 링크, 영상 추가/삭제/순서변경, 영상별 **ID(또는 링크)·행사 제목·참여 파트** 편집, 히어로 대표영상 변경
- 유튜브 전체 링크를 붙여넣어도 11자리 ID만 자동 추출됩니다.

### 편집 → 공개 반영 흐름
1. `/admin`에서 편집
2. **미리보기 저장** — 같은 브라우저에서 사이트를 열면 즉시 반영(이 브라우저에서만, localStorage)
3. **works.json 다운로드** — 받은 파일을 배포 폴더 루트의 `works.json`으로 덮어쓰고 다시 배포(git push) → **모든 방문자에게 반영**

> 즉 "편집 → 내보내기 → 배포" 방식입니다. 정적 사이트라 서버 DB가 없기 때문이며, 무료/간단합니다.

### 데이터 구조 (`works.json`)
```json
{
  "hero": "유튜브ID",
  "categories": [
    { "key": "ad", "title": "Advertisement",
      "videos": [ { "id": "유튜브ID", "title": "행사 제목", "parts": "참여 파트" } ] },
    { "key": "film", "title": "Film & Drama", "playlist": "PL...", "videos": [ ... ] },
    { "key": "live", "title": "Live Broadcast", "soon": true, "videos": [] }
  ]
}
```
- 홈 카테고리 섹션의 배경 대표영상 = 각 카테고리의 **첫 번째 영상**
- `soon:true` 카테고리는 "업로드 예정"으로 표시(배경영상 없음)
- `playlist` 가 있으면 서브페이지에 'Playlist' 카드가 추가됨

### 실시간 반영(선택)
방문자 모두에게 **즉시** 반영되게 하려면 Supabase/Vercel KV 같은 저장소가 필요합니다(정적 → 약간의 백엔드 추가). 필요하면 별도로 구성 안내 가능합니다.

### 보안 참고
`/admin`은 검색 비노출(noindex)만 적용돼 있고 URL을 아는 누구나 열 수 있습니다. 다만 어드민에서 할 수 있는 건 "내 브라우저 미리보기"와 "파일 다운로드"뿐이고, 실제 공개 반영은 저장소 push 권한이 있어야 하므로 외부인이 사이트를 바꿀 수는 없습니다. 그래도 가리고 싶으면 Vercel의 비밀번호 보호(Deployment Protection) 또는 별도 경로로 옮기는 방법이 있습니다.

---

## 카테고리 정적 페이지 (SEO)

검색 색인을 위해 카테고리마다 실제 URL 페이지가 있습니다: `/works/performance`, `/works/film`, `/works/ad`, `/works/highlight`, `/works/live`.
- 각 페이지는 고유 title·description·canonical·OG를 가지며, 영상·제목·참여파트가 HTML에 그대로 들어가 크롤러가 읽습니다.
- 홈에서 "전체 보기"/사이드바를 누르면 JS가 부드러운 오버레이로 열고 주소도 `/works/<키>`로 바뀝니다. JS가 없거나 크롤러/직접 접속이면 정적 페이지가 그대로 로드됩니다(점진적 향상).
- `sitemap.xml`에 홈 + 카테고리 URL이 포함됩니다.

### works.json을 바꾼 뒤에는 반드시 재생성
어드민에서 받은 `works.json`으로 교체했다면, 정적 페이지·사이트맵을 다시 만들어야 합니다:
```bash
cd skarte-deploy
python3 gen_works_pages.py   # /works/<키>/index.html + sitemap.xml 재생성
```
그런 다음 배포(git push)하면 정적 페이지까지 최신 내용으로 반영됩니다.

> (선택) Vercel 빌드 단계에서 이 스크립트를 자동 실행하게 만들면 수동 재생성이 필요 없습니다. 원하면 빌드 설정을 안내해 드립니다.
