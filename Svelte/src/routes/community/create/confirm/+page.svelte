<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let draft: { name?: string; adults?: number; children?: number; password?: string } = {};

  onMount(() => {
    try {
      const s = sessionStorage.getItem('newCommunityDraft');
      if (s) draft = JSON.parse(s);
    } catch (e) {}
  });

  function back() { goto('/community/create/form'); }
  function create() {
    // UI-only: mark created by storing a 'selectedCommunityId' and storing details under a demo key
    try {
      const id = `comm-${Math.random().toString(36).slice(2,9)}`;
      sessionStorage.setItem('selectedCommunityId', id);
      const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
      const edits = JSON.parse(editsRaw || '{}');
      edits[id] = { name: draft.name || '', count: (draft.adults||0)+(draft.children||0) };
      sessionStorage.setItem('communityEdits', JSON.stringify(edits));
      sessionStorage.setItem('lastCreatedCommunity', id);
      sessionStorage.removeItem('newCommunityDraft');
    } catch (e) {}

    goto('/community/account');
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:720px; width:100%">
    <h2>作成内容の確認</h2>
    <p><strong>コミュニティ名:</strong> {draft.name}</p>
    <p><strong>大人:</strong> {draft.adults ?? '—'}</p>
    <p><strong>子供:</strong> {draft.children ?? '—'}</p>
    <p><strong>合計人数:</strong> {(draft.adults||0)+(draft.children||0)}</p>

    <div class="actions">
      <button class="btn" on:click={back}>戻る</button>
      <button class="btn primary" on:click={create}>コミュニティ作成</button>
    </div>
  </section>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color:#27b85a; color:#fff }
</style>
