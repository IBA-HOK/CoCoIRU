<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let id = '';
  onMount(() => {
    try { id = sessionStorage.getItem('lastDestroyedCommunity') || ''; } catch (e) {}
  });
  function toTop() { goto('/community'); }
</script>

<main class="page">
  <section class="card">
    <h2>コミュニティを破棄しました</h2>
    <p>コミュニティ <strong>{id}</strong> を破棄しました。</p>
    <div class="actions">
      <button class="btn primary" on:click={toTop}>トップへ戻る</button>
    </div>
  </section>
</main>

<style>
  .page { padding: 1rem; display:flex; justify-content:center }
  .card { max-width:720px; width:100%; text-align:center; background: var(--card); color: var(--text); padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px var(--shadow) }
  .actions { margin-top:1rem }
  .btn.primary { background: var(--primary); border-color: var(--primary); color: var(--on-primary) }
</style>
