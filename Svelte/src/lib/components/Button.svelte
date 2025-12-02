<script lang="ts">
	export let text = 'ボタンテキスト';
	export let variant: 'primary' | 'secondary' | 'accent' = 'primary';

	/**
	 * @component Button
	 * @description
	 * ボタンのコンポーネント
	 * variant
	 * - primary: メイン（緑）※デフォルト
	 * - secondary: サブ/戻るボタン（グレー）
	 * - accent: 強調/確定ボタン（紫）
	 */	
</script>

<button class={variant} on:click>
	{text}
</button>

<style>
	button {
		flex: 1;
		width: 100%;
		padding: 20px;
		text-decoration: none;
		border: none;
		border-radius: 8px;
		transition: all 0.2s ease;
		box-shadow: 0 4px 6px color-mix(in srgb, var(--shadow), transparent 85%);
		text-align: center;
		font-weight: bold;
		font-size: 1.5rem;
		cursor: pointer;
		font-family: inherit;
    
    --btn-bg: var(--primary);
    --btn-text: var(--on-primary);
    background-color: var(--btn-bg);
    color: var(--btn-text);
	}

  button.secondary {
    --btn-bg: var(--outline-sub);
    --btn-text: var(--text);
  }
  
  button.accent {
    --btn-bg: var(--accent);
    --btn-text: var(--on-accent);
  }

	button:hover {
		transform: translateY(-4px);
		box-shadow: 0 8px 15px color-mix(in srgb, var(--shadow), transparent 80%);
		background-color: color-mix(in srgb, var(--btn-bg), black 10%);
	}

	button:active {
		transform: translateY(-1px);
		box-shadow: 0 2px 4px color-mix(in srgb, var(--shadow), transparent 85%);
	}
</style>
