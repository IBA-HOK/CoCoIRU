<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { login as authLogin, setToken } from '$lib/stores/auth';

  let communityId = '';
  let password = '';
  let error = '';
  let isSubmitting = false;

  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  onMount(() => {
    try {
      const pref = sessionStorage.getItem('selectedCommunityId');
      if (pref) communityId = pref;
    } catch (e) {}
  });

  async function submit() {
    error = '';
    const id = (communityId || '').trim();
    if (!id) { error = 'コミュニティIDを入力してください'; return; }

    isSubmitting = true;

    try {
      const body = {
        user_type: 'community',
        community_id: Number(id),
        password
      };

      const res = await fetch(`${API_BASE}/api/v1/login/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(body)
      });

      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(d.detail || 'ログインに失敗しました');
      }

      // 成功: サーバーが HttpOnly Cookie をセットする
      const data = await res.json().catch(() => (null));
      if (data && data.access_token) {
        try { setToken(data.access_token); } catch (e) {}
      }
      try { sessionStorage.setItem('selectedCommunityId', id); } catch (e) {}
      try { authLogin(id); } catch (e) {}

      goto('/community/account');
    } catch (e) {
      console.error(e);
      error = e instanceof Error ? e.message : 'ログインエラー';
    } finally {
      isSubmitting = false;
    }
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:480px; width:100%">
    <h2>コミュニティにログイン</h2>
    <p>コミュニティIDとパスワードを入力してサーバー側で認証します。</p>

    <label>コミュニティID
      <input type="text" bind:value={communityId} placeholder="例: 1" />
    </label>

    <label>パスワード
      <input type="password" bind:value={password} placeholder="パスワード" />
    </label>

    {#if error}
      <div class="error">{error}</div>
    {/if}

    <div class="actions">
      <button class="btn" type="button" on:click={() => goto('/community')}>戻る</button>
      <button class="btn primary" type="button" on:click={submit} disabled={isSubmitting}>
        {isSubmitting ? '処理中...' : 'ログイン'}
      </button>
    </div>
  </section>
</main>

<style>
  .card { background: var(--card); color: var(--text); padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px var(--shadow) }
  label { display:block; margin-bottom:0.75rem }
  input[type="text"], input[type="password"] { width:100%; padding:0.5rem; border:1px solid var(--outline-sub); border-radius:4px; background: transparent; color: inherit }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid var(--outline); background: var(--card-high); color: var(--text); cursor:pointer }
  .btn.primary { background: var(--primary); border-color: var(--primary); color: var(--on-primary) }
  .error { color: var(--error); margin-top:0.5rem }
</style>
