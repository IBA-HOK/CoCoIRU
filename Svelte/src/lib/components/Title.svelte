<script lang="ts">
	/**
	 * @component Title
	 * @description
	 * 各画面のタイトル・サブタイトルコンポーネント
	 */

	export let titleText = '';
	export let subtitleText = '';
</script>

<div class="container">
	<h1 class="title">{titleText}</h1>
	{#if subtitleText != ''}
		<p class="subtitle">{subtitleText}</p>
	{/if}
</div>

<style>
	.container {
		margin: 20px 20px 40px 20px;
	}
	.title {
		color: var(--primary);
		border-bottom: 2px solid var(--primary);
		padding-bottom: 10px;
		padding-left: 20px;
	}
	.subtitle {
		padding-left: 40px;
		font-size: 1.1em;
		color: var(--text);
	}
</style>
