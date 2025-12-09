<script lang="ts">
	import Header from '$lib/features/government/components/HeaderGovernment.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { govLoggedIn } from '$lib/stores/auth';
	import { page } from '$app/stores';

	let isGovLoggedIn = false;

	const unsubscribe = govLoggedIn.subscribe((value) => {
		isGovLoggedIn = value;
	});

	onMount(() => {
		if ($page.url.pathname !== '/government/login' && !isGovLoggedIn) {
			goto('/government/login');
		}
	});
</script>

<Header />

<slot />

<style>
</style>
