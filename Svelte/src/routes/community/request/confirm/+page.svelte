<script lang="ts">
  import { goto } from '$app/navigation';
  import { requestItems } from '$lib/features/request/requestItems';
  import { Button } from '$lib';
  import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
  import RequestNoteInput from '$lib/features/request/components/RequestNoteInput.svelte';

  // 特記事項
  let notes = '';

  $: selectedItems = $requestItems.filter(requestItems => requestItems.value > 0);

  // ボタン
  function backButtonClick() {
    goto('/community/request');
  }
  function orderButtonClick() {
    // 仮の処理
    console.log('注文内容:', selectedItems);
    console.log('特記事項:', notes);
    goto('/community/request/complete'); 
  }
</script>

<div class="page-wrapper">
  <div class="container">
    
    <h1 class="page-title">申請内容の確認</h1>
    <p class="page-subtitle">以下の内容で申請します。漏れがないかご確認ください。</p>

    <section class="section-card surface">
      <h2 class="section-title">選択したアイテム</h2>
      <div class="list-wrapper">
        <RequestItemList items={selectedItems} />
      </div>
    </section>

    <section class="section-card">
      <RequestNoteInput bind:value={notes} />
    </section>

    <div class="request_footer">
      <Button text="戻る" on:click={backButtonClick} />
      <Button text="注文する" on:click={orderButtonClick} />
    </div>

  </div>
</div>

<style>
  /* 全体の背景設定 */
  .page-wrapper {
    background-color: #f5f5f5; /* 背景色 */
    min-height: 100vh;
    padding: 2rem 1rem;
    box-sizing: border-box;
  }

  .container {
    max-width: 600px; /* 中央揃えで見やすい幅に制限 */
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px; /* 各セクションの間隔 */
  }

  .page-title {
    text-align: center;
    margin: 0;
    color: #333;
    font-size: 1.5rem;
  }

  .page-subtitle {
    text-align: center;
    color: #666;
    margin: 0 0 1rem 0;
    font-size: 0.9rem;
  }

  /* カード（Surface）スタイル */
  .surface {
    background-color: #fff;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05), 0 0 1px rgba(0,0,0,0.1);
    border: 1px solid rgba(0,0,0,0.03);
  }

  .section-title {
    margin: 0 0 16px 0;
    font-size: 1.1rem;
    color: #333;
    border-bottom: 1px solid #eee;
    padding-bottom: 8px;
  }

  .list-wrapper {
    max-height: 40vh; /* リストが長すぎる場合はスクロール */
    overflow-y: auto;
  }

  /* フッター */
  .request_footer {
    display: flex;
    justify-content: center; /* ボタンを中央寄せ */
    gap: 24px;
    margin-top: 1rem;
    padding-bottom: 3rem;
  }
</style>