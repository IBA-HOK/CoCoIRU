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

<div class="container">
	<div class="image-wrapper">
		<img src="/src/lib/assets/CoCoIRU_emblem.png" alt="完了画像" class="title-image" />
	</div>
	<div class="btn-erea">
		<Button text="コミュニティ画面" on:click={communityButtonClick} />
		<Button text="行政画面" on:click={governmentButtonClick} />
	</div>
</div>

<style>
	.container {
		max-width: 600px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		justify-content: center;
		padding: 2rem 0;
	}

	.image-wrapper {
		display: flex;
		justify-content: center;
		margin-bottom: 5rem;
		padding: 0 20px;
	}

	.title-image {
		max-width: 100%;
		height: auto;
	}
	
	.btn-erea {
		display: flex;
		gap: 1rem;
		justify-content: center;
		flex-wrap: wrap;
	}
</style>
