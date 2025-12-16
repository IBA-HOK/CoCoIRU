<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let draft: { communityId?: string; name?: string; count?: number; password?: string } = {};
  let isSubmitting = false;
  let error = '';
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  onMount(() => {
    try {
      const saved = sessionStorage.getItem('editDraft');
      if (saved) draft = JSON.parse(saved);
    } catch (e) {}
  });

  function back() { goto('/community/community_Login/edit'); }
  async function confirm() {
    // send update to backend
    error = '';
    if (!draft.communityId) { error = 'コミュニティIDが不明です'; return; }
    isSubmitting = true;
    try {
      const body: any = { name: draft.name || '', password: draft.password || '', member_count: draft.count };
      const res = await fetch(`${API_BASE}/api/v1/communities/${draft.communityId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(body)
      });

      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(d.detail || `更新が失敗しました (status=${res.status})`);
      }

      // update local cache and clear draft
      try {
        const data = await res.json().catch(() => ({}));
        const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
        const edits = JSON.parse(editsRaw || '{}');
        edits[draft.communityId || ''] = { name: data.name || draft.name, count: draft.count };
        sessionStorage.setItem('communityEdits', JSON.stringify(edits));
        sessionStorage.removeItem('editDraft');
        sessionStorage.setItem('lastEditedCommunity', draft.communityId || '');
      } catch (e) {}

      goto('/community/community_Login/edit/complete');
    } catch (e) {
      console.error(e);
      error = e instanceof Error ? e.message : '更新エラー';
    } finally {
      isSubmitting = false;
    }
  }
</script>

<main class="page">
  <div class="force-black-page">
  <section class="card">
    <h2>変更内容の確認</h2>
    <p><strong>コミュニティID:</strong> {draft.communityId}</p>
    <p><strong>コミュニティ名:</strong> {draft.name}</p>
    <p><strong>人数:</strong> {draft.count}</p>

    {#if error}
      <div class="result error">
        <h3>❌ エラー</h3>
        <p>{error}</p>
      </div>
    {/if}

    <div class="actions">
      <button class="btn" on:click={back} disabled={isSubmitting}>戻る</button>
      <button class="btn primary" on:click={confirm} disabled={isSubmitting}>
        {isSubmitting ? '更新中...' : '変更を確定する'}
      </button>
    </div>
  </section>
  </div>
</main>

<style>
  .page { padding: 1rem; display: flex; justify-content: center; }
  .card { width: 100%; max-width: 720px; background: #fff; border-radius: 8px; padding: 1.25rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  label { display:block; margin-bottom:0.75rem }
  input[type="text"], input[type="number"] { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color: #27b85a; color:white }
  .force-black-page, .force-black-page * { color: #000 !important; }
  .force-black-page .btn.primary { color: #fff !important; }
</style>
