<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let id = '';
  let password = '';

  onMount(() => {
    try { id = sessionStorage.getItem('selectedCommunityId') || ''; } catch (e) {}
  });

  function destroy() {
    // UI-only: clear selectedCommunityId and mark destroyed
    try {
      sessionStorage.removeItem('selectedCommunityId');
      sessionStorage.setItem('lastDestroyedCommunity', id);
    } catch (e) {}
    goto('/community/destroy/complete');
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:720px; width:100%">
    <h2>コミュニティを破棄しますか？</h2>
    <p>本当に破棄しますか？この操作は取り消せません。</p>

    <label>コミュニティパスワード
      <input type="password" bind:value={password} placeholder="パスワードを入力" />
    </label>

    <div class="actions">
      <button class="btn" on:click={() => goto('/community/account')}>戻る</button>
      <button class="btn danger" on:click={destroy} disabled={!password}>破棄する</button>
    </div>
  </section>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  label { display:block; margin-bottom:0.75rem }
  input { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.danger { background:#e74c3c; color:#fff }
</style>
