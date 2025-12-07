<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import MapComponent from '$lib/MapComponent.svelte';

  // デフォルトの中心点（名古屋駅周辺など、取得失敗時のフォールバック用）
  let center: [number, number] = [136.884, 35.170];
  let isLocationLoaded = false; // 位置情報取得完了フラグ
  let errorMsg = '';

  // --- 型定義 ---
  interface Community {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    address?: string;
  }

  // 検索範囲（km）
  const FIXED_RADIUS_KM = 2;
  const UPDATE_INTERVAL_MS = 5000;

  let communities: Community[] = [];
  let markers: any[] = [];
  let intervalId: any;

  // --- APIからデータを取得する関数 ---
  async function fetchNearbyCommunities(lat: number, lng: number) {
    try {
      // Python側のAPIに合わせてURLを構築
      const url = `http://127.0.0.1:8000/api/v1/gnss/nearby?latitude=${lat}&longitude=${lng}&range=${FIXED_RADIUS_KM}`;
      
			const res = await fetch(url, {
				credentials: 'include'
			});
      if (!res.ok) throw new Error('データ取得失敗');

      const data: Community[] = await res.json();
      communities = data; // リスト表示用

      // MapComponent用にデータを変換
      markers = data.map(c => ({
        lat: c.latitude,
        lng: c.longitude,
        caption: c.name,
        detail: c // 詳細データを持たせておく
      }));

    } catch (e) {
      console.error(e);
      errorMsg = '避難所データの取得に失敗しました';
    }
  }

  // --- 現在位置を取得して更新する関数 ---
  function updateLocationAndFetch() {
    if (!navigator.geolocation) {
      errorMsg = '位置情報に対応していません';
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        center = [lng, lat];
        isLocationLoaded = true;
        errorMsg = ''; // 成功したらエラー消去

        // API更新
        fetchNearbyCommunities(lat, lng);
      },
      (error) => {
        console.warn('位置情報エラー:', error);
        // 位置が取れない場合は既存のcenter（またはデフォルト）で再検索を試みる
        fetchNearbyCommunities(center[1], center[0]);
      },
      {
        enableHighAccuracy: true, // 高精度モード
        timeout: 4000,            // タイムアウトはインターバルより短く
        maximumAge: 0             // 常に最新を取得
      }
    );
  }

  onMount(() => {
    // 1. 初回実行
    updateLocationAndFetch();

    // 2. 定期実行を開始 (5秒ごと)
    intervalId = setInterval(() => {
      updateLocationAndFetch();
    }, UPDATE_INTERVAL_MS);
  });

  // --- 画面破棄時の処理 ---
  onDestroy(() => {
    // 画面遷移した時に裏で動き続けないようタイマーを消す
    if (intervalId) clearInterval(intervalId);
  });

  // --- 再検索ボタンの処理 ---
  function handleSearch() {
    // 現在の中心点と半径で再検索
    fetchNearbyCommunities(center[1], center[0]);
  }

  function handleRefresh() {
    fetchNearbyCommunities(center[1], center[0]);
  }

  // --- マーカークリック時の処理（MapComponentから発火） ---
  function handleMarkerClick(e: CustomEvent) {
    const markerInfo = e.detail;
    alert(`選択された避難所: ${markerInfo.caption}`);
  }
</script>

<div class="dashboard-container">
  <div class="sidebar">
    <h2>コミュニティ一覧</h2>
    
    <div class="info-area">
      <p class="radius-info">
        周辺 <strong>{FIXED_RADIUS_KM}km</strong> の避難所を表示中
      </p>
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
