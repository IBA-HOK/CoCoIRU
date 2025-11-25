<script lang="ts">
  /**
   * @component RequestItemCard
   * @description 申請アイテムを表示するカードコンポーネント
   */
  export let item: { text: string; value: number };

  const maxQuantity = 100;
</script>

<div class="card" class:selected={item.value > 0}>
  <div class="card-content">
    <div class="item-name">
      {item.text}
    </div>

    <div class="control-area">
      <select bind:value={item.value}>
        {#each Array(maxQuantity) as _, i}
          <option value={i}>
            {i}
          </option>
        {/each}
      </select>
      <span class="unit">個</span>
    </div>
  </div>
</div>

<style>
  .card {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    height: 100%;
    box-sizing: border-box;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .card.selected {
    border-color: #4CAF50;
    background-color: #e0ffe0;
    box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
  }

  .card-content {
    display: flex;
    flex-direction: column;
    gap: 12px;
    align-items: center;
    width: 100%;
  }

  .item-name {
    font-weight: bold;
    font-size: 1rem;
    text-align: center;
    line-height: 1.4;
    word-break: break-word;
  }

  .control-area {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
    justify-content: center;
  }

  select {
    font-size: 1rem;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    background-color: white;
    width: 100%;
    max-width: 100px;
    cursor: pointer;
  }
  
  .unit {
    font-size: 0.9rem;
    color: #666;
    white-space: nowrap;
  }

  .selected select {
    border-color: #4CAF50;
    color: #000;
  }
</style>