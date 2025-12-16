<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { Button, Surface, Title } from '$lib';
	import { requestItems } from '$lib/features/request/requestItems';
	import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
	import AddRequestItemModal from '$lib/features/request/components/AddRequestItemModal.svelte';
	import RequestItemGrid from '$lib/features/request/components/RequestItemGrid.svelte';
	import RequestNoteInput from '$lib/features/request/components/RequestNoteInput.svelte';

	// $: は、依存する変数(items)が変更されるたびに自動で再計算します
	$: selectedItems = $requestItems.filter((item) => item.value > 0);
	$: totalSelected = $requestItems.reduce((sum, item) => sum + item.value, 0);
	let showModal = false;
	let notes = '';
	// サイドバーのDOM要素を格納する変数
	let sidebarElement: HTMLElement;
	let showMobileButton = true;

	function confirmButtonClick() {
		goto('/community/request/confirm');
	}
	// サイドバーへスムーズスクロールする関数
	function scrollToSidebar() {
		if (sidebarElement) {
			sidebarElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
		}
	}

	// サイドバーが見えているかどうかを監視する
	onMount(() => {
		if (!sidebarElement) return;

		const observer = new IntersectionObserver(
			(entries) => {
				const entry = entries[0];
				showMobileButton = !entry.isIntersecting;
			},
			{
				root: null,
				threshold: 0.1
			}
		);

		observer.observe(sidebarElement);

		return () => {
			observer.disconnect();
		};
	});

	// ページ表示時にヘッダーの onHomeClick と同等のリセット処理を行う
	onMount(() => {
		try {
			// 既存の申請入力保存キーを消す
			sessionStorage.removeItem('applicationForm');
			sessionStorage.removeItem('applicationFormData');

			// リセットフラグ（タイムスタンプ）を入れてイベントを発火
			const ts = Date.now().toString();
			sessionStorage.setItem('resetApplicationForm', ts);
			window.dispatchEvent(new CustomEvent('resetApplicationForm', { detail: { ts } }));
		} catch (err) {
			window.dispatchEvent(new CustomEvent('resetApplicationForm'));
		}

		// requestItems の数量をリセットする
		try {
			requestItems.update((items) => items.map((it) => ({ ...it, value: 0 })));
		} catch (e) {
			console.error('failed to reset requestItems', e);
		}
	});
</script>

<Title titleText="支援物資の申請" subtitleText="品目を選択し、「申請する」を押してください。" />
<div class="container">
	<!-- 申請品目選択カード -->
	<div class="main-content">
		<Surface>
			<h2 class="section-title">品目を選択</h2>
			<RequestItemGrid on:addClick={() => (showModal = true)} />
		</Surface>
	</div>

	<!-- 選択済み申請品目サイドバー -->
	<div class="sidebar-content" bind:this={sidebarElement}>
		<Surface>
			<!-- サイドバータイトル -->
			<div class="sidebar-header">
				<h2 class="section-title">選択済み</h2>
					{#if selectedItems.length > 0}
						<span class="badge">{selectedItems.length}件</span>
					{/if}
			</div>

			<!-- 選択済み品目一覧 -->
			<div class="sidebar-body">
				{#if selectedItems.length === 0}
					<p class="empty-message">アイテムが選択されていません</p>
				{:else}
					<RequestItemList items={selectedItems} />
				{/if}
			</div>

			<!-- 特記事項入力欄 --
			<!<RequestNoteInput bind:value={notes} /> -->
			<RequestNoteInput />

			<!-- 合計数量と確定ボタン -->
			<div class="sidebar-footer">
				<div class="summary-line">
					<span>合計数量:</span>
					<strong>{totalSelected} 個</strong>
				</div>
				<div class="action-button">
					<Button text="申請する" variant="accent" on:click={confirmButtonClick} />
				</div>
			</div>
		</Surface>
	</div>
</div>

<!-- モバイル用：サイドバーへスクロールするボタン -->
<div class="mobile-action-bar {showMobileButton ? '' : 'hidden'}">
	<Button text="確認 ▼" on:click={scrollToSidebar} />
</div>

<!-- 品目追加モーダル -->
<!-- <AddRequestItemModal bind:show={showModal} /> -->

<style>
	.container {
		margin: 0 auto;
		display: flex;
		flex-direction: row;
		align-items: stretch;
		padding-bottom: 20px;
	}

	.main-content {
		flex: 1;
		min-width: 0;
	}

	.section-title {
		margin: 0 0 1.5rem 0;
		font-size: 1.25rem;
		color: var(--text);
		font-weight: 500;
	}

	.sidebar-content {
		min-width: 30%;
		flex-shrink: 0;
	}

	.sidebar-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid var(--outline-sub);
	}

	.sidebar-body {
		flex-grow: 1;
		overflow-y: auto;
	}

	.sidebar-footer {
		border-top: 1px solid var(--outline-sub);
		padding-top: 16px;
		margin-top: auto;
		display: flex;
		flex-direction: column;
	}

	.summary-line {
		display: flex;
		justify-content: space-between;
		margin-bottom: 16px;
		font-size: 1rem;
		align-items: center;
		color: var(--text);
	}

	.action-button {
		text-align: center;
	}

	.badge {
		background-color: var(--primary-container);
		color: var(--on-primary-container);
		padding: 2px 8px;
		border-radius: 12px;
		font-size: 0.85rem;
		font-weight: bold;
	}

	.empty-message {
		color: var(--text-sub);
		text-align: center;
		padding: 20px 0;
		font-size: 0.9rem;
	}

	.mobile-action-bar {
		display: none; /* PCでは非表示 */
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		box-sizing: border-box;
		z-index: 100;
		padding: 16px 48px;
		background-color: color-mix(in srgb, var(--bg), transparent 80%);

		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
		border-top: 1px solid var(--outline-sub);
		box-shadow: 0 -2px 10px color-mix(in srgb, var(--primary), transparent 80%);

		transition:
			transform 0.3s ease,
			opacity 0.3s ease;
		transform: translateY(0);
		opacity: 1;
	}

	/* レスポンシブ対応: スマホでは縦並び(要修正) */
	@media (max-width: 768px) {
		.container {
			flex-direction: column;
			text-align: center;
			align-items: stretch;
			padding-bottom: 80px;
		}

		.sidebar-content {
			width: 100%;
			height: auto;
			scroll-margin-top: 20px;
		}

		.mobile-action-bar {
			display: flex;
			justify-content: center;
		}

		.mobile-action-bar.hidden {
			transform: translateY(100%); /* 下にスライドさせて隠す */
			opacity: 0;
			pointer-events: none; /* クリックできないようにする */
		}
	}
</style>
