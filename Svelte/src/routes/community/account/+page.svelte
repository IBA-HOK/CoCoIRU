<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let id = '';
  let name = '';
  let count: number | null = null;
  let isLoading = false;
  let error = '';
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  onMount(() => {
    try {
      const sel = sessionStorage.getItem('selectedCommunityId');
      if (sel) {
        id = sel;
        // fetch latest community data from backend only if id is numeric
        const numericMatch = String(id).match(/^\d+$/);
        if (numericMatch) {
          fetchCommunity(Number(id));
        }
      }
      // fallback: read cached edits if present
      const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
      const edits = JSON.parse(editsRaw || '{}');
      const e = edits[id] || null;
      if (!name) name = e?.name || '';
      if (count === null) count = typeof e?.count === 'number' ? e.count : null;
    } catch (e) {
      id = '';
      name = '';
      count = null;
    }
  });

  async function fetchCommunity(itemId: number) {
    if (!itemId) return;
    isLoading = true;
    error = '';
    try {
      const res = await fetch(`${API_BASE}/api/v1/communities/${itemId}`, {
        method: 'GET',
        credentials: 'include'
      });

      if (!res.ok) {
        // if unauthorized or not found, clear values
        if (res.status === 401 || res.status === 403) {
          error = '認証が必要です。ログインしてください。';
        } else if (res.status === 404) {
          error = 'コミュニティが見つかりません';
        } else {
          const d = await res.json().catch(() => ({}));
          error = d.detail || 'コミュニティ情報の取得に失敗しました';
        }
        name = '';
        count = null;
        return;
      }

      const data = await res.json();
      name = data.name || '';
      // db schema uses member_count
      count = typeof data.member_count === 'number' ? data.member_count : (typeof data.member_id === 'number' ? data.member_id : null);

      // cache a lightweight copy for offline/faster load
      try {
        const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
        const edits = JSON.parse(editsRaw || '{}');
        edits[String(itemId)] = { name, count };
        sessionStorage.setItem('communityEdits', JSON.stringify(edits));
      } catch (e) {}
    } catch (e) {
      console.error(e);
      error = e instanceof Error ? e.message : '通信エラー';
    } finally {
      isLoading = false;
    }
  }

  function toEdit() { goto('/community/edit'); }
  function toDestroy() { goto('/community/destroy/confirm'); }
  function toNearby() { goto('/community/nearby'); }
  function toRequest() { goto('/community/request'); }
  function doLogout() {
    if (!confirm('ログアウトしますか？')) return;
    try { sessionStorage.removeItem('selectedCommunityId'); } catch (e) {}
    try { sessionStorage.removeItem('editDraft'); } catch (e) {}
    try { sessionStorage.removeItem('newCommunityDraft'); } catch (e) {}
    id = '';
    name = '';
    count = null;
    goto('/community');
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <div class="force-black-text">
  <section class="card" style="max-width:720px; width:100%">
    <h2>ログイン状態</h2>
    <p><strong>コミュニティID:</strong> {id || '—'}</p>
    <p><strong>コミュニティ名:</strong> {name || '—'}</p>
    <p><strong>人数:</strong> {count === null ? '—' : `${count} 人`}</p>

    <div class="actions">
      <button class="btn" on:click={toEdit}>コミュニティを編集</button>
      <button class="btn danger" on:click={toDestroy}>コミュニティを破棄</button>
      <button class="btn" on:click={doLogout}>ログアウト</button>
    </div>

    <div class="nav-links">
      <h3>メニュー</h3>
      <ul>
        <li><button class="link-btn" on:click={toNearby}>近くのコミュニティ</button></li>
        <li><button class="link-btn" on:click={toRequest}>支援リクエスト</button></li>
      </ul>
    </div>
  </section>
  </div>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.danger { background:#e74c3c; color:#fff }
  .nav-links { margin-top:1.5rem; border-top:1px solid #eee; padding-top:1rem }
  .nav-links h3 { margin-bottom:0.5rem; font-size:1.1rem }
  .nav-links ul { list-style:none; padding:0; margin:0 }
  .nav-links li { margin-bottom:0.5rem }
  .link-btn { padding:0.5rem 0.75rem; border:none; background:none; color:#007bff; text-decoration:underline; cursor:pointer; font-size:1rem }
  .link-btn:hover { color:#0056b3 }
  /* 非操作テキストを黒にする（見出し・段落など）。ボタンは上書きしない */
  .force-black-text h1,
  .force-black-text h2,
  .force-black-text h3,
  .force-black-text h4,
  .force-black-text h5,
  .force-black-text h6,
  .force-black-text p,
  .force-black-text span,
  .force-black-text li,
  .force-black-text label,
  .force-black-text strong,
  .force-black-text em,
  .force-black-text td,
  .force-black-text th {
    color: #000 !important;
  }
</style>
