<script>
	import { goto } from '$app/navigation';
	import { Button } from '$lib';

	function communityButtonClick() {
		goto('/community');
	}
	function governmentButtonClick() {
		goto('/government');
	}
</script>

<div style="text-align: center;">
	<Button text="コミュニティ画面" on:click={communityButtonClick} />
	<Button text="行政画面" on:click={governmentButtonClick} />
</div>
