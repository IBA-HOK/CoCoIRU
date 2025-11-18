<script lang="ts">
  // APIデータなしでUIの枠組みのみを作成
  const mapCenterText = "API接続が完了すると、地図の中心座標 (緯度, 経度) が表示されます。";
</script>

<div class="map-page-container">
	<h1>📍 避難所コミュニティ位置情報</h1>
	<p class="subtitle">すべての避難所コミュニティの位置、人数、特記事項などを地図で確認します。</p>
	
	<div class="map-placeholder">
		<div class="map-content">
			<p class="map-label">【地図表示エリア】</p>
			<p class="map-note">ここに Leaflet や Google Maps などの地図が統合されます。</p>
			<p class="map-note center-text">{mapCenterText}</p>
		</div>
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
        margin-bottom: 40px;
    }
	.map-placeholder {
    width: 100%;
    height: 600px; /* マップを想定した固定の高さ */
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    border-radius: 8px;
    }
	.map-content {
		text-align: center;
		color: #888;
	}
	.map-label {
		font-size: 1.5em;
		font-weight: bold;
		color: #666;
	}
	.center-text {
		margin-top: 15px;
		font-style: italic;
		max-width: 400px;
	}
</style>