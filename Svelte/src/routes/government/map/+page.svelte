<script lang="ts">
  	import MapComponent from '$lib/MapComponent.svelte';
		import Modal from '$lib/MapInfoModal.svelte';
  	import type { PageData } from './$types';

  	export let data: PageData;

	// --- 状態 ---
  let searchKeyword = "";
  let searchRadiusKm = 10.0;
  let isSelectionMode = false;
  let mapCenter = data.mapCenter;

	// モーダル用
  let showModal = false;
  let selectedCommunity: any = null;

	// テスト用のダミーデータ ---
  const dummyMarkers = [
    { lat: 35.6895, lng: 139.6917, caption: '📍 新宿 (テストデータ)' },
    { lat: 35.6585, lng: 139.7454, caption: '🗼 東京タワー (テストデータ)' },
    { lat: 35.7100, lng: 139.8107, caption: '🗼 スカイツリー (テストデータ)' },
    { lat: 35.6277, lng: 139.7812, caption: '🚢 お台場 (テストデータ)' }
  ];

	// APIデータ (communities) を MapComponent 用の markers 形式に変換
  $: mapMarkers = [
    ...dummyMarkers, // 先頭にダミーを追加
    ...data.communities // onMountでAPIから取得したデータ
    .filter(c => c.latitude != null && c.longitude != null) // 座標がないデータは除外
    .map(c => ({
      lat: c.latitude!,
      lng: c.longitude!,
      caption: c.name || '名前未設定',
      detail: c // 詳細モーダル用に生のデータを丸ごと渡す
    }))
    .filter(m => m.caption.includes(searchKeyword))
  ];
	
	// --- イベントハンドラ ---
  // マーカークリック時
  function handleMarkerClick(event: CustomEvent) {
    selectedCommunity = event.detail;
    showModal = true;
  }

  // 地図で半径変更中（プレビュー）
  function handleRadiusPreview(event: CustomEvent) {
    // 入力欄の数字だけ更新（APIはまだ叩かない）
    searchRadiusKm = parseFloat(event.detail.toFixed(2));
    isSelectionMode = false;
  }

  // 地図で半径変更確定
  function handleRadiusChange(event: CustomEvent) {
    searchRadiusKm = parseFloat(event.detail.toFixed(2));
    isSelectionMode = false; // モード終了
    // ★ここでAPIを再取得する処理を入れる (invalidateAllなど)
    // goto(`?lat=${mapCenter[1]}&lng=${mapCenter[0]}&range=${searchRadiusKm}`) など
  }

  // 地図の中心変更
  function handleCenterChange(event: CustomEvent) {
    const [lng, lat] = event.detail;
    mapCenter = [lng, lat];
  }

</script>

<div class="dashboard-container">
  <div class="sidebar">
    <h2>検索設定</h2>
    
    <div class="input-group">
      <label>キーワード</label>
      <input type="text" bind:value={searchKeyword} placeholder="避難所名など" />
    </div>

    <div class="input-group">
      <label>検索半径 (km)</label>
      <input type="number" bind:value={searchRadiusKm} step="0.1" />
    </div>

    <div class="mode-toggle">
      <button 
        class:active={isSelectionMode} 
        on:click={() => isSelectionMode = !isSelectionMode}
      >
        {isSelectionMode ? 'キャンセル' : '🗺️ 地図で範囲を指定する'}
      </button>
      <p class="help-text">
        ボタンを押すと、地図上でドラッグして範囲を指定できます。
      </p>
    </div>
    
    <button class="search-btn">この条件で検索</button>
  </div>

  <div class="main-content">
    <h1>📍 避難所マップ</h1>
    <div class="map-wrapper">
      <MapComponent 
        markers={mapMarkers}
        center={data.mapCenter}
        initialZoom={11}
        radiusKm={searchRadiusKm}
        bind:isSelectionMode={isSelectionMode}
        on:markerClick={handleMarkerClick}
        on:radiusChangePreview={handleRadiusPreview}
        on:radiusChange={handleRadiusChange}
        on:centerChange={handleCenterChange}
      />
    </div>
  </div>
</div>

{#if showModal}
  <Modal title={selectedCommunity.caption} on:close={() => showModal = false}>
    <div class="detail-content">
      <p><strong>緯度:</strong> {selectedCommunity.lat}</p>
      <p><strong>経度:</strong> {selectedCommunity.lng}</p>
      <hr>
      <h3>詳細情報</h3>
      <pre>{JSON.stringify(selectedCommunity.detail, null, 2)}</pre>
    </div>
  </Modal>
{/if}

<style>
  .dashboard-container {
    display: flex;
    gap: 20px;
    padding: 20px;
    height: 80vh;
    box-sizing: border-box;
  }
  
  .sidebar {
    width: 300px;
    background: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 15px;
  }

  .main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .map-wrapper {
    flex: 1;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  
  input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .mode-toggle button {
    width: 100%;
    padding: 10px;
    background: #fff;
    border: 2px solid #00796b;
    color: #00796b;
    font-weight: bold;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .mode-toggle button.active {
    background: #00796b;
    color: white;
  }

  .search-btn {
    background: #333;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: auto;
  }

  .help-text {
    font-size: 0.8rem;
    color: #666;
    margin-top: 5px;
  }
  
  h1, h2 { margin: 0 0 10px 0; color: #333; }
</style>