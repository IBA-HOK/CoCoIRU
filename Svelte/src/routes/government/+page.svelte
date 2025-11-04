<script lang="ts">
    const sectionName = "行政";
</script>

<div class="government-page">
    <header class="dashboard-header">
        <h1>{sectionName}トップページ</h1>
    </header>

    <section class="action-buttons-section">
        <a href="/government/communitielist" class="action-button left">
            <h2>コミュニティ一覧</h2>
        </a>

        <a href="/government/requestiist" class="action-button right">
            <h2>支援要請一覧</h2>
        </a>
    </section>

    <secton>
        <h2>避難所・要請地点 マップ</h2>
        <div class="map-placeholder">
            地図表示エリア（現在は枠のみ）
        </div>
    </secton>
</div>

<style>
    .government-page {
        margin-bottom: 30px;
        padding: 20px;
        border-bottom: 2px solid #004d40;
        text-align: center;
    }
    h1 {
        color: #004d40;
    }

    /* 上段 */
    .dashboard-header {
        padding-bottom: 20px;
    }

    /* 中段：ボタンセクション */
    .action-buttons-section {
        display: flex;
        gap: 20px;
        margin-bottom: 40px;
    }

    .action-button {
        flex: 1;
        padding: 20px;
        text-decoration: none; /* リンクの下線を消す */
        color: inherit; /* 文字の色を親要素から継承する */
        border: 1px solid #ddd;
        border-radius: 8px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 要素の下に影を付ける */
        text-align: center;
    }

    .action-button:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        background-color: #e8f5e9;
    }

    .action-button h2 {
        margin-top: 0;
        color: #00796b;
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