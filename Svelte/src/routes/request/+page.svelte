<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/Button.svelte';
	import cartIcon from '$lib/assets/shopping_cart.svg';

	// 申請物資のリスト
	let items = [
		{ text: '食料', selectedValue: 0 },
		{ text: '毛布', selectedValue: 0 },
		{ text: '乳児用粉・液体ミルク', selectedValue: 0 },
		{ text: '乳児・小児用おむつ', selectedValue: 0 },
		{ text: '生理用品', selectedValue: 0 },
		{ text: 'トイレットペーパー', selectedValue: 0 },
		{ text: '簡易・携帯トイレ', selectedValue: 0 },
		{ text: '大人用おむつ', selectedValue: 0 }
	];

	// 最大値は99
	const maxQuantity = 100;
	// $: は、依存する変数(items)が変更されるたびに自動で再計算します
  $: totalSelected = items.reduce((sum, item) => sum + item.selectedValue, 0);

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

<h1>申請画面</h1>
<img src={cartIcon} alt="ショッピングカート" class=shopping_cart/>
<div class=confirm>
	<h2>注文確認：</h2>
	<h2>{totalSelected}</h2>
</div>	
<div class="button-grid">
	{#each items as item}
		<div class="grid-item-container">
			<Button text={item.text} on:click={() => console.log(item.text)} />

			<select bind:value={item.selectedValue}>
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
	<pre>{JSON.stringify(items, null, 2)}</pre>
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
