<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
<script>  // ボタンのスクリプト
	import { goto } from '$app/navigation';
  import Button from '$lib/Button.svelte';

  function requestButtonClick() {
    goto('/request');
  }
  function nearbyButtonClick() {
    goto('/nearby');
  }
  function governmentButtonClick() {
    goto('/government');
  }
</script>

<Button text="request" on:click={requestButtonClick} />
<Button text="nearby" on:click={nearbyButtonClick} />
<Button text="government" on:click={governmentButtonClick} />