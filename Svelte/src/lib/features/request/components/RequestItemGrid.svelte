<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { requestItems } from '$lib/features/request/requestItems';
  import RequestItemCard from './RequestItemCard.svelte';

  // const dispatch = createEventDispatcher();

  // 追加ボタンが押されたことを親に通知する関数
  // function handleAddClick() {
  //   dispatch('addClick');
  // }
</script>

<div class="button-grid">
  {#each $requestItems as item}
    <RequestItemCard {item} />
  {/each}

  <!-- 項目追加ボタン -->
  <!-- <RequestItemCard 
    isAddButton={true} 
    on:click={handleAddClick} 
  /> -->
</div>

<style>
  .button-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    margin: 5%; 
    gap: 15px;
  }
</style>