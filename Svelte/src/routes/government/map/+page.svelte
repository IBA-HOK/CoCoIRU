<script lang="ts">
    import MapComponent from '$lib/MapComponent.svelte';
    import type { PageData } from './$types';

    export let data: PageData;

    $: mapMarkers = data.communities
     	.filter(c => c.latitude != null && c.longitude != null)
   		 .map(c => ({
			lat: c.latitude!,     // ! (Non-null assertion) を使い、null でないことをTSに伝える
			lng: c.longitude!,    // 同上
			caption: c.name || '名前未設定' // name が null の場合のフォールバック
    }));

</script>

<div class="map-page-container">
	<h1>📍 避難所コミュニティ位置情報</h1>
	<p class="subtitle">すべての避難所コミュニティの位置、人数、特記事項などを地図で確認します。</p>
	
	<div class="map-container-wrapper">
    <MapComponent 
        markers={mapMarkers}
        initialCenter={data.mapCenter}
        initialZoom={12}
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