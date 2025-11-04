<script lang="ts">
  import Button from '$lib/Button.svelte';

  // 申請物資のリスト
  let items = [
    { text: '食料', selectedValue: 0 },
    { text: '毛布', selectedValue: 0 },
    { text: '乳児用粉・液体ミルク', selectedValue: 0 },
    { text: '乳児・小児用おむつ', selectedValue: 0 },
    { text: '生理用品', selectedValue: 0 },
    { text: 'トイレットペーパー', selectedValue: 0 },
    { text: '簡易・携帯トイレ', selectedValue: 0 },
    { text: '大人用おむつ', selectedValue: 0 },
  ];
  
  // 最大値は99
  const maxQuantity = 100;

</script>

<div class="button-grid">
  {#each items as item}
    <div class="grid-item-container">
      
      <Button text={item.text} on:click={() => console.log(item.text)} />

      <select bind:value={item.selectedValue}>
        
        {#each Array(maxQuantity) as _, i}
          <option value={i}>
            {i}
          </option>
        {/each}
      </select>
    </div>
  {/each}
</div>

<details>
  <summary>現在の全データ（デバッグ用）</summary>
  <pre>{JSON.stringify(items, null, 2)}</pre>
</details>

<style>
  /* ... (style タグの中身は前回の回答から変更なし) ... */

  .button-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    margin: 5%;
    gap: 15px;
  }
  .grid-item-container {
    display: flex;
    gap: 8px;
    align-items: center;
  }
  .grid-item-container :global(button) {
    flex: 1; 
  }
  select {
    font-size: 1rem;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
    flex-basis: 80px; /* 数値だけなので幅を少し狭く調整 */
  }
  pre {
    background-color: #f4f4f4;
    padding: 10px;
    border-radius: 4px;
  }
</style>