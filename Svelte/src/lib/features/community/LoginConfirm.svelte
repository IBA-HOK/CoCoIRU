<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/auth';
  import { Button } from '$lib';

	const dispatch = createEventDispatcher();

	let draft: {
		name?: string;
		adults?: number;
		children?: number;
		count?: number;
		password?: string;
	} = {};

	onMount(() => {
		try {
			const s = sessionStorage.getItem('newCommunityDraft');
			if (s) draft = JSON.parse(s);
		} catch (e) {}
	});

	function back() {
		dispatch('back');
	}
	const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

	async function create() {
		// Persist community to backend and use returned numeric community_id
		try {
			const total =
				typeof draft.count === 'number' ? draft.count : (draft.adults || 0) + (draft.children || 0);
			const payload = {
				name: draft.name || '',
				password: draft.password || '',
				member_count: total
			};

			const res = await fetch(`${API_BASE}/api/v1/communities/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			});

			if (!res.ok) {
				const d = await res.json().catch(() => ({}));
				throw new Error(d.detail || `作成に失敗しました (status=${res.status})`);
			}

			const data = await res.json();
			const numericId = data.community_id;
			if (!numericId) throw new Error('サーバーから有効なコミュニティIDが返されませんでした');

			// store numeric id as string for sessionStorage and auth store
			const idStr = String(numericId);
			sessionStorage.setItem('selectedCommunityId', idStr);

			// cache display data
			try {
				const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
				const edits = JSON.parse(editsRaw || '{}');
				edits[idStr] = { name: data.name || draft.name || '', count: data.member_count || total };
				sessionStorage.setItem('communityEdits', JSON.stringify(edits));
				sessionStorage.setItem('lastCreatedCommunity', idStr);
				sessionStorage.removeItem('newCommunityDraft');
			} catch (e) {}

			// update auth store so other pages react immediately
			try {
				login(sessionStorage.getItem('selectedCommunityId') || '');
			} catch (e) {}

			goto('/community/community_Login/account');
		} catch (e) {
			console.error(e);
			alert(e instanceof Error ? e.message : 'コミュニティ作成エラー');
		}
	}
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
	<div class="force-black-text">
		<section class="card" style="max-width:720px; width:100%">
			<h2>作成内容の確認</h2>
			<p><strong>コミュニティ名:</strong> {draft.name}</p>
			<p>
				<strong>合計人数:</strong>
				{typeof draft.count === 'number'
					? draft.count
					: (draft.adults || 0) + (draft.children || 0)}
			</p>

			<div class="actions">
				<Button text="戻る" variant="secondary" size="small" on:click={back} />
				<Button text="コミュニティ作成" variant="primary" size="small" on:click={create} />
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
	.actions {
		display: flex;
		gap: 0.75rem;
		margin-top: 1rem;
	}
	.btn {
		padding: 0.5rem 0.75rem;
		border-radius: 6px;
		border: 1px solid #ccc;
		background: #f5f5f5;
		cursor: pointer;
	}
	.btn.primary {
		background: #2ecc71;
		border-color: #27b85a;
		color: #fff;
	}
</style>
