<script lang="ts">
	// 最小実装のヘッダー
	import { goto } from '$app/navigation';

	/**
	 * ホームボタン押下時の挙動:
	 * - ログイン情報は保持（何も消さない）
	 * - 申請入力をリセットするためのフラグを sessionStorage にセット
	 * - window に 'resetApplicationForm' カスタムイベントを dispatch
	 * - その後クライアントナビゲーションで / に遷移する
	 *
	 * ページ側では以下のどちらかで受け取れます：
	 *  - window.addEventListener('resetApplicationForm', ...) で受け取る
	 *  - マウント時に sessionStorage.getItem('resetApplicationForm') を確認して初期化
	 */
	function onHomeClick(e: MouseEvent) {
		e.preventDefault();

		try {
			// 既存の申請入力保存キーの例を消す（万が一使われている場合の保険）
			sessionStorage.removeItem('applicationForm');
			sessionStorage.removeItem('applicationFormData');

			// リセットフラグ（タイムスタンプ）を入れてイベントを発火
			const ts = Date.now().toString();
			sessionStorage.setItem('resetApplicationForm', ts);
			window.dispatchEvent(new CustomEvent('resetApplicationForm', { detail: { ts } }));
		} catch (err) {
			// sessionStorage 使えない場合はフォールバックで event のみ発火
			window.dispatchEvent(new CustomEvent('resetApplicationForm'));
		}

		// SvelteKit の goto で遷移（クライアント側ルーティング）
		goto('/');
	}
</script>

<header role="banner" class="app-header">
	<div class="container">
		<a href="/" class="home-btn" aria-label="トップに戻る">トップに戻る</a>
		<a href="/community" class="login-btn" aria-label="コミュニティへ">Login</a>
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
		position: relative; /* for absolute-positioned login button */
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

	.home-btn {
		position: absolute;
		left: 0;
		top: 50%;
		transform: translateY(-50%);
		display: inline-block;
		padding: 0.35rem 0.7rem;
		border-radius: 6px;
		background: rgba(255,255,255,0.08);
		color: #ffffff;
		text-decoration: none;
		border: 1px solid rgba(255,255,255,0.15);
		font-weight: 700;
	}

	.home-btn:hover,
	.home-btn:focus {
		background: rgba(255,255,255,0.14);
		outline: none;
		box-shadow: 0 0 0 3px rgba(255,255,255,0.04);
	}

	.login-btn {
		position: absolute;
		right: 0;
		top: 50%;
		transform: translateY(-50%);
		display: inline-block;
		padding: 0.35rem 0.7rem;
		border-radius: 6px;
		background: rgba(255,255,255,0.08);
		color: #ffffff;
		text-decoration: none;
		border: 1px solid rgba(255,255,255,0.15);
		font-weight: 700;
	}

	.login-btn:hover,
	.login-btn:focus {
		background: rgba(255,255,255,0.14);
		outline: none;
		box-shadow: 0 0 0 3px rgba(255,255,255,0.04);
	}

	@media (min-width: 768px) {
		.title {
			font-size: 2.6rem;
		}
	}
</style>

