<script lang="ts">
  import { goto } from '$app/navigation';
  import Button from '$lib/Button.svelte';
  // ボタン
  function homeButtonClick() {
    goto('/');
  }
</script>

<div style="text-align: center;">
<h1>申請が完了しました。</h1>
<img src="/src/lib/assets/bousai_goods.png" alt="完了画像" style="max-width: 100%; height: auto; margin: 1rem 0;" />

<div class="request_footer">
  <Button text="はじめに戻る" on:click={homeButtonClick} />
</div>
</div>