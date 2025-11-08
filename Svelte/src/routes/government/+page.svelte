<script lang="ts">
</script>

<div class="government-home-container">
    <h1>🚨 災害支援システム 行政ダッシュボード</h1>
    <p class="subtitle">避難所からの支援要請への迅速な対応を支援します。</p>

    <div class="card-grid">
        <a href="/government/requestlist" class="feature-card">
            <h2>📋 支援要請一覧</h2>
            <p>未対応の要請や対応状況を確認し、優先順位をつけて対応を開始します。</p>
            <div class="link-label">→ 詳細を見る</div>
        </a>
        
        <a href="/government/map" class="feature-card">
            <h2>📍 避難所マップ</h2>
            <p>すべてのコミュニティの現在位置（避難所）と周辺情報を地図上で確認します。</p>
            <div class="link-label">→ マップを見る</div>
        </a>
    </div>
</div>

<style>
    h1 {
        color: #00796b;
        border-bottom: 2px solid #00796b; /* solid：実線 */
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.1em;
        color: #555;
        margin-bottom: 40px;
    }
    .card-grid {
        display: grid;
        /* グリッドの列数や各グリッドのサイズ設定 */
        /* repeat(auto-fit, ...)で可能な限り自動生成 */
        /* 最小300px, 最大で残りスペースの1単位分 */
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 30px;
    }
    .feature-card {
        display: block;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 下方向に影、12px分ぼかし */
        text-decoration: none; /* 下線削除 */
        transition: transform 0.2s, box-shadow 0.2s; /* transform と box-shadow のプロパティが変化する際に、0.2秒かけて滑らかに変化 */
        background-color: #ffffff;
        border-top: 5px solid #00bcd4; /* Cyan Accent */
    }
    .feature-card:hover {
        transform: translateY(-5px); /* Y軸（垂直方向）に-5px（上方向）に移動 */
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.15);  /* 下方向に影、18px分ぼかし */
    }
    .feature-card h2 {
        color: #004d40;
        margin-top: 0;
        font-size: 1.5em;
    }
    .feature-card p {
        color: #666;
        line-height: 1.6; /* 行間を文字の大きさに対して1.6倍に調節 */
    }
    .link-label {
        margin-top: 15px;
        color: #00bcd4;
        font-weight: bold; /* 太字 */
    }
</style>