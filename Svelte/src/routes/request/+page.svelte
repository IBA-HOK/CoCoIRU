<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/Button.svelte';
	import { requestItems } from '$lib/requestItems';


	// 最大値は99
	const maxQuantity = 100;
	// $: は、依存する変数(items)が変更されるたびに自動で再計算します
  $: totalSelected = $requestItems.reduce((sum, requestItems) => sum + requestItems.value, 0);

	// ボタン
	function othersButtonClick() {
		goto('/request/others');
	}
	function homeButtonClick() {
		goto('/');
	}
	function confirmButtonClick() {
		goto('/request/confirm');
	}
</script>

<img src="/src/lib/features/request/shopping_cart.svg" alt="ショッピングカート" class="shopping_cart"/>
<div class=confirm>
	<h2>注文確認：</h2>
	<h2>{totalSelected}</h2>
</div>	
<div class="button-grid">
	{#each $requestItems as item}
		<div class="grid-item-container">
			<Button text={item.text} on:click={() => console.log(item.text)} />

			<select bind:value={item.value}>
				{#each Array(maxQuantity) as _, i}
					<option value={i}>
						{i}
					</option>
				{/each}
			</select>
		</div>
	{/each}
</div>
<div style="text-align: center;">
	<Button text="その他申請" on:click={othersButtonClick} />
</div>
<div class="request_footer">
	<Button text="はじめに戻る" on:click={homeButtonClick} />
	<Button text="注文確定" on:click={confirmButtonClick} />
</div>

<details>
	<summary>現在の全データ（デバッグ用）</summary>
	<pre>{JSON.stringify(requestItems, null, 2)}</pre>
</details>

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
		grid-template-columns: repeat(4, 1fr);
		margin: 5%;
		gap: 15px;
	}
	.grid-item-container {
		display: flex;
		gap: 8px;
		align-items: center;
	}
	.grid-item-container :global(button) {
		flex: 1;
	}
	select {
		font-size: 1rem;
		padding: 8px;
		border-radius: 4px;
		border: 1px solid #ccc;
		flex-basis: 80px;
	}

	.request_footer {
		padding-top: 50px;
		display: flex;
		justify-content: space-evenly;
	}

	/*  デバック用 */
	pre {
		background-color: #f4f4f4;
		padding: 10px;
		border-radius: 4px;
	}
</style>
