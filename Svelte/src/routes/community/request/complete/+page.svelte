<script lang="ts">
  import { goto } from '$app/navigation';
	import { Button } from '$lib';
	import Surface from '$lib/components/Surface.svelte';
  // ボタン
  function homeButtonClick() {
    goto('/community');
  }
  function loginButtonClick() {
    goto('/login');
  }
</script>

<div class="container">
  
  <!-- 完了メッセージカード -->
  <Surface>
    <h1 class="page-title">申請が完了しました</h1>
    <p class="page-subtitle">ご協力ありがとうございました。</p>
    
    <div class="image-wrapper">
      <img 
        src="/src/lib/assets/CoCoIRU_emblem.png" 
        alt="完了画像" 
        class="success-image"
      />
    </div>
  </Surface>

  <!-- フッターボタン -->
  <div class="request_footer">
    <div class="btn-area">
      <Button text="はじめに戻る" variant="primary" on:click={homeButtonClick} />
    </div>
    <div class="btn-area">
      <Button text="ログインへ" variant="secondary" on:click={loginButtonClick} />
    </div>
  </div>

</div>

<style>
  .container {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 24px;
    min-height: calc(100vh - 4rem);
    justify-content: center;
    padding: 2rem 0;
  }

  .page-title {
    margin: 0 0 0.5rem 0;
    color: var(--text);
    font-size: 1.5rem;
  }

  .page-subtitle {
    color: var(--text-sub);
    margin: 0 0 2rem 0;
    font-size: 1rem;
  }

  .image-wrapper {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .success-image {
    max-width: 100%;
    height: auto;
    max-height: 200px;
    object-fit: contain;
  }

  /* フッター */
  .request_footer {
    display: flex;
    flex-direction: column;
    gap: 16px;
    width: 100%;
    max-width: 400px;
    margin: 0 auto;
  }
  
  .btn-area {
    width: 100%;
  }

  /* 画面幅が広いときはボタンを横並びにする */
  @media (min-width: 600px) {
    .request_footer {
      flex-direction: row;
    }
  }
</style>