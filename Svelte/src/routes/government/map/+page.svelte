<script lang="ts">
import { onMount } from 'svelte';
	import type { PageData } from './$types';
	
	// --- コンポーネントのインポート (dev4の構造を採用) ---
	import Title from '$lib/components/Title.svelte';
	import Surface from '$lib/components/Surface.svelte';
	import Modal from '$lib/MapInfoModal.svelte';
	import mapIcon from '$lib/assets/map.png';
	
	// マップ機能コンポーネント
	import ShelterMap from '$lib/features/government/components/ShelterMap.svelte';
	import ShelterMapSidebar from '$lib/features/government/components/ShelterMapSidebar.svelte';

	export let data: PageData;

	// --- 設定 ---
	// dev4の設定(/api/v1)を採用しつつ、あなたのロジックで使います
	const API_BASE_URL = '/api/v1';

	// --- 状態変数 (あなたのロジックを採用) ---
	let searchKeyword = '';
	let searchRadiusKm = 10.0;
	let isSelectionMode = false;
	// 初期値はサーバーデータまたはデフォルト座標
	let mapCenter: [number, number] = data.mapCenter || [136.884, 35.170];

	// Initialize communities from page load data (SSR pre-fetched)
	let communities: any[] = data.communities || [];
	let locationQuery = '';
	let isSearchingLocation = false;
	let showModal = false;
	let selectedCommunity: any = null;
	// ダミーデータ
	const dummyMarkers = [
		{ lat: 35.6895, lng: 139.6917, caption: '📍 新宿 (テストデータ)' },
		{ lat: 35.6585, lng: 139.7454, caption: '🗼 東京タワー (テストデータ)' },
		{ lat: 35.71, lng: 139.8107, caption: '🗼 スカイツリー (テストデータ)' },
		{ lat: 35.6277, lng: 139.7812, caption: '🚢 お台場 (テストデータ)' }
	];
	// マーカー生成
  $: mapMarkers = [
    ...dummyMarkers, // 先頭にダミーを追加
    ...communities // onMountでAPIから取得したデータ
    .filter(c => c.latitude != null && c.longitude != null) // 座標がないデータは除外
    .map(c => ({
      lat: c.latitude,
      lng: c.longitude,
      caption: c.name || '名前未設定',
      detail: c // 詳細モーダル用に生のデータを丸ごと渡す
    }))
    .filter(m => m.caption.includes(searchKeyword))
  ];

	// API通信処理など (変更なしのため省略)
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

<Title
	iconSrc={mapIcon}
	iconAlt="地図アイコン"
	titleText="避難所マップ"
	subtitleText="避難所の位置情報を地図上で確認・検索できます"
/>

<div class="dashboard-container">
	<div class="sidebar-content">
		<div class="surface-wrapper">
			<Surface>
				<ShelterMapSidebar
					bind:locationQuery
					bind:isSearchingLocation
					bind:searchRadiusKm
					bind:isSelectionMode
					bind:searchKeyword
					on:search={searchLocation}
				/>
			</Surface>
		</div>
	</div>
	<div class="main-content">
		<div class="surface-wrapper">
			<Surface>
				<ShelterMap
					markers={mapMarkers}
					{mapCenter}
					{searchRadiusKm}
					bind:isSelectionMode
					on:markerClick={handleMarkerClick}
					on:radiusChangePreview={handleRadiusPreview}
					on:radiusChange={handleRadiusChange}
					on:centerChange={handleCenterChange}
				/>
			</Surface>
		</div>
	</div>
</div>

{#if showModal}
	<Modal title={selectedCommunity.caption} on:close={() => (showModal = false)}>
		<div class="detail-content">
			<p><strong>緯度:</strong> {selectedCommunity.lat}</p>
			<p><strong>経度:</strong> {selectedCommunity.lng}</p>
			<hr />
			<h3>詳細情報</h3>
			<pre>{JSON.stringify(selectedCommunity.detail, null, 2)}</pre>
		</div>
	</Modal>
{/if}

<style>
	/* === コンテナレイアウト === */
	.dashboard-container {
		display: flex;
		box-sizing: border-box;
		background-color: var(--bg);
		color: var(--text);
		flex: 1;
	}

	.sidebar-content {
		width: 400px;
		flex-shrink: 0;
	}

	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-width: 0;
	}

	.surface-wrapper {
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	@media (max-width: 768px) {
		.dashboard-container {
			flex-direction: column;
			height: auto;
		}

		.sidebar-content {
			width: 100%;
			margin-bottom: 20px;
		}

		.main-content {
			height: 50vh;
			min-height: 400px;
		}
	}

	.detail-content {
		color: var(--text);
	}

	hr {
		border: none;
		border-top: 1px solid var(--outline-sub);
		margin: 16px 0;
	}

	pre {
		background: var(--card-low);
		padding: 10px;
		border-radius: 4px;
		overflow-x: auto;
	}
</style>
