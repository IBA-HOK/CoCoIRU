<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  // MapComponentの場所に合わせてパスを確認してください
  // '$lib/components/MapComponent.svelte' の場合もあります
  import MapComponent from '$lib/MapComponent.svelte';

  // --- 設定値 ---
  const FIXED_RADIUS_KM = 2;       // 半径を5kmに固定
  const UPDATE_INTERVAL_MS = 5000; // 5秒ごとに更新

  // --- 状態変数 ---
  let center: [number, number] = [136.884, 35.170]; // デフォルト: 名古屋
  let isLocationLoaded = true;
  let errorMsg = '';
  let intervalId: any; // タイマーID

  // --- 型定義 ---
  interface Community {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    address?: string;
  }

  let communities: Community[] = []; // リスト表示用
  let markers: any[] = [];           // マップ表示用

  // --- APIからデータを取得する関数 ---
  async function fetchNearbyCommunities(lat: number, lng: number) {
    try {
      // APIエンドポイント (http://127.0.0.1:8000...)
      const url = `http://127.0.0.1:8000/api/v1/gnss/nearby?latitude=${lat}&longitude=${lng}&range=${FIXED_RADIUS_KM}`;
      
      // 認証が必要な場合は { credentials: 'include' } を追加
      const res = await fetch(url);
      
      if (!res.ok) throw new Error('データ取得失敗');

      const data: Community[] = await res.json();
      communities = data; 

      // MapComponent用にデータを変換
      markers = data.map(c => ({
        lat: c.latitude,
        lng: c.longitude,
        caption: c.name,
        detail: c 
      }));

    } catch (e) {
      console.error(e);
      // 自動更新を止めないためエラー表示は控えめに
      // errorMsg = 'データの更新に失敗しました'; 
    }
  }

  // --- 現在位置を取得して更新する関数 ---
  function updateLocationAndFetch() {
    if (!navigator.geolocation) {
      errorMsg = 'このブラウザは位置情報に対応していません';
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        // 中心点を更新
        center = [lng, lat];
        isLocationLoaded = true;
        errorMsg = ''; 

        // APIデータ更新
        fetchNearbyCommunities(lat, lng);
      },
      (error) => {
        console.warn('位置情報エラー:', error);
        // 失敗時は前回の位置(またはデフォルト)で再検索
        fetchNearbyCommunities(center[1], center[0]);
      },
      {
        enableHighAccuracy: true,
        timeout: 4000,
        maximumAge: 0
      }
    );
  }

  // --- ライフサイクル ---
  onMount(() => {
    // 初回実行
    updateLocationAndFetch();

    // 定期実行開始
    intervalId = setInterval(updateLocationAndFetch, UPDATE_INTERVAL_MS);
  });

  onDestroy(() => {
    // 画面を離れるときにタイマーを解除
    if (intervalId) clearInterval(intervalId);
  });

  // --- イベントハンドラ ---
  function handleMarkerClick(e: CustomEvent) {
    const markerInfo = e.detail;
    alert(`選択された避難所: ${markerInfo.caption}`);
    // ここにモーダル表示処理を追加できます
  }
</script>

<div class="dashboard-container">
  <div class="sidebar">
    <h2>コミュニティ一覧</h2>
    
    <div class="info-area">
      <p class="radius-info">
        周辺 <strong>{FIXED_RADIUS_KM}km</strong> の避難所を表示中
      </p>
      
      <div class="status-indicator">
        <span class="pulse-dot"></span>
        <span class="status-text">位置情報を自動更新中</span>
      </div>
    </div>

    <div class="community-list">
      {#if communities.length === 0}
        <div class="no-data-msg">
            <p>近くに避難所が見つかりません</p>
        </div>
      {:else}
        <ul>
          {#each communities as comm}
            <li class="community-item">
              <strong>{comm.name}</strong>
              {#if comm.address}<p class="address">{comm.address}</p>{/if}
            </li>
          {/each}
        </ul>
      {/if}
    </div>
  </div>

  <div class="main-content">
    <h1>📍 コミュニティマップ</h1>
    
    <div class="map-wrapper">
      {#if !isLocationLoaded}
        <div class="loading-state">
           <p>現在位置を取得中...</p>
        </div>
      {:else}
        <MapComponent 
          center={center}
          radiusKm={FIXED_RADIUS_KM}
          markers={markers}
          isSelectionMode={false}
          on:markerClick={handleMarkerClick}
        />
      {/if}
    </div>
    
    {#if errorMsg}
      <p class="error-msg">{errorMsg}</p>
    {/if}
  </div>
</div>

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
    overflow: hidden;
  }

  .info-area {
    padding-bottom: 15px;
    border-bottom: 1px solid #ddd;
    text-align: center;
  }
  
  .radius-info {
    margin: 0 0 10px 0;
    color: #555;
  }

  /* ステータスインジケーター */
  .status-indicator {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: #007cbf;
    font-size: 0.85rem;
    background: #e3f2fd;
    padding: 6px;
    border-radius: 20px;
    margin-top: 5px;
  }
  
  .status-text {
    font-weight: bold;
  }

  .pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #007cbf;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(0.8); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.6; }
    100% { transform: scale(0.8); opacity: 1; }
  }

  /* リスト */
  .community-list {
    flex: 1;
    overflow-y: auto;
  }
  .community-list ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .community-item {
    background: white;
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 4px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  }
  .community-item:hover {
    background-color: #f0f8ff;
  }
  .address {
    font-size: 0.8rem;
    color: #666;
    margin: 4px 0 0 0;
  }
  .no-data-msg {
    color: #888;
    text-align: center;
    margin-top: 20px;
    font-size: 0.9rem;
  }

  /* メインコンテンツ */
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
    position: relative;
    min-height: 400px;
  }

  .loading-state {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f0f0f0;
    color: #666;
    font-weight: bold;
  }

  h1, h2 { 
    margin: 0 0 10px 0; 
    color: #333;
  }

  .error-msg {
    color: #d32f2f;
    font-size: 0.9rem;
    margin-top: 5px;
  }
</style>