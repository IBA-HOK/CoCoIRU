<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let communityId = '';
  let name = '';
  let count = 1;
  let password = '';

  onMount(() => {
    try {
      const pref = sessionStorage.getItem('selectedCommunityId');
      if (pref) communityId = pref;
      // まず communityEdits マップから現在の値を取得してプリセット
      try {
        const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
        const edits = JSON.parse(editsRaw || '{}');
        const e = edits[communityId] || null;
        if (e?.name) name = e.name;
        if (typeof e?.count === 'number') count = e.count;
      } catch (e) {}

      // 既に編集下書きがあればそれで上書き（直前の入力を復元）
      const saved = sessionStorage.getItem('editDraft');
      if (saved) {
        const d = JSON.parse(saved);
        if (d?.name) name = d.name;
        if (typeof d?.count === 'number') count = d.count;
        if (d?.password) password = d.password;
      }
    } catch (e) {}
  });

  function inc() { count = Math.min(9999, count + 1); }
  function dec() { count = Math.max(0, count - 1); }

  function toConfirm() {
    const draft = { communityId, name, count, password };
    try { sessionStorage.setItem('editDraft', JSON.stringify(draft)); } catch (e) {}
    goto('/community/edit/confirm');
  }
  function back() { goto('/community/account'); }
</script>

<main class="page">
  <div class="force-black-page">
  <section class="card">
    <h2>コミュニティ情報を編集</h2>
    <p>コミュニティID: <strong>{communityId}</strong></p>

    <label>コミュニティ名
      <input type="text" bind:value={name} placeholder="コミュニティ名を入力" />
    </label>

    <label>人数
      <div class="count-row">
        <button class="small" type="button" on:click={dec}>−</button>
        <input type="number" bind:value={count} min="0" />
        <button class="small" type="button" on:click={inc}>＋</button>
      </div>
    </label>

    <label>パスワード (更新用)
      <input type="password" bind:value={password} placeholder="コミュニティのパスワード" />
    </label>

    <div class="actions">
      <button class="btn" on:click={back}>戻る</button>
      <button class="btn primary" on:click={toConfirm} disabled={!name.trim()}>確認へ</button>
    </div>
  </section>
  </div>
</main>

<style>
  .page { padding: 1rem; display: flex; justify-content: center; }
  .card { width: 100%; max-width: 720px; background: #fff; border-radius: 8px; padding: 1.25rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  label { display:block; margin-bottom:0.75rem }
  input[type="text"], input[type="number"] { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color: #27b85a; color:white }
  .info-block { margin-top:1rem; border-top:1px solid #eee; padding-top:1rem }
  ul { margin:0; padding-left:1rem }
  .count-row { display:flex; gap:8px; align-items:center }
  .count-row input { width:80px; text-align:center }
  .small { padding:0.25rem 0.5rem }
  /* community ページと合わせて表示テキストを黒にする（編集画面も同じ見た目に） */
  .force-black-page, .force-black-page * { color: #000 !important; }
  /* ただし緑の主要ボタンの文字色は白に戻す */
  .force-black-page .btn.primary { color: #fff !important; }
</style>
