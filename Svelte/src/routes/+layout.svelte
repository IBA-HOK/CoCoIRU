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
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem 1rem;
    box-sizing: border-box;
  }
</style>