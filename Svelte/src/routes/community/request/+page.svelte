<script lang="ts">
  import { goto } from '$app/navigation';
  import { Button } from '$lib';
  import { requestItems } from '$lib/features/request/requestItems';
  import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
  import AddRequestItemModal from '$lib/features/request/components/AddRequestItemModal.svelte';
  import RequestItemGrid from '$lib/features/request/components/RequestItemGrid.svelte';
  import RequestNoteInput from '$lib/features/request/components/RequestNoteInput.svelte';

  // $: は、依存する変数(items)が変更されるたびに自動で再計算します
  $: selectedItems = $requestItems.filter(item => item.value > 0);
  $: totalSelected = $requestItems.reduce((sum, item) => sum + item.value, 0);
  let showModal = false;
  let notes = '';

  function confirmButtonClick() {
    goto('/community/request/confirm');
  }
</script>

<div class="page-wrapper">
  <div class="container">
    
    <main class="main-content surface">
      <h2 class="section-title">申請品目を選択</h2>
      <RequestItemGrid on:addClick={() => (showModal = true)} />
    </main>

    <aside class="sidebar surface sticky-sidebar">
      <div class="sidebar-header">
        <h2 class="section-title">選択済み</h2>
        {#if selectedItems.length > 0}
          <span class="badge">{selectedItems.length}件</span>
        {/if}
      </div>

      <div class="sidebar-body">
        {#if selectedItems.length === 0}
          <p class="empty-message">アイテムが選択されていません</p>
        {:else}
          <RequestItemList items={selectedItems} />
        {/if}
      </div>

      <div class="sidebar-footer">
        <div class="summary-line">
            <span>合計数量:</span>
            <strong>{totalSelected} 個</strong>
        </div>
      <RequestNoteInput bind:value={notes} />
        <div class="action-button">
          <Button text="注文確定" on:click={confirmButtonClick} />
        </div>
      </div>
    </aside>
  </div>
</div>

<AddRequestItemModal bind:show={showModal} />

<style>
  .page-wrapper {
    background-color: #f5f5f5;
    min-height: 100vh;
    padding: 2rem 1rem;
    box-sizing: border-box;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    flex-direction: row;
    gap: 24px;
    align-items: flex-start;
  }

  /* --- 共通のカード（Surface）スタイル --- */
  .surface {
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05), 0 0 1px rgba(0,0,0,0.1);
    padding: 24px;
    border: 1px solid rgba(0,0,0,0.03);
  }

  /* --- メインコンテンツ --- */
  .main-content {
    flex: 1;
    min-width: 0;
  }

  .section-title {
    margin: 0 0 1.5rem 0;
    font-size: 1.25rem;
    color: #333;
    font-weight: 500;
  }

  /* --- サイドバー --- */
  .sidebar {
    width: 320px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  /* スクロールしてもついてくる設定 */
  .sticky-sidebar {
    position: sticky;
    top: 24px;
    max-height: calc(100vh - 48px);
    overflow-y: auto;
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #eee;
    padding-bottom: 12px;
  }

  .sidebar-body {
    flex-grow: 1;
    overflow-y: auto;
  }

  .sidebar-footer {
    border-top: 1px solid #eee;
    padding-top: 16px;
    margin-top: auto;
		display: flex;
    flex-direction: column;
    gap: 16px; 
  }

  .summary-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0; 
    font-size: 1rem;
    align-items: center;
  }

  .summary-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
    font-size: 1rem;
  }

  .action-button {
    text-align: center;
  }

  .badge {
    background-color: #e0e0e0;
    color: #333;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: bold;
  }

  .empty-message {
    color: #999;
    text-align: center;
    padding: 20px 0;
    font-size: 0.9rem;
  }

  /* レスポンシブ対応: スマホでは縦並び */
  @media (max-width: 768px) {
    .container {
      flex-direction: column;
			text-align: center;
    }
    .sidebar {
      width: 100%;
      position: static;
    }
  }
</style>