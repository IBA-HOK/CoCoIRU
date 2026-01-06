<script lang="ts">
	/**
	 * @component Title
	 * @description
	 * 各画面のタイトル・サブタイトルコンポーネント
	 */

	export let titleText = '';
	export let subtitleText = '';
	export let iconSrc = '';
	export let iconAlt = 'タイトルアイコン';
</script>

<div class="container">
	<div class="title-wrapper">
		{#if iconSrc}
			<img src={iconSrc} alt={iconAlt} class="title-icon" />
		{/if}
		<h1 class="title">{titleText}</h1>
	</div>
	{#if subtitleText != ''}
		<p class="subtitle">{subtitleText}</p>
	{/if}
</div>

<style>
	.container {
		margin: 20px 20px 20px 20px;
	}

	.title-wrapper {
		display: flex;
		align-items: center;
		border-bottom: 2px solid var(--primary);
	}

	.title {
		color: var(--primary);
		padding-bottom: 10px;
		margin: 0;
	}

	.title-icon {
		width: 2em;
		height: 2em;
		flex-shrink: 0;
		margin-right: 0.5rem;
		margin-bottom: 0.5rem;
	}
	
	.subtitle {
		padding-left: 40px;
		font-size: 1.1em;
		color: var(--text);
	}
</style>
