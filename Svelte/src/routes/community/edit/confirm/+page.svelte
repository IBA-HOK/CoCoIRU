<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let draft: { communityId?: string; name?: string; count?: number } = {};

  onMount(() => {
    try {
      const saved = sessionStorage.getItem('editDraft');
      if (saved) draft = JSON.parse(saved);
    } catch (e) {}
  });

  function back() { goto('/community/edit'); }
  function confirm() {
    // persist the edit - here we store into sessionStorage for demo
    try {
      const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
      const edits = JSON.parse(editsRaw);
      edits[draft.communityId || ''] = { name: draft.name, count: draft.count };
      sessionStorage.setItem('communityEdits', JSON.stringify(edits));
      sessionStorage.removeItem('editDraft');
      sessionStorage.setItem('lastEditedCommunity', draft.communityId || '');
    } catch (e) {}
    goto('/community/edit/complete');
  }
</script>

<main class="page">
  <div class="force-black-page">
  <section class="card">
    <h2>変更内容の確認</h2>
    <p><strong>コミュニティID:</strong> {draft.communityId}</p>
    <p><strong>コミュニティ名:</strong> {draft.name}</p>
    <p><strong>人数:</strong> {draft.count}</p>

    <div class="actions">
      <button class="btn" on:click={back}>戻る</button>
      <button class="btn primary" on:click={confirm}>変更を確定する</button>
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
