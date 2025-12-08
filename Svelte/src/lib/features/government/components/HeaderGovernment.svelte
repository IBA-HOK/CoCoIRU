<script lang="ts">
  import { page } from '$app/stores';

  // 現在のパスに基づいて、アクティブなナビゲーションリンクを判定する関数
  // $: を使ってパス変更時にリアクティブに再計算させます
  $: isActive = (path: string) => $page.url.pathname.startsWith(path);
</script>

<header class="main-header">
  <a href="/government" class="logo-link">
    <span class="logo-text">行政ダッシュボード</span>
  </a>

  <nav class="main-nav">
    <a 
      href="/government/requestlist" 
      class="nav-item" 
      class:active={isActive('/government/requestlist')}
    >
      支援要請一覧
    </a>
    <a 
      href="/government/map" 
      class="nav-item" 
      class:active={isActive('/government/map')}
    >
      避難所マップ
    </a>
  </nav>
</header>

<style>
  .main-header {
    background: linear-gradient(to right, var(--primary), var(--accent));
    color: var(--on-primary);
    padding: 20px 50px;
    display: flex;
    align-items: center;
  }

  /* ロゴのリンク */
  .logo-img img {
    height: 40px;
    width: auto;
  }

  .logo-link {
    text-decoration: none;
    color: var(--on-primary);
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
    color: var(--on-primary);
    opacity: 0.7;
    
    padding: 5px 0;
    position: relative;
    transition: all 0.2s;
  }
  
  .nav-item:hover {
    opacity: 1;
  }

  /* アクティブなページ */
  .nav-item.active {
    opacity: 1;
    font-weight: bold;
  }
  
  /* アクティブ時の下線 */
  .nav-item.active::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--on-primary);
    border-radius: 2px;
  }
</style>