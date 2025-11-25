<script lang="ts">
	import { requestItems } from '$lib/features/request/requestItems';
	import { Button } from '$lib';

	/**
	 * @component RequestItemModal
	 * @prop show
	 * @description
	 * モーダルを開くか閉じるかを制御するブール値。
	 * bind:show={...} で双方向にバインドされます。
	 *
	 * @see /routes/community/request/others/+page.svelte - 主な呼び出し元の確認ページ
	 */

	export let show: boolean = false;

	let newItemName: string = '';
  let newItemValue: number = 1;
  const maxValue = 100;

	function closeModal() {
		show = false;
	}

	// 背景クリック時の処理
	function handleBackdropClick(event: MouseEvent | KeyboardEvent) {
		if (event instanceof KeyboardEvent && event.key !== 'Enter' && event.key !== ' ') {
			return;
		}

		if (event.target === event.currentTarget) {
			closeModal();
		}
	}

  // 追加処理
	function addItem() {
		if (newItemName.trim() !== '') {
			requestItems.update((currentItems) => {
				const newItem = {
					text: newItemName.trim(),
          value: newItemValue
				};
				return [...currentItems, newItem];
			});

      // リセット
			newItemName = '';
      newItemValue = 1;
			closeModal();
		}
	}

	// Escキーでモーダルを閉じる
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			closeModal();
		}
	}
</script>

<!-- 
  Svelteの <svelte:window> を使うと、
  ウィンドウレベルでのイベント（ここでは 'keydown'）を
  コンポーネント内から監視できます。
-->
<svelte:window on:keydown={handleKeydown} />

{#if show}
	<div
		class="modal-overlay"
		role="button"
		tabindex="0"
		on:click={handleBackdropClick}
		on:keydown={handleBackdropClick}
	>
		<div class="modal-content" role="document">
			<h2>新規申請品目の追加</h2>
			<p>品目名と必要な数量を入力してください。</p>

			<div class="input-group">
				<label for="item-name">品目名:</label>
				<input type="text" id="item-name" bind:value={newItemName} placeholder="例: 頭痛薬" />
			</div>
      
      <div class="input-group">
        <label for="item-quantity">数量:</label>
        <select id="item-quantity" bind:value={newItemValue}>
          {#each Array(maxValue) as _, i}
            <option value={i}>
              {i}
            </option>
          {/each}
        </select>
      </div>

			<div class="modal-actions">
				<Button text="キャンセル" on:click={closeModal} />
				<Button text="追加" on:click={addItem} />
			</div>
		</div>
	</div>
{/if}

<style>
	.modal-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.6);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
	}

	.modal-content {
		background-color: white;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
		min-width: 400px;
		max-width: 90%;
		z-index: 1001;
		cursor: default;
	}

	h2 {
		margin-top: 0;
	}

	.input-group {
		margin: 1.5rem 0;
	}
	.input-group label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: bold;
	}
  .input-group input,
  .input-group select {
    width: 100%;
    padding: 0.5rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    background-color: white;
  }

	.modal-actions {
		display: flex;
		justify-content: flex-end;
		gap: 1rem;
	}
</style>
