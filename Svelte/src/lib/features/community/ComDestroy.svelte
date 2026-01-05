<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';
  import { goto } from '$app/navigation';
  import { Button } from '$lib';

  let id = '';
  let password = '';
  let error = '';
  let isComplete = false; 
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';
  const dispatch = createEventDispatcher();
  

  onMount(() => {
    try {
      id = sessionStorage.getItem('selectedCommunityId') || '';

    } catch (e) {}
  });

  async function destroy() {
    error = '';
    // 1) validate credentials via API
    try {
      const payload = {
        user_type: 'community',
        community_id: Number(id),
        password
      };

      const vres = await fetch(`${API_BASE}/api/v1/validate/validate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!vres.ok) {
        const d = await vres.json().catch(() => ({}));
        throw new Error(d.detail || `Validation failed (${vres.status})`);
      }

      const vdata = await vres.json();
      if (!vdata.valid) {
        throw new Error('IDまたはパスワードが正しくありません');
      }

      // 2) login to get HttpOnly cookie (server sets cookie). include credentials.
      await fetch(`${API_BASE}/api/v1/login/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      // 3) call delete endpoint with credentials included so server sees the cookie
      const res = await fetch(`${API_BASE}/api/v1/communities/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      });

      if (!res.ok) {
        const d = await res.json().catch(() => ({}));
        throw new Error(d.detail || `Delete failed (${res.status})`);
      }

      // success: clear client storage and navigate
      try {
        sessionStorage.removeItem('selectedCommunityId');
        sessionStorage.setItem('lastDestroyedCommunity', id);
      } catch (e) {}

      isComplete = true;
    } catch (e) {
      console.error(e);
      error = e instanceof Error ? e.message : '破棄に失敗しました';
    }
  }
  
  // キャンセル時の動作: 親コンポーネントに通知してアカウント画面に戻してもらう
  function handleBack() {
    dispatch('back');
  }

  // 完了後の動作: トップページへ戻る
  function toTop() {
    dispatch('complete');
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  {#if !isComplete}
    <section class="card" style="max-width:720px; width:100%">
      <h2>コミュニティを破棄しますか？</h2>
      <p>本当に破棄しますか？この操作は取り消せません。</p>

      <label>コミュニティパスワード
        <input type="password" bind:value={password} placeholder="パスワードを入力" />
      </label>

        {#if error}
          <div class="error">{error}</div>
        {/if}

        <div class="actions">
        <Button text="戻る" variant="secondary" on:click={handleBack} />
        {#if password}
          <Button text="破棄する" variant="primary" on:click={destroy} />
        {/if}
      </div>
    </section>

  {:else}
    <section class="card" style="max-width:720px; width:100%; text-align:center;">
      <h2>コミュニティを破棄しました</h2>
      <p>コミュニティ <strong>{id}</strong> を破棄しました。</p>
      <div class="actions" style="justify-content:center;">
        <Button text="トップへ戻る" variant="primary" on:click={toTop} />
      </div>
  </section>
  {/if}
</main>

<style>
  .card { background: var(--card); color: var(--text); padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px var(--shadow) }
  label { display:block; margin-bottom:0.75rem }
  input { width:100%; padding:0.5rem; border:1px solid var(--outline-sub); border-radius:4px; background: transparent; color: inherit }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid var(--outline); background: var(--card-high); color: var(--text); cursor:pointer }
  .btn.danger { background: var(--error); color: var(--on-error) }
  .error { color: var(--error); margin-top:0.5rem }
</style>
