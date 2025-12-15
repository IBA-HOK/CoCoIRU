<script lang="ts">
	import { goto } from '$app/navigation';
	import { Title, Button } from '$lib';

	function OnLoginButtonClick() {
		goto('/community/community_Login/login');
	}
	function OnCreateButtonClick() {
		goto('/community/community_Login/form');
	}
</script>

<Title
	titleText="CoCoIRU コミュニティ"
	subtitleText="コミュニティを作成し、支援物資の申請を行うことができます。"
/>

<div class="btn-container">
	<div class="btn-area">
		<Button text="コミュニティにログイン" variant="primary" on:click={OnLoginButtonClick} />
	</div>
	<div class="btn-area">
		<Button text="コミュニティを新規作成" variant="secondary" on:click={OnCreateButtonClick} />
	</div>
</div>

<style>
	.btn-container {
		display: flex;
    flex-direction: column;
		justify-content: center;
		align-items: center;
    gap: 1rem;
	}
	.btn-area {
		flex: 1;
		max-width: 400px;
	}
</style>
