<script lang="ts">
  import { goto } from '$app/navigation';

  function toCreate() { goto('/community/community_Login/form'); }
  function toLogin() { goto('/community/community_Login/login'); }
</script>

<main class="center" style="padding:2rem; display:flex; justify-content:center; align-items:center; min-height:60vh">
  <div>
    <div style="display:flex; gap:12px; flex-direction:column; align-items:center">
      <button class="btn primary" on:click={toCreate}>コミュニティID作成</button>
      <button class="btn" on:click={toLogin}>ログインする</button>
    </div>
  </div>
</main>

<style>
  .btn { padding:0.75rem 1rem; border-radius:8px; border:none; cursor:pointer }
  .btn.primary { background:#2ecc71; color:#fff }
</style>