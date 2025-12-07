<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { login as authLogin } from '$lib/stores/auth';

  let communityId = '';
  let error = '';

  onMount(() => {
    try {
      const pref = sessionStorage.getItem('selectedCommunityId');
      if (pref) communityId = pref;
    } catch (e) {}
  });

  function submit() {
    error = '';
    const id = (communityId || '').trim();
    if (!id) { error = 'コミュニティIDを入力してください'; return; }

    try { sessionStorage.setItem('selectedCommunityId', id); } catch (e) {}
    try { authLogin(id); } catch (e) {}

    goto('/community/account');
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:480px; width:100%">
    <h2>コミュニティにログイン</h2>
    <p>コミュニティIDを入力してログインしてください（デモ用、サーバー認証なし）。</p>

    <label>コミュニティID
      <input type="text" bind:value={communityId} placeholder="例: comm-abc123" />
    </label>

    {#if error}
      <div class="error">{error}</div>
    {/if}

    <div class="actions">
      <button class="btn" type="button" on:click={() => goto('/community')}>戻る</button>
      <button class="btn primary" type="button" on:click={submit}>ログイン</button>
    </div>
  </section>
</main>

<style>
  .card { background: var(--card); color: var(--text); padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px var(--shadow) }
  label { display:block; margin-bottom:0.75rem }
  input[type="text"] { width:100%; padding:0.5rem; border:1px solid var(--outline-sub); border-radius:4px; background: transparent; color: inherit }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid var(--outline); background: var(--card-high); color: var(--text); cursor:pointer }
  .btn.primary { background: var(--primary); border-color: var(--primary); color: var(--on-primary) }
  .error { color: var(--error); margin-top:0.5rem }
</style>
