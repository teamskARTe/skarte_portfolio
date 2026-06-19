/* =====================================================================
   SKARTE Film — Supabase 설정 (공개 사이트 + 관리자 공용)
   ---------------------------------------------------------------------
   ▶ 아래 두 값을 본인 프로젝트 값으로 교체하세요.
     Supabase 대시보드 > Project Settings > Data API (또는 API)
       - Project URL      → SUPABASE_URL
       - anon public key  → SUPABASE_ANON_KEY
   ▶ anon 키는 공개되어도 안전합니다 (RLS 로 쓰기를 막아둠).
   ===================================================================== */
window.SKARTE_SUPABASE = {
  url:  "https://YOUR-PROJECT-ref.supabase.co",
  anon: "YOUR-ANON-PUBLIC-KEY",
  // works 데이터를 저장하는 site_data 테이블의 key
  worksKey: "works"
};

/* ---------------------------------------------------------------------
   경량 Supabase REST 헬퍼 (SDK 없이 fetch 만 사용).
   - loadWorksFromCloud(): 공개 사이트가 works 를 읽음 (anon, 읽기 전용)
   - saveWorksToCloud(data, accessToken): 관리자가 저장 (로그인 토큰 필요)
   - signIn(email, password): 관리자 로그인 → access_token 반환
   --------------------------------------------------------------------- */
(function () {
  var CFG = window.SKARTE_SUPABASE;
  var configured =
    CFG && CFG.url.indexOf("YOUR-PROJECT") === -1 && CFG.anon.indexOf("YOUR-ANON") === -1;

  CFG.isConfigured = function () { return configured; };

  // works 한 행 읽기 (public read)
  CFG.loadWorks = async function () {
    if (!configured) return null;
    try {
      var url = CFG.url + "/rest/v1/site_data?key=eq." +
                encodeURIComponent(CFG.worksKey) + "&select=value";
      var r = await fetch(url, {
        headers: { apikey: CFG.anon, Authorization: "Bearer " + CFG.anon },
        cache: "no-store"
      });
      if (!r.ok) return null;
      var rows = await r.json();
      return (rows && rows[0] && rows[0].value) ? rows[0].value : null;
    } catch (e) { return null; }
  };

  // works 한 행 upsert (관리자 로그인 토큰 필요)
  CFG.saveWorks = async function (value, accessToken) {
    if (!configured) throw new Error("Supabase 설정이 비어 있습니다.");
    if (!accessToken) throw new Error("로그인이 필요합니다.");
    var url = CFG.url + "/rest/v1/site_data?on_conflict=key";
    var r = await fetch(url, {
      method: "POST",
      headers: {
        apikey: CFG.anon,
        Authorization: "Bearer " + accessToken,
        "Content-Type": "application/json",
        Prefer: "resolution=merge-duplicates,return=minimal"
      },
      body: JSON.stringify({ key: CFG.worksKey, value: value })
    });
    if (!r.ok) {
      var t = await r.text();
      throw new Error("저장 실패 (" + r.status + "): " + t);
    }
    return true;
  };

  // 관리자 로그인 (Supabase Auth, 이메일+비번) → access_token
  CFG.signIn = async function (email, password) {
    if (!configured) throw new Error("Supabase 설정이 비어 있습니다.");
    var url = CFG.url + "/auth/v1/token?grant_type=password";
    var r = await fetch(url, {
      method: "POST",
      headers: { apikey: CFG.anon, "Content-Type": "application/json" },
      body: JSON.stringify({ email: email, password: password })
    });
    var j = await r.json();
    if (!r.ok) throw new Error(j.error_description || j.msg || "로그인 실패");
    return j; // { access_token, refresh_token, user, ... }
  };
})();
