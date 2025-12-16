<script lang="ts">
  import { Title, Surface, Button } from '$lib';

  let itemName = '';
  let unit = '個';
  let reason = '';
  let message = '';

  function submit() {
    if (!itemName.trim()) {
      message = '物品名を入力してください';
      return;
    }

    console.log({ itemName, unit, reason });

    message = '申請物品項目を送信しました（承認待ち）';

    itemName = '';
    unit = '個';
    reason = '';
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
