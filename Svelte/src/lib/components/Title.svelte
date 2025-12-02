<script lang="ts">
	/**
	 * @component Title
	 * @description
	 * 各画面のタイトル・サブタイトルコンポーネント
	 */

	export let titleText = '';
	export let subtitleText = '';
</script>

<h1 class="title">{titleText}</h1>

{#if subtitleText != ''}
	<p class="subtitle">{subtitleText}</p>
{/if}

<style>
	.title {
		color: var(--primary);
		border-bottom: 2px solid var(--primary);
		padding-bottom: 10px;
		margin-bottom: 10px;
	}
	.subtitle {
		font-size: 1.1em;
		color: var(--text);
		margin-bottom: 40px;
	}
</style>
