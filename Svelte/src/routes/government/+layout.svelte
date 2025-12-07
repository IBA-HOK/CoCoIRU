<script>
    import { page } from '$app/stores';

    // 現在のパスに基づいて、アクティブなナビゲーションリンクを判定する関数
    function isActive(path) {
        return $page.url.pathname.startsWith(path);
    }
</script>

<div class="government-app">
    <header class="main-header">
        <a href="/government" class="logo-link">
            <span class="logo-text">行政ダッシュボード</span>
        </a>

        <nav class="main-nav">
            <a href="/government/requestlist" class="nav-item" class:active={isActive('/government/requestlist')}>
                支援要請一覧
            </a>
            <a href="/government/map" class="nav-item" class:active={isActive('/government/map')}>
                避難所マップ
            </a>
        </nav>
    </header>

    <slot />
</div>

<style>
    .government-app {
        min-height: 100vh; /* 画面いっぱいの高さ */
        font-size: 1.2em;
    }

    .main-header {
        background-color: #00796b;
        color: white;
        padding: 20px 50px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* ロゴのリンク */
    .logo-link {
        text-decoration: none;
        color: white;
        margin-right: 40px;
        font-size: 1.4em;
        font-weight: bold;
        transition: opacity 0.2s;
    }
    .logo-link:hover {
        opacity: 0.8;
    }

    /* ナビゲーションコンテナ */
    .main-nav {
        display: flex;
        gap: 25px;
        margin-left: auto;
    }

    /* ナビゲーションアイテム（リンク） */
    .nav-item {
        text-decoration: none;
        color: #ecf0f1; /* 明るいグレー */
        padding: 5px 0;
        position: relative;
        transition: color 0.2s;
    }
    .nav-item:hover {
        color: #3498db; /* ホバーで青色に */
    }

    /* アクティブなページの下線表示 */
    .nav-item.active {
        color: #3498db; /* アクティブなページは青色に */
        font-weight: bold;
    }
    .nav-item.active::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: #3498db;
    }
</style>