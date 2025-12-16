<script lang="ts">
  type UserType = 'community' | 'gov';
  
  let userType: UserType = 'gov';
  let username = 'gov_admin';
  let communityId = '';
  let password = 'gov_admin_pass';
  let isSubmitting = false;
  let loginResponse: any = null;
  let userInfo: any = null;
  let errorMessage: string | null = null;
  let isLoggedIn = false;

  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  import { setToken } from '$lib/stores/auth';

  async function handleLogin(event: SubmitEvent) {
    event.preventDefault();
    isSubmitting = true;
    errorMessage = null;
    loginResponse = null;
    userInfo = null;

    try {
      const body: any = {
        user_type: userType,
        password
      };

      if (userType === 'gov') {
        body.username = username;
      } else {
        body.community_id = Number(communityId);
      }

      const response = await fetch(`${API_BASE}/api/v1/login/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include', // Cookie送受信を有効化
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        const detail = await response.json();
        throw new Error(detail.detail || 'ログインに失敗しました');
      }

      const data = await response.json();
      loginResponse = data;
      if (data && data.access_token) {
        try { setToken(data.access_token); } catch (e) {}
      }
      isLoggedIn = true;
      
      // ログイン成功後、ユーザー情報を取得
      await fetchUserInfo();
    } catch (error) {
      console.error(error);
      errorMessage = error instanceof Error ? error.message : '予期せぬエラーが発生しました';
    } finally {
      isSubmitting = false;
    }
  }

  async function fetchUserInfo() {
    try {
      const response = await fetch(`${API_BASE}/api/v1/login/me`, {
        method: 'GET',
        credentials: 'include' // Cookieを自動送信
      });

      if (!response.ok) {
        throw new Error('ユーザー情報の取得に失敗しました');
      }

      const data = await response.json();
      userInfo = data;
    } catch (error) {
      console.error(error);
      errorMessage = error instanceof Error ? error.message : 'ユーザー情報取得エラー';
    }
  }

  async function handleLogout() {
    isSubmitting = true;
    errorMessage = null;

    try {
      const response = await fetch(`${API_BASE}/api/v1/login/logout`, {
        method: 'POST',
        credentials: 'include' // Cookieを送信
      });

      if (!response.ok) {
        throw new Error('ログアウトに失敗しました');
      }

      // 状態をリセット
      loginResponse = null;
      userInfo = null;
      isLoggedIn = false;
      password = userType === 'gov' ? 'gov_admin_pass' : '';
    } catch (error) {
      console.error(error);
      errorMessage = error instanceof Error ? error.message : 'ログアウトエラー';
    } finally {
      isSubmitting = false;
    }
  }

  async function testProtectedEndpoint() {
    errorMessage = null;
    
    try {
      const response = await fetch(`${API_BASE}/api/v1/communities/`, {
        method: 'GET',
        credentials: 'include' // Cookieを自動送信
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || '保護されたエンドポイントへのアクセスに失敗しました');
      }

      const communities = await response.json();
      alert(`✅ Gov専用エンドポイントアクセス成功！\nコミュニティ数: ${communities.length}`);
    } catch (error) {
      console.error(error);
      errorMessage = error instanceof Error ? error.message : 'エンドポイントアクセスエラー';
    }
  }

  function handleUserTypeChange() {
    errorMessage = null;
    if (userType === 'gov') {
      username = 'gov_admin';
      password = 'gov_admin_pass';
    } else {
      communityId = '';
      password = '';
    }
  }
</script>

<svelte:head>
  <title>Cookie認証テスト | CoCoIRU</title>
</svelte:head>

<main class="login-page">
  <section class="card">
    <h1>🔐 Cookie認証テスト</h1>
    <p class="helper">HTTPOnly Cookie + トークンブラックリストの動作確認</p>

    {#if !isLoggedIn}
      <form on:submit|preventDefault={handleLogin}>
        <div class="radio-group">
          <label class="radio-label">
            <input 
              type="radio" 
              bind:group={userType} 
              value="gov" 
              on:change={handleUserTypeChange}
            />
            <span>Gov管理者</span>
          </label>
          <label class="radio-label">
            <input 
              type="radio" 
              bind:group={userType} 
              value="community"
              on:change={handleUserTypeChange}
            />
            <span>コミュニティ</span>
          </label>
        </div>

        {#if userType === 'gov'}
          <label>
            ユーザー名
            <input type="text" bind:value={username} placeholder="gov_admin" required />
          </label>
        {:else}
          <label>
            コミュニティID
            <input type="number" bind:value={communityId} placeholder="1" required />
          </label>
        {/if}

        <label>
          パスワード
          <input type="password" bind:value={password} placeholder="password" required />
        </label>

        <button type="submit" class="primary" disabled={isSubmitting}>
          {isSubmitting ? '送信中...' : 'ログイン'}
        </button>
      </form>
    {:else}
      <div class="logged-in">
        <div class="status-badge success">✅ ログイン中</div>
        
        {#if loginResponse}
          <div class="info-box">
            <h3>📝 ログインレスポンス</h3>
            <code>{JSON.stringify(loginResponse, null, 2)}</code>
          </div>
        {/if}

        {#if userInfo}
          <div class="info-box">
            <h3>👤 ユーザー情報 (Cookie自動送信)</h3>
            <code>{JSON.stringify(userInfo, null, 2)}</code>
          </div>
        {/if}

        <div class="button-group">
          <button class="secondary" on:click={fetchUserInfo} disabled={isSubmitting}>
            🔄 ユーザー情報を再取得
          </button>
          
          {#if userInfo?.role === 'gov'}
            <button class="secondary" on:click={testProtectedEndpoint} disabled={isSubmitting}>
              🔒 Gov専用エンドポイントテスト
            </button>
          {/if}

          <button class="danger" on:click={handleLogout} disabled={isSubmitting}>
            {isSubmitting ? '処理中...' : '🚪 ログアウト'}
          </button>
        </div>
      </div>
    {/if}

    {#if errorMessage}
      <div class="result error">
        <h3>❌ エラー</h3>
        <p>{errorMessage}</p>
      </div>
    {/if}
  </section>

  <section class="card tips">
    <h2>📋 テスト手順</h2>
    <ol>
      <li><strong>ログイン:</strong> Gov管理者 (gov_admin / gov_admin_pass) でログイン</li>
      <li><strong>Cookie確認:</strong> ブラウザの開発者ツールで <code>access_token</code> Cookieを確認</li>
      <li><strong>自動認証:</strong> 「ユーザー情報を再取得」でCookieが自動送信されることを確認</li>
      <li><strong>Gov専用アクセス:</strong> 「Gov専用エンドポイントテスト」でロールベースアクセス制御を確認</li>
      <li><strong>ログアウト:</strong> ログアウトしてトークンがブラックリストに追加されることを確認</li>
      <li><strong>再アクセステスト:</strong> ログアウト後にブラウザバックなどで再度アクセスしても401エラーになることを確認</li>
    </ol>

    <h3>🔧 実装詳細</h3>
    <ul>
      <li><code>credentials: 'include'</code> でCookieの送受信を有効化</li>
      <li>HTTPOnly Cookie なので JavaScript からは直接アクセス不可</li>
      <li>ログアウト時にサーバー側でトークンをブラックリストに登録</li>
      <li>ブラックリストされたトークンは再利用不可 (セキュリティ)</li>
    </ul>

    <h3>🌐 CORS設定</h3>
    <p class="note">
      <strong>注意:</strong> Cookie認証を使用する場合、バックエンドのCORS設定で以下が必要です:
    </p>
    <code class="cors-example">
allow_credentials=True
allow_origins=["http://localhost:5173"]
    </code>
  </section>
</main>

<style>
  .login-page {
    display: grid;
    gap: 2rem;
    padding: 3rem 1rem;
    max-width: 960px;
    margin: 0 auto;
  }

  .card {
    background: #fff;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
  }

  h1 {
    margin-bottom: 0.5rem;
  }

  .helper {
    color: #5f7082;
    margin-bottom: 1.5rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .radio-group {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 0.5rem;
  }

  .radio-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    cursor: pointer;
  }

  .radio-label input[type="radio"] {
    width: auto;
    margin: 0;
  }

  label {
    display: flex;
    flex-direction: column;
    font-weight: 600;
    color: #344054;
    gap: 0.35rem;
  }

  input[type="text"],
  input[type="number"],
  input[type="password"] {
    padding: 0.95rem 1.05rem;
    border-radius: 10px;
    border: 1px solid #d5d9df;
    font-size: 1rem;
  }

  button {
    padding: 0.95rem;
    border: none;
    border-radius: 10px;
    font-size: 1.05rem;
    cursor: pointer;
    transition: transform 120ms ease, box-shadow 120ms ease;
    font-weight: 600;
  }

  .primary {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    color: #fff;
  }

  .secondary {
    background: #f8f9fa;
    color: #344054;
    border: 1px solid #d5d9df;
  }

  .danger {
    background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    color: #fff;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  button:not(:disabled):hover {
    transform: translateY(-2px);
  }

  .primary:not(:disabled):hover {
    box-shadow: 0 10px 20px rgba(0, 114, 255, 0.25);
  }

  .danger:not(:disabled):hover {
    box-shadow: 0 10px 20px rgba(255, 65, 108, 0.25);
  }

  .logged-in {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    width: fit-content;
  }

  .status-badge.success {
    background: #d1fae5;
    color: #065f46;
  }

  .info-box {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
  }

  .info-box h3 {
    margin: 0 0 0.75rem 0;
    font-size: 0.95rem;
    color: #344054;
  }

  .button-group {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .result {
    margin-top: 1.75rem;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid transparent;
  }

  .result.error {
    border-color: #ffd7d7;
    background: #fff5f5;
  }

  .result h3 {
    margin: 0 0 0.5rem 0;
  }

  code {
    display: block;
    margin-top: 0.5rem;
    white-space: pre-wrap;
    word-break: break-all;
    font-size: 0.9rem;
    color: #0f172a;
    background: #f1f5f9;
    padding: 0.75rem;
    border-radius: 6px;
  }

  .cors-example {
    background: #1e293b;
    color: #e2e8f0;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 0.5rem;
  }

  .tips h2,
  .tips h3 {
    margin-top: 1.5rem;
  }

  .tips h2:first-child {
    margin-top: 0;
  }

  .tips ol,
  .tips ul {
    margin: 0.75rem 0;
    padding-left: 1.5rem;
    color: #475467;
    line-height: 1.7;
  }

  .tips li + li {
    margin-top: 0.5rem;
  }

  .tips li strong {
    color: #1e293b;
  }

  .note {
    margin: 0.75rem 0;
    padding: 0.75rem;
    background: #fef3c7;
    border-left: 3px solid #f59e0b;
    border-radius: 4px;
    color: #92400e;
  }
</style>
