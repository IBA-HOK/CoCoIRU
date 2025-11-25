<script lang="ts">
  import { goto } from '$app/navigation';
  import { requestItems } from '$lib/features/request/requestItems';
	import { Button } from '$lib';
  import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';

  // 特記事項
  let notes = '';

  $: selectedItems = $requestItems.filter(requestItems => requestItems.value > 0);

  // ボタン
  function backButtonClick() {
    goto('/community/request');
  }
  function orderButtonClick() {
    // 仮の処理(todo: 実際のデータベース処理を実装)
    console.log('注文内容:', selectedItems);
    console.log('特記事項:', notes);
    goto('/community/request/complete'); 
  }
</script>

<h1 style="text-align: center;">申請漏れはございませんか？</h1>

<div class="content-container">
  <RequestItemList items={selectedItems} />
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