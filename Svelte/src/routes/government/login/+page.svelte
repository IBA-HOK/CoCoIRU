<script lang="ts">
  import { goto } from '$app/navigation';
  import { govLogin } from '$lib/stores/auth';

  let username = 'gov_admin';
  let password = 'gov_admin_pass';
  let isSubmitting = false;
  let errorMessage: string | null = null;

  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  async function handleLogin(event: SubmitEvent) {
    event.preventDefault();
    isSubmitting = true;
    errorMessage = null;

    try {
      const response = await fetch(`${API_BASE}/api/v1/login/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          user_type: 'gov',
          username,
          password
        })
      });

      if (!response.ok) {
        const detail = await response.json();
        throw new Error(detail.detail || 'ログインに失敗しました');
      }

      const data = await response.json();

      // Gov login success
      govLogin({ username, role: 'gov' });

      goto('/government');
    } catch (error) {
      console.error(error);
      errorMessage = error instanceof Error ? error.message : '予期せぬエラーが発生しました';
    } finally {
      isSubmitting = false;
    }
  }
</script>

<main class="login-page">
  <section class="card">
    <h1>政府管理者ログイン</h1>
    <p>政府関連ページにアクセスするにはログインが必要です。</p>

    <form on:submit|preventDefault={handleLogin}>
      <label>
        ユーザー名
        <input type="text" bind:value={username} placeholder="gov_admin" required />
      </label>

      <label>
        パスワード
        <input type="password" bind:value={password} placeholder="password" required />
      </label>

      <button type="submit" class="primary" disabled={isSubmitting}>
        {isSubmitting ? '送信中...' : 'ログイン'}
      </button>
    </form>

    {#if errorMessage}
      <div class="result error">
        <h3>❌ エラー</h3>
        <p>{errorMessage}</p>
      </div>
    {/if}
  </section>
</main>

<style>
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
  }

  .card {
    background: #fff;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
    max-width: 400px;
    width: 100%;
  }

  h1 {
    margin-bottom: 0.5rem;
    text-align: center;
  }

  p {
    color: #5f7082;
    margin-bottom: 1.5rem;
    text-align: center;
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

  input[type="text"],
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
    transition: transform 120ms ease;
    font-weight: 600;
  }

  .primary {
    background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
    color: #fff;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  button:not(:disabled):hover {
    transform: translateY(-2px);
  }

  .result.error {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 8px;
    background: #fee;
    border: 1px solid #fcc;
  }

  .result.error h3 {
    margin: 0 0 0.5rem 0;
    color: #c33;
  }

  .result.error p {
    margin: 0;
    color: #c33;
  }
</style>