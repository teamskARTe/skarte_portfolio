-- ============================================================
-- SKARTE Film 포트폴리오 — Supabase 스키마
-- Supabase 대시보드 > SQL Editor 에 붙여넣고 RUN 하세요.
-- ============================================================

-- 1) 사이트 데이터 저장용 key-value 테이블
--    works 데이터 전체(JSON)를 하나의 행에 저장합니다. key = 'works'
create table if not exists public.site_data (
  key         text primary key,
  value       jsonb not null,
  updated_at  timestamptz not null default now()
);

-- 2) updated_at 자동 갱신 트리거
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists trg_site_data_touch on public.site_data;
create trigger trg_site_data_touch
  before update on public.site_data
  for each row execute function public.touch_updated_at();

-- 3) RLS(Row Level Security) 활성화
alter table public.site_data enable row level security;

-- 4) 정책
--    (a) 누구나 읽기 가능 (공개 사이트가 anon key 로 works 를 읽어야 하므로)
drop policy if exists "public read site_data" on public.site_data;
create policy "public read site_data"
  on public.site_data for select
  using (true);

--    (b) 쓰기는 로그인한(authenticated) 사용자만 가능
--        => 관리자 페이지에서 Supabase Auth 로 로그인한 경우에만 저장됨
drop policy if exists "authenticated write site_data" on public.site_data;
create policy "authenticated write site_data"
  on public.site_data for all
  using (auth.role() = 'authenticated')
  with check (auth.role() = 'authenticated');

-- ============================================================
-- [선택·권장] 이메일 화이트리스트로 쓰기 제한 (서버 방어선)
-- ------------------------------------------------------------
-- 위 (b) 정책은 "로그인한 누구나" 쓰기가 됩니다. 단일 관리자 서비스라면
-- '지정한 관리자 이메일'만 쓰기 가능하게 좁히는 것을 권장합니다.
-- 이렇게 하면 관리자 이메일이 클라이언트 코드에 없어도(서버 정책에만 존재)
-- 권한 통제가 됩니다.
--
-- 사용법: 위 (b) 블록 대신 아래를 실행하세요. (이메일을 관리자 것으로 교체)
-- ------------------------------------------------------------
-- drop policy if exists "authenticated write site_data" on public.site_data;
-- drop policy if exists "whitelist write site_data" on public.site_data;
-- create policy "whitelist write site_data"
--   on public.site_data for all
--   using (
--     auth.role() = 'authenticated'
--     and lower(auth.jwt() ->> 'email') in ('admin@skarte.kr')
--   )
--   with check (
--     auth.role() = 'authenticated'
--     and lower(auth.jwt() ->> 'email') in ('admin@skarte.kr')
--   );
-- 여러 명이면: in ('a@skarte.kr','b@skarte.kr')
-- ============================================================

-- ============================================================
-- 참고:
--  - anon(공개) 키로는 읽기만 됩니다. 안전합니다.
--  - 관리자 저장은 Supabase Auth 로그인 후 authenticated 키로 동작합니다.
--  - 관리자 계정은 Supabase 대시보드 > Authentication > Users 에서
--    이메일/비밀번호로 1개 생성하세요. (예: skartefilm@naver.com)
-- ============================================================
