<script lang="ts">
  import { goto } from '$app/navigation';
  import { createEventDispatcher } from 'svelte';

  // Reuse the create form UI (UI-only). Use a single 'count' for total members.
  let name = '';
  let count: number = 0;
  let password = '';
  const dispatch = createEventDispatcher();

  function toConfirm() {
    const draft = { name, count, password };
    try { sessionStorage.setItem('newCommunityDraft', JSON.stringify(draft)); } catch (e) {}
    goto('/community/community_Login/confirm');
  }
  function back() { goto('/community'); }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <div class="force-black-text">
  <section class="card" style="max-width:720px; width:100%">
    <h2>コミュニティ作成フォーム</h2>

    <label>コミュニティ名
      <input type="text" bind:value={name} placeholder="コミュニティ名を入力" />
    </label>

    <label>人数
      <input type="number" bind:value={count} min="0" />
    </label>

    <label>コミュニティパスワード
      <input type="password" bind:value={password} placeholder="任意のパスワード" />
    </label>

    <div class="actions">
      <button class="btn" on:click={() => dispatch('back')}>戻る</button>
      <button class="btn primary" on:click={toConfirm} disabled={!name.trim()}>確認へ</button>
    </div>
  </section>
  </div>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  label { display:block; margin-bottom:0.75rem }
  input { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color:#27b85a; color:#fff }
</style>
