<script lang="ts">
  	import MapComponent from '$lib/MapComponent.svelte';
  	import type { PageData } from './$types';

  	export let data: PageData;

	// APIで検索に使用した半径 (仮に10km）
	const searchRadiusKm = 10.0;

	// テスト用のダミーデータ ---
  const dummyMarkers = [
    { lat: 35.6895, lng: 139.6917, caption: '📍 新宿 (テストデータ)' },
    { lat: 35.6585, lng: 139.7454, caption: '🗼 東京タワー (テストデータ)' },
    { lat: 35.7100, lng: 139.8107, caption: '🗼 スカイツリー (テストデータ)' },
    { lat: 35.6277, lng: 139.7812, caption: '🚢 お台場 (テストデータ)' }
  ];

	$: mapMarkers = [
    ...dummyMarkers, // 先頭にダミーを追加
    ...data.communities
      .filter(c => c.latitude != null && c.longitude != null)
      .map(c => ({
        lat: c.latitude!,
        lng: c.longitude!,
        caption: c.name || '名前未設定'
      }))
  ];
</script>

<div class="map-page-container">
	<h1>📍 避難所コミュニティ位置情報</h1>
	<p class="subtitle">すべての避難所コミュニティの位置、人数、特記事項などを地図で確認します。</p>
	
	<div class="map-container-wrapper">
    <MapComponent 
        markers={mapMarkers}
        initialCenter={data.mapCenter}
        initialZoom={12}
		radiuskm={searchRadiusKm}
    />
	</div>
</div>

<style>
	h1 {
		color: #00796b;
		border-bottom: 2px solid #00796b;
		padding-bottom: 10px;
		margin-bottom: 10px;
	}
	.subtitle {
    	font-size: 1.1em;
		color: #555;
    	margin-bottom: 20px;
	}
	.map-container-wrapper {
    	width: 100%;
		height: 600px;
		border: 1px solid #ccc;
		border-radius: 8px;
		overflow: hidden; 
	}
</style>