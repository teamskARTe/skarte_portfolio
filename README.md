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
