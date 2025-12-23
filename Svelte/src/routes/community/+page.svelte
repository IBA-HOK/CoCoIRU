<script lang="ts">
	import { goto } from '$app/navigation';
	import { Title, Button } from '$lib';
	import LoginForm from '$lib/features/community/LoginForm.svelte';
	import LogonForm from '$lib/features/community/LogonForm.svelte';
	import LoginConfirm from '$lib/features/community/LoginConfirm.svelte';
	import LoginAccount from '$lib/features/community/LoginAccount.svelte';
  import ComDestroy from '$lib/features/community/ComDestroy.svelte';
  import ComEdit from '$lib/features/community/ComEdit.svelte';

	let state = "none";

	function OnLoginButtonClick() {
		state = "login";
	}
	function OnCreateButtonClick() {
		state = "create";
	}
	function OnAccountButtonClick() {
		state = "account";
	}
</script>

<Title
	titleText="CoCoIRU コミュニティ"
	subtitleText="コミュニティを作成し、支援物資の申請を行うことができます。"
/>

{#if state === "none"}
  <div class="btn-container">
    <div class="btn-area">
      <Button text="コミュニティにログイン" variant="primary" on:click={OnLoginButtonClick} />
    </div>
    <div class="btn-area">
      <Button text="コミュニティを新規作成" variant="secondary" on:click={OnCreateButtonClick} />
    </div>
  </div>
{:else if state === "login"}
  <LoginForm on:back={() => (state = 'none')}/>
{:else if state === "create"}
	<LogonForm 
    on:back={() => (state = 'none')} 
    on:confirm={() => (state = 'confirm')} 
  />
{:else if state === "confirm"}
  <LoginConfirm
    on:back={() => (state = 'none')}
    on:complete={() => (state = 'account')}
	/>
{:else if state === "account"}
  <LoginAccount 
    on:request={() => (state = 'request')}
    on:destroy={() => (state = 'destroy')}
    on:edit={() => (state = 'edit')}
  />
{:else if state === "destroy"}
  <ComDestroy
    on:back={() => (state = 'account')}
    on:complete={() => (state = 'none')}
  />
  {:else if state === "edit"}
    <ComEdit on:back={() => (state = 'account')} />
{/if}

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
