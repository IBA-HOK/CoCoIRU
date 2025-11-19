<script>
	import { goto } from '$app/navigation';
	import { Button } from '$lib';

	function requestButtonClick() {
		goto('/community/request');
	}
	function nearbyButtonClick() {
		goto('/community/nearby');
	}
</script>

<div style="text-align: center;">
	<Button text="支援物資申請" on:click={requestButtonClick} />
	<Button text="周辺コミュニティ" on:click={nearbyButtonClick} />
</div>
