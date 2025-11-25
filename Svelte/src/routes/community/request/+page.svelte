<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '$lib';
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

	function confirmButtonClick() {
		goto('/community/request/confirm');
	}
</script>

<div class="container">
	<!-- 申請品目選択カード -->
	<main class="main-content surface">
		<h2 class="section-title">申請品目を選択</h2>
		<RequestItemGrid on:addClick={() => (showModal = true)} />
	</main>

	<!-- 選択済み申請品目サイドバー -->
	<aside class="sidebar surface sticky-sidebar">
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

		<!-- 特記事項入力欄 -->
		<RequestNoteInput bind:value={notes} />

		<!-- 合計数量と確定ボタン -->
		<div class="sidebar-footer">
			<div class="summary-line">
				<span>合計数量:</span>
				<strong>{totalSelected} 個</strong>
			</div>
			<div class="action-button">
				<Button text="申請する" on:click={confirmButtonClick} />
			</div>
		</div>
	</aside>
</div>

<!-- 品目追加モーダル -->
<AddRequestItemModal bind:show={showModal} />

<style>
	.container {
		margin: 0 auto;
		display: flex;
		flex-direction: row;
		gap: 24px;
		align-items: stretch;
	}

	/* --- 共通のカード（Surface）スタイル --- */
	.surface {
		background-color: var(--card);
		border-radius: 16px;
		box-shadow:
			0 2px 4px color-mix(in srgb, var(--shadow), transparent 95%),
			0 0 1px color-mix(in srgb, var(--shadow), transparent 90%);
		padding: 24px;
		border: 1px solid var(--outline-sub);
	}

	/* --- メインコンテンツ --- */
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

	/* --- サイドバー --- */
	.sidebar {
		width: 480px;
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.sticky-sidebar {
		position: sticky;
		top: 24px;
		max-height: calc(100vh - 48px);
		overflow-y: auto;
	}

	.sidebar-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid var(--outline-sub);
		padding-bottom: 12px;
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
		gap: 16px;
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

	/* レスポンシブ対応: スマホでは縦並び(要修正) */
	@media (max-width: 768px) {
		.container {
			flex-direction: column;
			text-align: center;
		}
		.sidebar {
			width: 100vh;
			position: static;
		}
	}
</style>
