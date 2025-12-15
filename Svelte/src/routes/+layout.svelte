<script lang="ts">
	import favicon from '$lib/assets/CoCoIRU_icon.png';
	import '$lib/theme.css';
	import { Footer } from '$lib';
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="page-wrapper">
	<main class="main-content">
        <slot />
  </main>
	<Footer />
</div>

<style>
	.page-wrapper {
		min-height: 100vh;
		font-size: 1.0em;
		background-color: var(--bg);
		color: var(--text);
		display: flex;
        flex-direction: column;
	}
	.main-content {
        flex: 1;
        width: 100%;
    }
</style>