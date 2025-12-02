<svelte:head>
  <meta name="robots" content="noindex" />
  <title>コミュニティ</title>
</svelte:head>
<header class="community-header" role="banner">
  <div class="container">
    <h1 class="title">コミュニティ</h1>
    <nav class="actions" aria-label="community header actions">
      <a class="home-btn" href="/">ホーム</a>
      <a class="login-btn" href="/community">ログイン</a>
    </nav>
  </div>
</header>

<slot />

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
</style>
