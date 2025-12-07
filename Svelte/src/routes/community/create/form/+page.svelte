<script lang="ts">
  import { goto } from '$app/navigation';

  let name = '';
  let adults: number = 0;
  let children: number = 0;
  let password = '';

  function toConfirm() {
    const draft = { name, adults, children, password };
    try { sessionStorage.setItem('newCommunityDraft', JSON.stringify(draft)); } catch (e) {}
    goto('/community/create/confirm');
  }
  function back() { goto('/community/create'); }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
  <section class="card" style="max-width:720px; width:100%">
    <h2>コミュニティ作成フォーム</h2>

    <label>コミュニティ名
      <input type="text" bind:value={name} placeholder="コミュニティ名を入力" />
    </label>

    <label>大人の人数
      <input type="number" bind:value={adults} min="0" />
    </label>

    <label>子供の人数
      <input type="number" bind:value={children} min="0" />
    </label>

    <label>コミュニティパスワード
      <input type="password" bind:value={password} placeholder="任意のパスワード" />
    </label>

    <div class="actions">
      <button class="btn" on:click={back}>戻る</button>
      <button class="btn primary" on:click={toConfirm} disabled={!name.trim()}>確認へ</button>
    </div>
  </section>
</main>

<style>
  .card { background:#fff; padding:1.25rem; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.06) }
  label { display:block; margin-bottom:0.75rem }
  input { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color:#27b85a; color:#fff }
</style>
