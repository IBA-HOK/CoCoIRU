<script lang="ts">
	// 最小実装のヘッダー
</script>

<header role="banner" class="app-header">
	<div class="container">
		<h1 class="title">申請画面</h1>
	</div>
</header>

<style>
	/* Googleフォント読み込み（ネットワーク接続がある場合に有効） */
	@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');

	.app-header {
		background-color: #2ecc71; /* 明るい緑 */
		padding: 1rem;
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.title {
		color: #ffffff;
		font-size: 1.9rem;
		margin: 0;
		font-weight: 900; /* 太字 */
		font-family: 'Noto Sans JP', 'Yu Gothic', 'Meiryo', system-ui, -apple-system, 'Hiragino Kaku Gothic ProN', sans-serif;
		letter-spacing: 0.02em;
		text-transform: none;
	}

	@media (min-width: 768px) {
		.title {
			font-size: 2.6rem;
		}
	}
</style>

