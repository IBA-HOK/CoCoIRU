<svelte:head>
  <meta name="robots" content="noindex" />
  <title>コミュニティ</title>
</svelte:head>
<script>
  import '$lib/theme.css';
</script>
<header class="community-header" role="banner">
  <div class="container">
    <h1 class="title">コミュニティ</h1>
    <nav class="actions" aria-label="community header actions">
      <a class="home-btn" href="/">ホーム</a>
      <a class="login-btn" href="/community">ログイン</a>
    </nav>
  </div>
</header>

<div class="page-wrapper force-black">
  <slot />
</div>

<style>
  .community-header {
    background: #2ecc71;
    padding: 0.75rem 1rem;
    color: #fff;
  }
  .container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .title { margin: 0; font-weight: 800; font-size: 1.2rem }
  .actions { display:flex; gap:0.5rem }
  .home-btn, .login-btn { color: white; background: rgba(255,255,255,0.08); padding: 0.4rem 0.7rem; border-radius:6px; text-decoration:none }
  .home-btn:hover, .login-btn:hover { background: rgba(255,255,255,0.14) }

  .page-wrapper {
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem 1rem;
    box-sizing: border-box;
  }
  /* 変更: 影響範囲を限定して、テキスト要素のみ黒にする。
     ボタンや入力などのコンポーネント固有のスタイルは上書きしない。
  */
  :global(.force-black) h1,
  :global(.force-black) h2,
  :global(.force-black) h3,
  :global(.force-black) h4,
  :global(.force-black) h5,
  :global(.force-black) h6,
  :global(.force-black) p,
  :global(.force-black) span,
  :global(.force-black) li,
  :global(.force-black) label,
  :global(.force-black) strong,
  :global(.force-black) em,
  :global(.force-black) td,
  :global(.force-black) th {
    color: #000 !important;
  }
</style>
