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

<style>
  .form {
    max-width: 640px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  input, textarea {
    padding: 8px;
    font-size: 1rem;
  }
  .btn-area {
    margin-top: 8px;
  }
  .message {
    margin-top: 12px;
    color: #2e7d32;
  }
</style>
