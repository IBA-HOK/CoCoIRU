<script lang="ts">
  import { goto } from '$app/navigation';
  import Button from '$lib/Button.svelte';
  import { requestItems } from '$lib/requestItems';

  // 特記事項
  let notes = '';

  $: selectedItems = $requestItems.filter(requestItems => requestItems.value > 0);

  // ボタン
  function backButtonClick() {
    goto('/request');
  }
  function orderButtonClick() {
    // 仮の処理(todo: 実際のデータベース処理を実装)
    console.log('注文内容:', selectedItems);
    console.log('特記事項:', notes);
    goto('/request/complete'); 
  }
</script>

<h1 style="text-align: center;">申請漏れはございませんか？</h1>

<div class="content-container">
  <div class="selected-items-list">
    {#each selectedItems as item}
      <div class="selected-item">
        <span class="item-text">{item.text}</span>
        <div class="item-quantity">
          <span>{item.value}</span>
        </div>
      </div>
    {/each}
  </div>

  <textarea 
    bind:value={notes} 
    placeholder="特記事項があればお書きください。"
    rows={5}
  ></textarea>
</div>

<div class="request_footer">
  <Button text="戻る" on:click={backButtonClick} />
  <Button text="注文する" on:click={orderButtonClick} />
</div>

<style>
  .content-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 1rem;
    max-height: 60vh;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 1rem;
  }

  .selected-items-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .selected-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #e0ffe0;
    border: 1px solid #c0e0c0;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 1.1rem;
  }

  .item-text {
    font-weight: bold;
  }

  .item-quantity {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: #4CAF50;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
  }

  textarea {
    width: 100%;
    font-size: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    resize: vertical;
    box-sizing: border-box;
  }

  .request_footer {
    padding-top: 50px;
    display: flex;
    justify-content: space-evenly;
  }
</style>