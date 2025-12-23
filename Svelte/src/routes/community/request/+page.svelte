<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { Button, Surface, Title } from '$lib';
	import { requestItems } from '$lib/features/request/requestItems';
	import type { RequestItem } from '$lib/features/request/requestItems';
	import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
	import AddRequestItemModal from '$lib/features/request/components/AddRequestItemModal.svelte';
	import RequestItemGrid from '$lib/features/request/components/RequestItemGrid.svelte';
	import RequestNoteInput from '$lib/features/request/components/RequestNoteInput.svelte';
	import { requestNote } from '$lib/features/request/requestNoteStore';
	import { communityId } from '$lib/stores/auth';

	// $: は、依存する変数(items)が変更されるたびに自動で再計算します
	$: selectedItems = $requestItems.filter((item) => item.value > 0);
	$: totalSelected = $requestItems.reduce((sum, item) => sum + item.value, 0);
	let showModal = false;
	let notes = '';
	// サイドバーのDOM要素を格納する変数
	let sidebarElement: HTMLElement;
	let showMobileButton = true;

	// --- confirm modal (統合: /community/request/confirm の内容) ---
	let isConfirmOpen = false;
	const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';
	let currentCommunityId: number | null = null;

	// community_id を store から取得（数値でない場合は null）
	$: currentCommunityId = null;
	$: if (typeof $communityId !== 'undefined' && $communityId !== null) {
		const s = String($communityId);
		currentCommunityId = /^\d+$/.test(s) ? Number(s) : null;
	}

	function openConfirm() {
		isConfirmOpen = true;
	}

	function closeConfirm() {
		isConfirmOpen = false;
		try {
			sessionStorage.removeItem('openRequestConfirmModal');
		} catch (e) {}
	}

	function confirmButtonClick() {
		openConfirm();
	}

	async function createOneRequest(item: RequestItem) {
		const rcPayload = {
			items_id: item.id,
			number: item.value,
			other_note: $requestNote
		};

		const rcRes = await fetch(`${API_BASE}/api/v1/request_content/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify(rcPayload)
		});

		if (!rcRes.ok) {
			console.error(await rcRes.text());
			throw new Error('RequestContent 作成失敗');
		}

		const rcData = await rcRes.json();
		const request_content_id = rcData.request_content_id;

		if (!currentCommunityId) {
			throw new Error('コミュニティIDが不正です。コミュニティにログインしてください。');
		}
		const srPayload = {
			community_id: currentCommunityId,
			request_content_id,
			status: 'pending'
		};

		const srRes = await fetch(`${API_BASE}/api/v1/support_requests/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify(srPayload)
		});

		if (!srRes.ok) {
			console.error(await srRes.text());
			throw new Error('SupportRequest 作成失敗');
		}

		return await srRes.json();
	}

	async function saveAllRequests() {
		const results = [];
		for (const item of selectedItems as RequestItem[]) {
			const result = await createOneRequest(item);
			results.push(result);
		}
		return results;
	}

	async function orderButtonClick() {
		try {
			const results = await saveAllRequests();
			console.log('保存された申請:', results);
			closeConfirm();
			goto('/community/request/complete');
		} catch (err) {
			console.error(err);
			alert('申請処理中にエラーが発生しました');
		}
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

	// /community/request/confirm からの遷移などで確認モーダルを開く
	onMount(() => {
		try {
			if (sessionStorage.getItem('openRequestConfirmModal')) {
				openConfirm();
				sessionStorage.removeItem('openRequestConfirmModal');
			}
		} catch (e) {}
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

{#if isConfirmOpen}
	<div class="modal" role="dialog" aria-modal="true" on:click={closeConfirm}>
		<div class="modal-content" on:click|stopPropagation>
			<button class="close" type="button" aria-label="閉じる" on:click={closeConfirm}>&times;</button>

			<div class="confirm-container">
				<Surface class="confirm-card">
					<div class="header-area">
						<h1 class="page-title">申請内容の確認</h1>
						<p class="page-subtitle">以下の内容で申請します。漏れがないかご確認ください。</p>
					</div>

					<section class="section-card flex-grow-card">
						<h2 class="section-title">申請品目</h2>
						<div class="list-wrapper">
							<RequestItemList items={selectedItems} />
						</div>
					</section>

					<section class="section-card">
						<RequestNoteInput />
					</section>

					<div class="request_footer">
						<div class="btn-area">
							<Button text="戻る" variant="secondary" on:click={closeConfirm} />
						</div>
						<div class="btn-area">
							<Button text="申請" variant="accent" on:click={orderButtonClick} />
						</div>
					</div>
				</Surface>
			</div>
		</div>
	</div>
{/if}

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

	/* confirm modal (request/confirm 統合) */
	.modal {
		position: fixed;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 16px;
		background: color-mix(in srgb, var(--shadow), transparent 60%);
		z-index: 1000;
	}

	.modal-content {
		position: relative;
		width: min(900px, 100%);
		max-height: calc(100vh - 32px);
		overflow: auto;
		background: var(--bg);
		border: 1px solid var(--outline-sub);
		border-radius: 12px;
		padding: 16px;
		box-shadow: 0 8px 24px var(--shadow);
	}

	.close {
		position: absolute;
		top: 10px;
		right: 12px;
		width: 40px;
		height: 40px;
		border-radius: 9999px;
		border: 1px solid var(--outline-sub);
		background: var(--card-high);
		color: var(--text);
		cursor: pointer;
		font-size: 24px;
		line-height: 1;
	}

	.confirm-container {
		max-width: 800px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
	}

	:global(.confirm-card) {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.header-area {
		text-align: center;
		margin-bottom: 0.5rem;
		flex-shrink: 0;
	}

	.page-title {
		margin: 0 0 0.5rem 0;
		color: var(--text);
		font-size: 1.5rem;
	}

	.page-subtitle {
		color: var(--text-sub);
		margin: 0;
		font-size: 0.9rem;
	}

	.flex-grow-card {
		flex: 1;
		min-height: 0;
		display: flex;
		flex-direction: column;
		padding-bottom: 0;
	}

	.list-wrapper {
		flex: 1;
		overflow-y: auto;
		padding-bottom: 24px;
	}

	.request_footer {
		display: flex;
		justify-content: center;
		gap: 24px;
		margin-top: 0;
		padding-bottom: 0;
		flex-shrink: 0;
	}

	.btn-area {
		flex: 1;
		max-width: 200px;
	}
</style>
