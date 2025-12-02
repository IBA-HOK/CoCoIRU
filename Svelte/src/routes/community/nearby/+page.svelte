<script lang="ts">
</script>

<div class="dashboard-container">
    <div class="sidebar">
        <h2>コミュニティ一覧</h2>
        
        <div class="mode-toggle">
            <p class="help-text">
                ボタンを押すと、地図上でドラッグして範囲を指定できます。
            </p>
        </div>
    
        <button class="search-btn">この条件で検索</button>

    </div>

    <div class="main-content">
        <h1>📍 コミュニティマップ</h1>
        
        <div class="map-wrapper">
            <div class="map-placeholder">
                地図表示エリア（現在は枠のみ）
            </div>
        </div>
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

    
    /* 地図枠セクション */
    .map-placeholder {
        width: 100%;
        height: 50vh; /* 画面の高さの半分 */
        background-color: #e0e0e0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.2em;
        color: #555;
        border-radius: 4px;
        margin-top: 15px;
        box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1);
    }
</style>