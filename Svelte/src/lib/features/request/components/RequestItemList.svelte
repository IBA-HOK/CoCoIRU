<script lang="ts">
/**
  * @component RequestItemsList
  * @description
  * 申請されたアイテム（数量が0より大きいもの）を受け取り、
  * 読み取り専用のリストとして表示するコンポーネントです。
  *
  * @see /routes/community/request/+page.svelte
  * @see /routes/community/request/confirm/+page.svelte - 主な呼び出し元の確認ページ
  */

  type Item = {
    text: string;
    value: number;
  };

  export let items: Item[] = [];
</script>

<div class="items-list">
  {#each items as item}
    <div class="item">
      <span class="item-text">{item.text}</span>
      <div class="item-quantity">
        <span>{item.value}</span>
        <span class="unit">個</span>
      </div>
    </div>
  {/each}
</div>

<style>
  .items-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
  }

  .item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: var(--primary-container);
    border: 1px solid color-mix(in srgb, var(--primary), transparent 70%);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 1.1rem;
    color: var(--on-primary-container);
  }

  .item-text {
    font-weight: bold;
    word-break: break-word;
    margin-right: 8px;
  }

  .item-quantity {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background-color: var(--primary);
    color: var(--on-primary);
    padding: 0.25rem 0.75rem;
    border-radius: 4px;
  }

  .unit {
    font-size: 0.8rem;
    opacity: 0.9;
  }
</style>