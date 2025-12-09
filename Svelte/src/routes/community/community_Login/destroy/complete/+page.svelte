<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let id = '';
  onMount(() => {
    try { id = sessionStorage.getItem('lastDestroyedCommunity') || ''; } catch (e) {}
  });
  function toTop() { goto('/community'); }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:720px; width:100%; text-align:center">
    <h2>コミュニティを破棄しました</h2>
    <p>コミュニティ <strong>{id}</strong> を破棄しました。</p>
    <div style="margin-top:1rem">
      <button class="btn primary" on:click={toTop}>トップへ戻る</button>
    </div>
  </section>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  .btn.primary { background:#2ecc71; color:#fff }
</style>
