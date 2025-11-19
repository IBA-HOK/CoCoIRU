<script lang="ts">
  import { goto } from '$app/navigation';
  import { requestItems } from '$lib/features/request/requestItems';
	import { Button } from '$lib';
  import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
  import AddRequestItemModal from '$lib/features/request/components/AddRequestItemModal.svelte';

  // モーダルの表示状態を管理する変数
  let showModal = false;

  function backButtonClick() {
    goto('/community/request');
  }
  
  $: selectedItems = $requestItems.filter(requestItems => requestItems.value > 0);
</script>

<AddRequestItemModal bind:show={showModal} />
<RequestItemList items={selectedItems} />

<div style="text-align: center; display: flex; flex-direction: column; gap: 1rem; align-items: center; margin-top: 2rem;">
  <!-- 
    モーダルを開くためのボタンを追加しました。
    クリックすると showModal が true になり、モーダルが表示されます。
  -->
  <Button text="申請項目を増やす" on:click={() => (showModal = true)} />

  <!-- 完了ボタン -->
  <Button text="完了" on:click={backButtonClick} />
</div>