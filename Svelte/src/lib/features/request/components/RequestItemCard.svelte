<script lang="ts">
	/**
	 * @component RequestItemCard
	 * @description 申請アイテムを表示するカード、または追加ボタンとして機能する
	 */

	import { requestItems } from '$lib/features/request/requestItems';
	// item は通常モードでは必須、追加ボタンモードでは不要なので optional にします
	export let item: { text: string; value: number } | undefined = undefined;

	// 追加ボタンとして表示するかどうかのフラグ
	export let isAddButton: boolean = false;

	const maxQuantity = 100;
</script>

<div
	class="card"
	class:selected={!isAddButton && item && item.value > 0}
	class:add-button={isAddButton}
	on:click
	role="button"
	tabindex="0"
	on:keypress
>
	<div class="card-content">
		{#if isAddButton}
			<span class="plus-icon">＋</span>
			<span class="add-text">項目を増やす</span>
		{:else if item}
			<div class="item-name">
				{item.text}
			</div>

			<div class="control-area" on:click|stopPropagation>
				<select bind:value={item.value} on:change={() => requestItems.update((n) => n)}>
					{#each Array(maxQuantity) as _, i}
						<option value={i}>
							{i}
						</option>
					{/each}
				</select>
				<span class="unit">個</span>
			</div>
		{/if}
	</div>
</div>

<style>
	.card {
		background-color: var(--card-high);
		border: 1px solid var(--outline-sub);
		border-radius: 8px;
		padding: 16px;
		height: 100%;
		min-height: 160px;
		box-sizing: border-box;
		transition: all 0.2s ease;
		display: flex;
		flex-direction: column;
		justify-content: center;
		position: relative;
		color: var(--text);
	}

	/* --- 通常時のスタイル（選択中） --- */
	.card.selected {
		border-color: var(--primary);
		background-color: var(--primary-container);
		box-shadow: 0 2px 8px color-mix(in srgb, var(--primary), transparent 80%);
	}

	/* --- 追加ボタンモードのスタイル --- */
	.card.add-button {
		background-color: transparent;
		border: 2px dashed var(--outline);
		cursor: pointer;
		color: var(--text-sub);
	}

	.card.add-button:hover {
		background-color: var(--primary-container);
		border-color: var(--primary);
		color: var(--on-primary-container);
	}

	.plus-icon {
		font-size: 3rem;
		font-weight: bold;
		line-height: 1;
		margin-bottom: 0.5rem;
	}

	.add-text {
		font-size: 1rem;
		font-weight: bold;
	}

	/* --- 共通レイアウト --- */
	.card-content {
		display: flex;
		flex-direction: column;
		gap: 12px;
		align-items: center;
		width: 100%;
	}

	.item-name {
		font-weight: bold;
		font-size: 1rem;
		text-align: center;
		line-height: 1.4;
		word-break: break-word;
	}
	.card.selected .item-name {
		color: var(--on-primary-container);
	}

	.control-area {
		display: flex;
		align-items: center;
		gap: 8px;
		width: 100%;
		justify-content: center;
	}

	select {
		font-size: 1rem;
		padding: 8px;
		border-radius: 4px;
		border: 1px solid var(--outline);
		background-color: var(--bg);
		color: var(--text);
		width: 100%;
		max-width: 100px;
		cursor: pointer;
	}

	.unit {
		font-size: 0.9rem;
		color: var(--text-sub);
		white-space: nowrap;
	}

	.selected select {
		border-color: var(--primary);
		background-color: var(--bg);
	}

	.selected .unit {
		color: var(--on-primary-container);
	}
</style>
