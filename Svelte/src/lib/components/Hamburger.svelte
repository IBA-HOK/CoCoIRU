<script lang="ts">
  import { fade } from 'svelte/transition';
  
  // 親から受け取るリンクのリスト
  export let links: App.NavLink[] = [];

  // メニューの開閉状態
  let isOpen = false;

  // メニューを切り替える関数
  function toggle() {
    isOpen = !isOpen;
  }

  // メニューを閉じる関数（リンククリック時など）
  function close() {
    isOpen = false;
  }
</script>

<div class="menu-wrapper">
  <button 
    class="menu-icon" 
    class:open={isOpen} 
    on:click={toggle}
    aria-label="メニューを開閉"
  >
    <span></span>
    <span></span>
    <span></span>
  </button>

  {#if isOpen}
    <div 
      class="overlay" 
      transition:fade={{ duration: 300 }}
      on:click={close}
    ></div>
  {/if}

  <nav class="menu" class:open={isOpen}>
    <ul>
      {#each links as link}
        <li>
          <a href={link.href} on:click={close}>
            {link.label}
          </a>
        </li>
      {/each}
    </ul>
    <div class="footer-container">
      <img src="/src/lib/assets/CoCoIRU_logo.png" alt="CoCoIRU"class="footer-logo"/>
    </div>
  </nav>
</div>

<style>
  .menu-wrapper {
    position: relative;
  }

  /* === アイコンボタン === */
  .menu-icon {
    width: 40px;
    height: 30px;
    position: relative;
    cursor: pointer;
    z-index: 1001; /* 最前面に */
    
    /* ボタンのスタイルリセット */
    background: transparent;
    border: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .menu-icon span {
    display: block;
    height: 4px;
    width: 100%;
    background: var(--on-primary); /* テーマカラー適用 */
    border-radius: 2px;
    transition: all 0.4s ease;
    transform-origin: center;
  }

  .menu-icon.open span {
    background-color: var(--primary); 
  }

  /* === ハンバーガー変形アニメーション === */
  /* 上の線: 回転して下へ */
  .menu-icon.open span:nth-child(1) {
    transform: translateY(13px) rotate(45deg);
  }
  /* 真ん中の線: 消える */
  .menu-icon.open span:nth-child(2) {
    opacity: 0;
  }
  /* 下の線: 回転して上へ */
  .menu-icon.open span:nth-child(3) {
    transform: translateY(-13px) rotate(-45deg);
  }

  /* === オーバーレイ === */
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5); /* 半透明の黒 */
    z-index: 999;
  }

  /* === メニュー本体 === */
  .menu {
    position: fixed;
    top: 0;
    left: -280px; /* 初期位置：画面外 */
    width: 280px;
    height: 100%;
    
    /* テーマカラー適用 */
    background: var(--bg);
    color: var(--text);
    box-shadow: 4px 0 10px var(--shadow);
    
    transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1000;
    padding-top: 80px; /* アイコンとかぶらないように余白 */
    box-sizing: border-box;
  }

  .menu.open {
    left: 0; /* 出現 */
  }

  .menu ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .menu li {
    border-bottom: 1px solid var(--outline-sub);
  }

  .menu a {
    display: block;
    padding: 20px 30px;
    text-decoration: none;
    color: var(--text);
    font-size: 1.1rem;
    font-weight: 500;
    transition: var(--bg) 0.2s, color 0.2s;
  }

  .menu a:hover {
    background-color: var(--primary-container);
    color: var(--primary);
  }

  .footer-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: auto;
    padding: 20px 0;
  } 

  .footer-logo {
    height: 40px;
    width: auto;
    margin-top: 50px;
    transition: filter 0.3s;
  }
</style>