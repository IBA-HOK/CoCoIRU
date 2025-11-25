<script lang="ts">
  import { goto } from '$app/navigation';
	import { Button } from '$lib';
  // ボタン
  function homeButtonClick() {
    goto('/community');
  }
</script>

<div style="text-align: center;">
<h1>申請が完了しました。</h1>
<img src="/src/lib/features/request/bousai_goods.png" alt="完了画像" style="max-width: 100%; height: auto; margin: 1rem 0;" />

<div class="request_footer">
  <Button text="はじめに戻る" on:click={homeButtonClick} />
</div>
</div>