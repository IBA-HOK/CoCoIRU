<script lang="ts">
  import { Title, Surface, Button } from '$lib';
  import { getToken, communityId } from '$lib/stores/auth';
  import { get } from 'svelte/store';

  let itemName = '';
  let unit = '個';
  let reason = '';
  let message = '';

  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

async function submit() {
  message = '';

  if (!itemName.trim()) {
    message = '物品名を入力してください';
    return;
  }

  // ★ リクエスト直前に毎回トークンを読む
  // getToken が "Bearer xxx" を返す実装でも安全にする
  const raw = getToken() || '';
  const bearer = raw.replace(/^Bearer\s+/i, '').trim(); // Bearer二重対策

  // community_id は store から取る（取れなければ 1 にフォールバック）
  const cid = get(communityId) ?? 1;

  const payload = {
    community_id: cid,
    item_name: itemName,
    item_unit: unit,
    reason,
    timestamp: new Date().toISOString()
  };

  try {
    // ① まず cookie 認証で試す
    let res = await fetch(`${API_BASE}/api/v1/item_addition_requests/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    });

    // ② cookieでダメなら Bearer を付けて再挑戦
    if (!res.ok) {
      if (!bearer) {
        const txt = await res.text().catch(() => '');
        message =
          'ログインが必要です（トークンがありません）。communityログイン後に再度申請してください。' +
          (txt ? ` / ${txt}` : '');
        return;
      }

      // ★ 再挑戦の直前にも念のためもう一回読む（更新されるケース対策）
      const raw2 = getToken() || '';
      const bearer2 = raw2.replace(/^Bearer\s+/i, '').trim();

      res = await fetch(`${API_BASE}/api/v1/item_addition_requests/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${bearer2 || bearer}`
        },
        credentials: 'include',
        body: JSON.stringify(payload)
      });
    }

    if (!res.ok) {
      const txt = await res.text().catch(() => '');
      throw new Error(txt || `HTTP ${res.status}`);
    }

    message = '申請物品項目を送信しました（承認待ち）';

    itemName = '';
    unit = '個';
    reason = '';
  } catch (e: any) {
    message = `送信に失敗しました：${e?.message ?? e}`;
  }
}



</script>

<Title titleText="申請物品項目 追加申請" />

<div class="container">
<Surface>
  <div class="form">
    <label for="itemName">物品名（必須）</label>
    <input id="itemName" type="text" bind:value={itemName} placeholder="例：粉ミルク" />

    <label for="unit">単位（任意）</label>
    <input id="unit" type="text" bind:value={unit} placeholder="例：個、箱、本" />

    <label for="reason">申請理由（任意）</label>
    <textarea id="reason" rows="4" bind:value={reason} placeholder="必要な理由や用途など"></textarea>

    <div class="btn-area">
      <Button text="申請する" variant="accent" on:click={submit} />
    </div>

    {#if message}
      <p class="message">{message}</p>
    {/if}
  </div>
</Surface>
</div>

<style>
  .form {
    margin: 0 auto;
    max-width: 640px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  input, textarea {
    width: 100%;
    box-sizing: border-box;
    padding: 10px;
    font-size: 1rem;

    background-color: var(--bg);        /* ★ 完全に同じ白 */
    border: 1px solid var(--outline);       /* ★ 同じ枠色 */
    border-radius: 8px;             /* ★ RequestNoteInput と同じ角丸 */

    outline: none;
    box-shadow: none;
    font-family: inherit;
    color: var(--text);
  }  
  .btn-area {
    margin-top: 8px;
  }
  .message {
    margin-top: 12px;
    color: #2e7d32;
  }

  .container {
  max-width: 720px; /* ← 好きな幅 */
  margin: 0 auto;
  padding: 0 16px;
}

/* CoCoIRU フォーム統一ルール */
input:focus,
input:focus-visible,
textarea:focus,
textarea:focus-visible {
  border-width: 2px;              /* ★ 太くする */
  background-color: var(--bg);
  outline: none;
  box-shadow: none;
}



</style>
