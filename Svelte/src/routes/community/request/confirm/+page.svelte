<script lang="ts">
	import { goto } from '$app/navigation';
	import { requestItems } from '$lib/features/request/requestItems';
	import { Button } from '$lib';
	import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
	import RequestNoteInput from '$lib/features/request/components/RequestNoteInput.svelte';

	// 特記事項
	let notes = '';

	$: selectedItems = $requestItems.filter((requestItems) => requestItems.value > 0);

	// ボタン
	function backButtonClick() {
		goto('/community/request');
	}
	function orderButtonClick() {
		// 仮の処理
		console.log('注文内容:', selectedItems);
		console.log('特記事項:', notes);
		goto('/community/request/complete');
	}
</script>

<div class="page-wrapper">
	<div class="container">
		<div class="header-area">
			<h1 class="page-title">申請内容の確認</h1>
			<p class="page-subtitle">以下の内容で申請します。漏れがないかご確認ください。</p>
		</div>

		<section class="section-card surface flex-grow-card">
			<h2 class="section-title">選択したアイテム</h2>
			<div class="list-wrapper">
				<RequestItemList items={selectedItems} />
			</div>
		</section>

		<section class="section-card">
			<RequestNoteInput bind:value={notes} />
		</section>

		<div class="request_footer">
			<div class="btn-area back-btn">
				<Button text="戻る" on:click={backButtonClick} />
			</div>
			<div class="btn-area order-btn">
				<Button text="申請" on:click={orderButtonClick} />
			</div>
		</div>
	</div>
</div>

<style>
	.container {
		max-width: 600px;
    min-height: 600px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 24px;
    height: calc(100vh - 4rem);
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

	/* カード（Surface）スタイル */
	.surface {
		background-color: var(--card);
		border-radius: 16px;
		padding: 24px;
		box-shadow:
			0 2px 4px color-mix(in srgb, var(--shadow), transparent 95%),
			0 0 1px color-mix(in srgb, var(--shadow), transparent 90%);
		border: 1px solid var(--outline-sub);
	}

  .flex-grow-card {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    padding-bottom: 0;
  }

	.section-title {
		margin: 0 0 16px 0;
		font-size: 1.1rem;
		color: var(--text);
		border-bottom: 1px solid var(--outline-sub);
		padding-bottom: 8px;
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

	.back-btn {
		--primary: var(--md-sys-color-surface-variant);
		--on-primary: var(--text);

		--primary-container: var(--md-sys-color-outline);
	}

	.order-btn {
		--primary: var(--accent);
	}
</style>
