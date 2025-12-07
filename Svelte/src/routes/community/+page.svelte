<script lang="ts">
  import { goto } from '$app/navigation';

  function toCreate() { goto('/community/create'); }
</script>

<main class="center" style="padding:2rem; display:flex; justify-content:center; align-items:center; min-height:60vh">
  <div>
    <button class="btn primary" on:click={toCreate}>コミュニティID作成</button>
  </div>
</main>

<style>
  .btn { padding:0.75rem 1rem; border-radius:8px; border:none; cursor:pointer }
  .btn.primary { background:#2ecc71; color:#fff }
</style>