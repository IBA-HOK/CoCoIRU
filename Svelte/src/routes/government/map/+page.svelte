<script lang="ts">
	import { onMount } from 'svelte';
	import MapComponent from '$lib/MapComponent.svelte';
	import Modal from '$lib/MapInfoModal.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	// --- 設定 ---
  const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

	// --- 状態 ---
  let searchKeyword = "";
  let searchRadiusKm = 10.0;
  let isSelectionMode = false;
	let mapCenter: [number, number] = data.mapCenter;

	// APIから取得した「生」のコミュニティデータ
  let communities: any[] = [];

	// 地名検索用の変数
  let locationQuery = "";
  let isSearchingLocation = false;

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
  $: mapMarkers = communities
    .filter(c => c.latitude != null && c.longitude != null) // 座標がないデータは除外
    .map(c => ({
      lat: c.latitude,
      lng: c.longitude,
      caption: c.name || '名前未設定',
      detail: c // 詳細モーダル用に生のデータを丸ごと渡す
    }))
    .filter(m => m.caption.includes(searchKeyword));
	
	// --- 関数: 避難所データをAPIから取得 ---
  async function fetchShelters(lat: number, lng: number, rangeKm: number) {
    try {
      // API Usage ドキュメントに基づくエンドポイント: /gnss/nearby
      const url = `${API_BASE_URL}/gnss/nearby?latitude=${lat}&longitude=${lng}&range=${rangeKm}`;
      console.log(`Fetching: ${url}`); // デバッグ用

      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`API Error: ${res.status}`);
      }
      
      const json = await res.json();
      communities = json; // データを更新 (画面に反映される)
      console.log("取得データ:", communities);

    } catch (e) {
      console.error("避難所データの取得に失敗しました:", e);
      // エラー時はリストを空にするか、以前のままにするか。今回はアラートを出す
      // alert("データの取得に失敗しました。バックエンドが起動しているか確認してください。");
    }
  }

	// --- 関数: 住所・地名検索 (Nominatim API) ---
  async function searchLocation() {
    if (!locationQuery) return;
    isSearchingLocation = true;

    try {
      // OpenStreetMapの検索APIを叩く
      const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationQuery)}&limit=1`;
      const res = await fetch(url);
      const json = await res.json();

      if (json && json.length > 0) {
        const result = json[0];
        const lat = parseFloat(result.lat);
        const lon = parseFloat(result.lon);
        mapCenter = [lon, lat];
				fetchShelters(lat, lon, searchRadiusKm);
      } else {
        alert("場所が見つかりませんでした");
      }
    } catch (e) {
      console.error(e);
      alert("検索エラーが発生しました");
    } finally {
      isSearchingLocation = false;
    }
  }

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
  }

  // 地図で半径変更確定
  function handleRadiusChange(event: CustomEvent) {
    searchRadiusKm = parseFloat(event.detail.toFixed(2));
    isSelectionMode = false; // モード終了
    // APIを再検索
		fetchShelters(mapCenter[1], mapCenter[0], searchRadiusKm);
  }

  // 地図の中心変更
  function handleCenterChange(event: CustomEvent) {
    mapCenter = event.detail;
  }
</script>

<div class="dashboard-container">
  <div class="sidebar">
    <h2>🗺️ マップ設定</h2>
    
    <div class="section-box">
      <h3>📍 場所を移動</h3>
      <div class="search-row">
        <input 
          type="text" 
          bind:value={locationQuery} 
          placeholder="例: 名古屋駅, 豊田市役所" 
          on:keydown={(e) => e.key === 'Enter' && searchLocation()}
        />
        <button on:click={searchLocation} disabled={isSearchingLocation}>
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
          on:click={() => isSelectionMode = !isSelectionMode}
        >
          {isSelectionMode ? 'キャンセル' : '👆 地図をドラッグして指定'}
        </button>
      </div>
    </div>

    <div class="section-box">
      <h3>🔍 避難所を絞り込み</h3>
      <input type="text" bind:value={searchKeyword} placeholder="避難所名を入力..." />
    </div>

  </div>

  <div class="main-content">
    <h1>避難所マップ</h1>
    <div class="map-wrapper">
      <MapComponent 
        markers={mapMarkers}
        center={mapCenter}
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