<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { RequestTable } from '$lib';

	export let show = false;

	// 親から受け取るデータ (Props)
	export let itemName: string = '';
	export let requests: any[] = [];

	$: totalPending = requests
		.filter((r: any) => r.status === 'pending')
		.reduce((sum: number, r: any) => sum + (r.number || 0), 0);
	$: unit = requests.length > 0 && requests[0].unit ? requests[0].unit : '';
	
	const dispatch = createEventDispatcher();

	function close() {
		show = false;
		dispatch('close');
	}

	// キーボード操作で背景が押されたときの処理
	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			close();
		}
	}

	// RequestTableからアイテム名クリックイベントを受け取る
  function handleTableCommunityClick(event: CustomEvent) {
    dispatch('communityClick', event.detail);
  }
</script>

{#if show}
	<div
		class="modal-backdrop"
		on:click={close}
		on:keydown={handleKeydown}
		role="button"
		tabindex="0"
		on:keydown
	>
		<div class="modal-content" on:click|stopPropagation role="document">
			<button class="close-btn" on:click={close}>✕</button>

			<div class="detail-content">
				<header>
					<h1>{itemName}</h1>
				</header>

				<div class="special-notes-card">
					<p><strong>総要請コミュニティ数:</strong> {requests.length} コミュニティ</p>
					<p>
						<strong>未対応合計数量:</strong> <span class="total-count">{totalPending} {unit}</span>
					</p>
				</div>

				<RequestTable
          {requests}
          viewMode="item"
          on:communityClick={handleTableCommunityClick}
        />
			</div>
		</div>
	</div>
{/if}

<style>
	/* モーダルスタイル */
	.modal-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		z-index: 10000;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.modal-content {
		background: var(--bg);
		color: var(--text);
		width: 90%;
		max-width: 900px;
		max-height: 90vh;
		overflow-y: auto;
		border-radius: 12px;
		padding: 24px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
		position: relative;
	}

	.close-btn {
		position: absolute;
		top: 16px;
		right: 16px;
		background: transparent;
		border: none;
		font-size: 1.5rem;
		cursor: pointer;
		color: var(--text-sub);
		z-index: 10;
	}
	.close-btn:hover {
		color: var(--text);
	}

	/* コンテンツスタイル */
	.detail-content {
		width: 100%;
		font-family: sans-serif;
		color: var(--text);
	}

	header {
		border-bottom: 2px solid var(--primary);
		padding-bottom: 10px;
		margin-bottom: 20px;
		margin-right: 30px; /* 閉じるボタン避け */
	}

	h1 {
		color: var(--primary);
		margin: 0 0 10px 0;
		font-size: 1.5rem;
	}

	.info-bar span {
		margin-right: 20px;
		font-size: 1.1em;
		color: var(--text-sub);
	}

	/* 特記事項のスタイル */
	.special-notes-card {
		background-color: var(--card-high);
		border: 1px solid var(--outline-sub);
		border-left: 5px solid var(--accent);
		padding: 15px;
		margin-bottom: 25px;
		border-radius: 4px;
	}

	.special-notes-card h3 {
		margin-top: 0;
		color: var(--accent);
		font-size: 1.1em;
		display: flex;
		align-items: center;
	}

	.note-content {
		margin-bottom: 0;
		font-size: 1.1em;
		color: var(--text);
		font-weight: bold;
	}

	.total-count {
		font-size: 1.2em;
		font-weight: bold;
		color: #d35400;
	}
</style>
