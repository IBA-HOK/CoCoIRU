<script lang="ts">
  import { page } from '$app/stores';
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
	$: isActive = (path: string) => $page.url.pathname.startsWith(path);
</script>

<header class="main-header">
  <a href="/" class="logo-link">
    <span class="logo-text">コミュニティ</span>
  </a>

  <nav class="main-nav">
    <a 
      href="/community/community_Login/login" 
      class="nav-item" 
      class:active={isActive('/community/community_Login')}
    >
      ログイン
    </a>
    <a 
      href="/community/request" 
      class="nav-item" 
      class:active={isActive('/community/request')}
    >
      物品申請
    </a>
    <a 
      href="/community/addItemRequest" 
      class="nav-item" 
      class:active={isActive('/community/addItemRequest')}
    >
      項目追加
    </a>
  </nav>
</header>

<style>
  .main-header {
    background: linear-gradient(to right, var(--primary), var(--accent));
    color: var(--on-primary);
    padding: 20px 50px;
    display: flex;
    align-items: center;
  }

  /* ロゴのリンク */
  .logo-img img {
    height: 40px;
    width: auto;
  }

  .logo-link {
    text-decoration: none;
    color: var(--on-primary);
    margin-right: 40px;
    font-size: 1.4em;
    font-weight: bold;
    transition: opacity 0.2s;
  }
  .logo-link:hover {
    opacity: 0.8;
  }

  /* ナビゲーションコンテナ */
  .main-nav {
    display: flex;
    gap: 25px;
    margin-left: auto;
  }

  /* ナビゲーションアイテム（リンク） */
  .nav-item {
    text-decoration: none;
    color: var(--on-primary);
    opacity: 0.7;
    
    padding: 5px 0;
    position: relative;
    transition: all 0.2s;
  }
  
  .nav-item:hover {
    opacity: 1;
  }

  /* アクティブなページ */
  .nav-item.active {
    opacity: 1;
    font-weight: bold;
  }
  
  /* アクティブ時の下線 */
  .nav-item.active::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--on-primary);
    border-radius: 2px;
  }
</style>