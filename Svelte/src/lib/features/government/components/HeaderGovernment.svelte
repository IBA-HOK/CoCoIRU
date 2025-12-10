<script lang="ts">
  import { page } from '$app/stores';
  import { Hamburger } from '$lib';

  const navLinks = [
    { href: '/government/requestlist', label: '支援要請一覧' },
    { href: '/government/map', label: '避難所マップ' },
    { href: '/government/addItem', label: '支援品目追加' }
  ];
  
  $: isActive = (path: string) => $page.url.pathname.startsWith(path);
</script>

<header class="main-header">

  <!-- モバイル用ハンバーガーメニュー -->
  <div class="mobile-only">
    <Hamburger links={navLinks} />
  </div>

  <!-- タイトルロゴ -->
  <a href="/government" class="logo-link">
    <span class="logo-text">CoCoIRU アドミン</span>
  </a>

  <!-- デスクトップ用ナビゲーション -->
  <nav class="main-nav desktop-only">
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
    <a 
      href="/government/addItem" 
      class="nav-item" 
      class:active={isActive('/government/addItem')}
    >
      支援品目追加
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

  .mobile-only {
    display: none;
  }

  /* スマホサイズ(768px以下)のとき */
  @media (max-width: 768px) {
    .desktop-only {
      display: none;
    }
    
    .mobile-only {
      display: block;
    }
    
    .main-header {
      padding: 15px 20px;
      justify-content: space-between;
    }
  }
</style>