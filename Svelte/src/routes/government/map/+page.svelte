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

	// API通信処理など (変更なしのため省略)
	async function fetchShelters(lat: number, lng: number, rangeKm: number) {
		try {
			const url = `${API_BASE_URL}/gnss/nearby?latitude=${lat}&longitude=${lng}&range=${rangeKm}`;
			const res = await fetch(url, {
				credentials: 'include'
			});
			if (!res.ok) throw new Error(`API Error: ${res.status}`);
			communities = await res.json();
		} catch (e) {
			console.error('データ取得失敗:', e);
		}
	}

	// 検索処理
	async function searchLocation() {
		if (!locationQuery) return;
		isSearchingLocation = true;
		try {
			const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationQuery)}&limit=1`;
			const res = await fetch(url, {
				credentials: 'include'
			});
			const json = await res.json();
			if (json && json.length > 0) {
				const result = json[0];
				const lat = parseFloat(result.lat);
				const lon = parseFloat(result.lon);
				mapCenter = [lon, lat];
				fetchShelters(lat, lon, searchRadiusKm);
			} else {
				alert('場所が見つかりませんでした');
			}
		} catch (e) {
			console.error(e);
			alert('検索エラー');
		} finally {
			isSearchingLocation = false;
		}
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