<script lang="ts">
	import favicon from '$lib/assets/CoCoIRU_icon.png';
	import '$lib/theme.css';
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="page-wrapper">
	<slot />
</div>

<style>
	.page-wrapper {
		min-height: 100vh;
		font-size: 1.0em;
		background-color: var(--bg);
		color: var(--text);
	}
</style>
