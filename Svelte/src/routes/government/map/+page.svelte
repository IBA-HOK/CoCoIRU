<script lang="ts">
	import Modal from '$lib/MapInfoModal.svelte';
	import type { PageData } from './$types';
	import Title from '$lib/components/Title.svelte';

	// マップコンポーネント
	import ShelterMap from '$lib/features/government/components/ShelterMap.svelte';
	// ★作成したサイドバーコンポーネント
	import ShelterMapSidebar from '$lib/features/government/components/ShelterMapSidebar.svelte';
	import Surface from '$lib/components/Surface.svelte';

	export let data: PageData;

	// --- 設定 ---
	// Use proxied relative path so Vite dev server forwards to backend (same-origin)
	const API_BASE_URL = '/api/v1';

	// --- 状態 ---
	let searchKeyword = '';
	let searchRadiusKm = 10.0;
	let isSelectionMode = false;
	let mapCenter: [number, number] = data.mapCenter;

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
	$: mapMarkers = (() => {
		const filtered = communities
			.filter((c) => c.latitude != null && c.longitude != null)
			.map((c) => ({
				lat: c.latitude,
				lng: c.longitude,
				caption: c.name || '名前未設定',
				detail: c
			}))
			.filter((m) => m.caption.includes(searchKeyword));
		console.log('[+page.svelte] mapMarkers updated:', filtered);
		return filtered;
	})();

	// API通信処理など (変更なしのため省略)
	async function fetchShelters(lat: number, lng: number, rangeKm: number) {
		try {
			const url = `${API_BASE_URL}/gnss/nearby?latitude=${lat}&longitude=${lng}&range=${rangeKm}`;
			// Cookie (access_token) を送るため credentials: 'include' を指定
			const res = await fetch(url, { credentials: 'include' });
			if (!res.ok) throw new Error(`API Error: ${res.status}`);
			const data = await res.json();
			console.log('[+page.svelte] API response data:', data);
			communities = data;
			console.log('[+page.svelte] communities state updated with', communities.length, 'items');
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
			const res = await fetch(url);
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

	// イベントハンドラ
	function handleMarkerClick(event: CustomEvent) {
		selectedCommunity = event.detail;
		showModal = true;
	}
	function handleRadiusPreview(event: CustomEvent) {
		searchRadiusKm = parseFloat(event.detail.toFixed(2));
	}
	function handleRadiusChange(event: CustomEvent) {
		searchRadiusKm = parseFloat(event.detail.toFixed(2));
		isSelectionMode = false;
		fetchShelters(mapCenter[1], mapCenter[0], searchRadiusKm);
	}
	function handleCenterChange(event: CustomEvent) {
		mapCenter = event.detail;
	}
</script>

<Title titleText="避難所マップ" />

<div class="dashboard-container">
	<div class="sidebar-content">
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
	<div class="main-content">
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
		gap: 20px;
		height: 80vh;
		box-sizing: border-box;
		background-color: var(--bg);
		color: var(--text);
	}

	.sidebar-content {
		width: 500px;
		flex-shrink: 0;
	}

	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-width: 0;
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
