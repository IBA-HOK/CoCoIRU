<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let id = '';
  let name = '';
  let count: number | null = null;

  onMount(() => {
    try {
      const sel = sessionStorage.getItem('selectedCommunityId');
      if (sel) id = sel;
      const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
      const edits = JSON.parse(editsRaw || '{}');
      const e = edits[id] || null;
      name = e?.name || '';
      count = typeof e?.count === 'number' ? e.count : null;
    } catch (e) {
      id = '';
      name = '';
      count = null;
    }
  });

  function toEdit() { goto('/community/edit'); }
  function toDestroy() { goto('/community/destroy/confirm'); }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:720px; width:100%">
    <h2>ログイン状態</h2>
    <p><strong>コミュニティID:</strong> {id || '—'}</p>
    <p><strong>コミュニティ名:</strong> {name || '—'}</p>
    <p><strong>人数:</strong> {count === null ? '—' : `${count} 人`}</p>

    <div class="actions">
      <button class="btn" on:click={toEdit}>コミュニティを編集</button>
      <button class="btn danger" on:click={toDestroy}>コミュニティを破棄</button>
    </div>
  </section>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.danger { background:#e74c3c; color:#fff }
</style>
