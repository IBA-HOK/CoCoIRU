<script lang="ts">
  let communityId = '';
  let password = '';
  let isSubmitting = false;
  let token: string | null = null;
  let errorMessage: string | null = null;

  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    isSubmitting = true;
    errorMessage = null;
    token = null;

    try {
      const response = await fetch(`${API_BASE}/api/v1/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          community_id: Number(communityId),
          password
        })
      });

      if (!response.ok) {
        const detail = await response.text();
        throw new Error(detail || 'ログインに失敗しました');
      }

      const data = await response.json();
      token = data.access_token ?? data.token ?? JSON.stringify(data, null, 2);
    } catch (error) {
      console.error(error);
      errorMessage = error instanceof Error ? error.message : '予期せぬエラーが発生しました';
    } finally {
      isSubmitting = false;
    }
  }
</script>

<svelte:head>
  <title>ログイン | CoCoIRU</title>
</svelte:head>

<main class="login-page">
  <section class="card">
    <h1>ログイン</h1>
    <p class="helper">APIトークン取得のサンプルフォームです。</p>

    <form on:submit|preventDefault={handleSubmit}>
      <label>
        コミュニティID
        <input type="number" bind:value={communityId} placeholder="1" required />
      </label>

      <label>
        パスワード
        <input type="password" bind:value={password} placeholder="password" required />
      </label>

      <button type="submit" class="primary" disabled={isSubmitting}>
        {isSubmitting ? '送信中...' : 'ログイン'}
      </button>
    </form>

    {#if token}
      <div class="result success">
        <h2>受信したトークン</h2>
        <code>{token}</code>
      </div>
    {/if}

    {#if errorMessage}
      <div class="result error">
        <h2>エラー</h2>
        <p>{errorMessage}</p>
      </div>
    {/if}
  </section>

  <section class="card tips">
    <h2>サンプルAPIについて</h2>
    <ul>
      <li>バックエンドは FastAPI の OAuth2 Password Flow を想定</li>
      <li>トークンエンドポイントは <code>/api/v1/token</code></li>
      <li>コミュニティIDとパスワードで認証します</li>
      <li>環境変数 <code>VITE_API_BASE</code> を設定すると API ベースURLを差し替え可能</li>
    </ul>
  </section>
</main>

<style>
  :global(body) {
    background: #f4f7f9;
  }

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

  label {
    display: flex;
    flex-direction: column;
    font-weight: 600;
    color: #344054;
    gap: 0.35rem;
  }

  input {
    padding: 0.95rem 1.05rem;
    border-radius: 10px;
    border: 1px solid #d5d9df;
    font-size: 1rem;
  }

  .primary {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    color: #fff;
    padding: 0.95rem;
    border: none;
    border-radius: 10px;
    font-size: 1.05rem;
    cursor: pointer;
    transition: transform 120ms ease, box-shadow 120ms ease;
  }

  .primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .primary:not(:disabled):hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 114, 255, 0.25);
  }

  .result {
    margin-top: 1.75rem;
    padding: 1rem;
    border-radius: 12px;
    border: 1px solid transparent;
  }

  .result.success {
    border-color: #cce8d8;
    background: #f4fbf7;
  }

  .result.error {
    border-color: #ffd7d7;
    background: #fff5f5;
  }

  code {
    display: block;
    margin-top: 0.75rem;
    white-space: pre-wrap;
    word-break: break-all;
    font-size: 0.95rem;
    color: #0f172a;
  }

  .tips ul {
    margin: 0;
    padding-left: 1.25rem;
    color: #475467;
  }

  .tips li + li {
    margin-top: 0.4rem;
  }
</style>
