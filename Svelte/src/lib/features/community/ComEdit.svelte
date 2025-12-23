<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { Button } from '$lib';

	const dispatch = createEventDispatcher();
	const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

	// 状態管理: 'input' (入力) -> 'confirm' (確認) -> 'complete' (完了)
	let step: 'input' | 'confirm' | 'complete' = 'input';

	let communityId = '';
	let name = '';
	let count = 1;
	let password = '';

	let error = '';
	let isSubmitting = false;

	// 初期化：現在のコミュニティ情報をロード
	onMount(() => {
		try {
			const pref = sessionStorage.getItem('selectedCommunityId');
			if (pref) communityId = pref;

			// 1. キャッシュされた編集情報を取得 (表示用)
			const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
			const edits = JSON.parse(editsRaw);
			const e = edits[communityId] || null;
			if (e?.name) name = e.name;
			if (typeof e?.count === 'number') count = e.count;

			// 2. 編集中の一時保存があれば復元 (入力途中だった場合)
			const saved = sessionStorage.getItem('editDraft');
			if (saved) {
				const d = JSON.parse(saved);
				// 同じコミュニティIDの場合のみ復元
				if (d.communityId === communityId) {
					if (d.name) name = d.name;
					if (typeof d.count === 'number') count = d.count;
					if (d.password) password = d.password;
				}
			}
		} catch (e) {}
	});

	// 人数変更ハンドラ
	function inc() {
		count = Math.min(9999, count + 1);
	}
	function dec() {
		count = Math.max(0, count - 1);
	}

	// --- STEP 1: 入力画面の処理 ---

	function toConfirm() {
		error = '';
		if (!name.trim()) {
			error = 'コミュニティ名を入力してください';
			return;
		}
		// 入力内容を一時保存
		try {
			sessionStorage.setItem('editDraft', JSON.stringify({ communityId, name, count, password }));
		} catch (e) {}

		step = 'confirm';
	}

	function handleBackToAccount() {
		// アカウント画面へ戻る
		dispatch('back');
	}

	// --- STEP 2: 確認画面の処理 ---

	function backToInput() {
		step = 'input';
	}

	async function submitEdit() {
		error = '';
		if (!communityId) {
			error = 'コミュニティIDが不明です';
			return;
		}

		isSubmitting = true;
		try {
			const body = {
				name: name || '',
				password: password || '',
				member_count: count
			};

			const res = await fetch(`${API_BASE}/api/v1/communities/${communityId}`, {
				method: 'PUT',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify(body)
			});

			if (!res.ok) {
				const d = await res.json().catch(() => ({}));
				throw new Error(d.detail || `更新に失敗しました (${res.status})`);
			}

			const data = await res.json();

			// 成功時: キャッシュを更新し、ドラフトを削除
			try {
				const editsRaw = sessionStorage.getItem('communityEdits') || '{}';
				const edits = JSON.parse(editsRaw);
				edits[communityId] = { name: data.name, count: data.member_count };
				sessionStorage.setItem('communityEdits', JSON.stringify(edits));

				sessionStorage.setItem('lastEditedCommunity', communityId);
				sessionStorage.removeItem('editDraft');
			} catch (e) {}

			// 完了画面へ
			step = 'complete';
		} catch (e) {
			console.error(e);
			error = e instanceof Error ? e.message : '更新エラー';
		} finally {
			isSubmitting = false;
		}
	}

	// --- STEP 3: 完了画面の処理 ---

	function finish() {
		// 親コンポーネントに完了(戻る)を通知
		dispatch('back');
	}
</script>

<main class="page" style="padding:1rem; display:flex; justify-content:center">
	{#if step === 'input'}
		<div class="force-black-text">
			<section class="card" style="max-width:720px; width:100%">
				<h2>コミュニティ情報の編集</h2>

				<label
					>コミュニティID (変更不可)
					<input type="text" value={communityId} disabled style="background:#f0f0f0; color:#666" />
				</label>

				<label
					>コミュニティ名
					<input type="text" bind:value={name} placeholder="コミュニティ名" />
				</label>

				<label
					>人数
					<div style="display:flex; gap:0.5rem">
						<button class="small" type="button" on:click={dec}>－</button>
						<input type="number" bind:value={count} min="0" style="text-align:center" />
						<button class="small" type="button" on:click={inc}>＋</button>
					</div>
				</label>

				<label
					>パスワード (変更の確認用)
					<input type="password" bind:value={password} placeholder="パスワードを入力" />
				</label>

				{#if error}
					<div class="error">{error}</div>
				{/if}

				<div class="actions">
					<Button text="戻る" variant="secondary" on:click={handleBackToAccount} />
					{#if name.trim()}
						<Button text="確認へ" variant="primary" on:click={toConfirm} />
					{:else}
						<button class="btn-disabled" disabled>確認へ</button>
					{/if}
				</div>
			</section>
		</div>
	{:else if step === 'confirm'}
		<div class="force-black-text">
			<section class="card" style="max-width:720px; width:100%">
				<h2>変更内容の確認</h2>
				<p>以下の内容で更新します。</p>

				<div style="margin: 1rem 0; padding: 1rem; background: #f9f9f9; border-radius: 4px;">
					<p><strong>コミュニティID:</strong> {communityId}</p>
					<p><strong>コミュニティ名:</strong> {name}</p>
					<p><strong>人数:</strong> {count}</p>
				</div>

				{#if error}
					<div class="error" style="margin-bottom:1rem;">{error}</div>
				{/if}

				<div class="actions">
					{#if !isSubmitting}
						<Button
							text="修正する"
							variant="secondary"
							on:click={backToInput}
						/>
						<Button
							text="変更を確定する"
							variant="primary"
							on:click={submitEdit}
						/>
					{:else}
						<button class="btn-disabled" disabled>修正する</button>
						<button class="btn-disabled" disabled>更新中...</button>
					{/if}
				</div>
			</section>
		</div>
	{:else if step === 'complete'}
		<div class="force-black-text">
			<section class="card" style="max-width:720px; width:100%; text-align:center;">
				<h2>編集が完了しました</h2>
				<p>コミュニティ: <strong>{communityId}</strong> の情報を更新しました。</p>

				<div class="actions" style="justify-content:center; margin-top:1.5rem">
					<Button text="コミュニティ一覧に戻る" variant="primary" on:click={finish} />
				</div>
			</section>
		</div>
	{/if}
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
	.small {
		padding: 0.25rem 0.75rem;
		cursor: pointer;
	}
	.error {
		color: var(--error);
		margin-top: 0.5rem;
	}
	.force-black-text {
		color: #000;
	}
	.force-black-text strong {
		color: #000;
	}
	.btn-disabled {
		padding: 0.5rem 1rem;
		border-radius: 4px;
		background: #ccc;
		color: #666;
		border: none;
		cursor: not-allowed;
	}
</style>
