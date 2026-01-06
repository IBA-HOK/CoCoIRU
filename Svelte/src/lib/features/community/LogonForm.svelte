<script lang="ts">
  import { goto } from '$app/navigation';
  import { createEventDispatcher, onMount } from 'svelte';
  import { Button } from '$lib';

  // Reuse the create form UI (UI-only). Use a single 'count' for total members.
  let name = '';
  let count: number = 0;
  let password = '';
  const dispatch = createEventDispatcher();

  onMount(() => {
    try {
      const saved = sessionStorage.getItem('newCommunityDraft');
      if (saved) {
        const d = JSON.parse(saved);
        if (d.name) name = d.name;
        if (d.count) count = d.count;
        if (d.password) password = d.password;
      }
    } catch (e) {}
  });

  function toConfirm() {
    const draft = { name, count, password };
    try {
      sessionStorage.setItem('newCommunityDraft', JSON.stringify(draft));
    } catch (e) { console.error(e); }
    dispatch('confirm');
  }
  function back() {
    dispatch('back');
  }
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
	<div class="force-black-text">
		<section class="card" style="max-width:720px; width:100%">
			<h2>コミュニティ作成フォーム</h2>

			<label
				>コミュニティ名
				<input type="text" bind:value={name} placeholder="コミュニティ名を入力" />
			</label>

			<label
				>人数
				<input type="number" bind:value={count} min="0" />
			</label>

			<label
				>コミュニティパスワード
				<input type="password" bind:value={password} placeholder="任意のパスワード" />
			</label>

			<div class="actions">
				<Button text="戻る" variant="secondary" size="small" on:click={() => dispatch('back')} />
				<Button text="確認へ" variant="primary" on:click={toConfirm} size="small" />
			</div>
		</section>
	</div>
</main>

<style>
	.card {
		background: var(--card);
    color: var(--text);
		padding: 1.25rem;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
	}
	label {
		display: block;
		margin-bottom: 0.75rem;
	}
	input {
		width: 100%;
		padding: 0.5rem;
		border: 1px solid #ddd;
		border-radius: 4px;
	}
	.actions {
		display: flex;
		gap: 0.75rem;
		margin-top: 1rem;
	}
</style>
