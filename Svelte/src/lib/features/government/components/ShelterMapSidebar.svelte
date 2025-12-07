<script lang="ts">
  import Surface from '$lib/components/Surface.svelte';
  import { createEventDispatcher } from 'svelte';

  // 親と双方向バインディングする変数
  export let locationQuery: string = "";
  export let isSearchingLocation: boolean = false;
  export let searchRadiusKm: number = 10.0;
  export let isSelectionMode: boolean = false;
  export let searchKeyword: string = "";

  const dispatch = createEventDispatcher();

  // 検索ボタンが押されたことを親に伝える
  function handleSearch() {
    dispatch('search');
  }

  // トグル切り替え
  function toggleSelectionMode() {
    isSelectionMode = !isSelectionMode;
    // 必要であれば親に通知（bindしているので必須ではないが、明示的なイベントが必要な場合）
    // dispatch('toggleMode', isSelectionMode);
  }
</script>

<div class="sidebar-wrapper">
  <Surface>
    <h2>🗺️ マップ設定</h2>
    
    <div class="section-box">
      <h3>📍 場所を移動</h3>
      <div class="search-row">
        <input 
          type="text" 
          bind:value={locationQuery} 
          placeholder="例: 名古屋駅, 豊田市役所" 
          on:keydown={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button class="btn-primary" on:click={handleSearch} disabled={isSearchingLocation}>
          {isSearchingLocation ? '...' : '移動'}
        </button>
      </div>
    </div>

    <div class="section-box">
      <h3>⭕ 検索範囲</h3>
      <div class="input-group">
        <label>半径 (km)</label>
        <input type="number" bind:value={searchRadiusKm} step="0.1" />
      </div>

      <div class="mode-toggle">
        <button 
          class:active={isSelectionMode} 
          on:click={toggleSelectionMode}
        >
          {isSelectionMode ? 'キャンセル' : '👆 地図をドラッグして指定'}
        </button>
      </div>
    </div>

    <div class="section-box">
      <h3>🔍 避難所を絞り込み</h3>
      <input type="text" bind:value={searchKeyword} placeholder="避難所名を入力..." />
    </div>
  </Surface>
</div>

<style>
  /* === サイドバー固有のレイアウト === */
  .sidebar-wrapper {
    width: 300px; /* 固定幅あるいは親に任せるなら flex-basis 等 */
    flex-shrink: 0;
  }

  /* === 入力エリアのスタイル === */
  .section-box {
    margin-bottom: 24px;
  }

  h2 {
    margin: 0 0 16px 0;
    color: var(--primary);
    font-size: 1.25rem;
  }

  h3 {
    margin: 0 0 8px 0;
    font-size: 1rem;
    color: var(--text-sub);
  }

  /* === 入力フォーム === */
  input {
    padding: 10px;
    border: 1px solid var(--outline);
    border-radius: 4px;
    background-color: var(--bg);
    color: var(--text);
    width: 100%;
    box-sizing: border-box;
  }

  input:focus {
    outline: 2px solid var(--primary);
    border-color: transparent;
  }

  .search-row {
    display: flex;
    gap: 8px;
  }
  
  .input-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 10px;
  }

  label {
    font-size: 0.9rem;
    color: var(--text);
  }

  /* === ボタンデザイン === */
  .btn-primary {
    background-color: var(--primary);
    color: var(--on-primary);
    padding: 10px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    white-space: nowrap;
    transition: opacity 0.2s;
  }
  .btn-primary:hover {
    opacity: 0.9;
  }
  .btn-primary:disabled {
    background-color: var(--outline-sub);
    cursor: not-allowed;
  }

  /* トグルボタン */
  .mode-toggle button {
    width: 100%;
    padding: 10px;
    background: transparent;
    border: 1px solid var(--primary);
    color: var(--primary);
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .mode-toggle button:hover {
    background-color: var(--primary-container);
  }

  .mode-toggle button.active {
    background: var(--primary);
    color: var(--on-primary);
  }
</style>