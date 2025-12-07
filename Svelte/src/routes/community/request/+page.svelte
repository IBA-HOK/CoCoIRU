<script lang="ts">
	import { goto } from '$app/navigation';
	import { Button } from '$lib';
	import { requestItems } from '$lib/features/request/requestItems';
	import RequestItemCard from '$lib/features/request/components/RequestItemCard.svelte';
	import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';

	// $: は、依存する変数(items)が変更されるたびに自動で再計算します
	$: totalSelected = $requestItems.reduce((sum, requestItems) => sum + requestItems.value, 0);
	$: selectedItems = $requestItems.filter((requestItems) => requestItems.value > 0);

	// ボタン
	function othersButtonClick() {
		goto('/community/request/others');
	}
	function homeButtonClick() {
		goto('/community');
	}
	function confirmButtonClick() {
		goto('/community/request/confirm');
	}
</script>

<img
	src="/src/lib/features/request/shopping_cart.svg"
	alt="ショッピングカート"
	class="shopping_cart"
/>
<div class="confirm">
	<h2>注文確認：</h2>
	<h2>{totalSelected}</h2>
</div>

<div class="container">
	<div class="main-content" id="mainContent">
		<div class="button-grid">
			{#each $requestItems as item}
				<RequestItemCard {item} />
			{/each}
		</div>
		<div style="text-align: center;">
			<Button text="その他申請" on:click={othersButtonClick} />
		</div>
	</div>
	<div class="sidebar">
		<RequestItemList items={selectedItems} />
	</div>
</div>

<div class="request_footer">
	<Button text="はじめに戻る" on:click={homeButtonClick} />
	<Button text="注文確定" on:click={confirmButtonClick} />
</div>

<style>
	.shopping_cart {
		width: 200px;
		height: auto;
		display: block;
		margin: 0 auto;
	}
	.confirm {
		display: flex;
		justify-content: center;
	}
	.button-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
		margin: 5%;
		gap: 15px;
	}

	.request_footer {
		padding-top: 50px;
		display: flex;
		justify-content: space-evenly;
	}

	.container {
		display: flex;
		flex-direction: row;
	}

	.main-content {
		width: 70%;
		padding: 10px;
	}

	.sidebar {
		width: 30%;
		padding: 10px;
	}
</style>
