<script lang="ts">
	import { onMount } from 'svelte';

	// APIのベースURL（環境に応じて変更してください）
	const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

	// 入力されたコミュニティID
	let communityId = '';
	
	// 取得したコミュニティ情報
	let communityData: any = null;
	
	// ローディング状態
	let loading = false;
	
	// エラーメッセージ
	let errorMessage = '';

	// コミュニティ情報を取得する関数
	async function fetchCommunityInfo() {
		if (!communityId || String(communityId).trim() === '') {
			errorMessage = 'コミュニティIDを入力してください';
			return;
		}

		loading = true;
		errorMessage = '';
		communityData = null;

		try {
			const response = await fetch(`${API_BASE_URL}/communities/${communityId}`);
			
			if (!response.ok) {
				if (response.status === 404) {
					errorMessage = 'コミュニティが見つかりませんでした';
				} else {
					errorMessage = `エラーが発生しました (ステータス: ${response.status})`;
				}
				return;
			}

			communityData = await response.json();
		} catch (error) {
			errorMessage = `通信エラー: ${error}`;
			console.error('Error fetching community:', error);
		} finally {
			loading = false;
		}
	}

	// すべてのコミュニティを取得する関数（デモ用）
	let allCommunities: any[] = [];
	let showAllCommunities = false;

	async function fetchAllCommunities() {
		loading = true;
		errorMessage = '';
		allCommunities = [];

		try {
			const response = await fetch(`${API_BASE_URL}/communities/`);
			
			if (!response.ok) {
				errorMessage = `エラーが発生しました (ステータス: ${response.status})`;
				return;
			}

			allCommunities = await response.json();
			showAllCommunities = true;
		} catch (error) {
			errorMessage = `通信エラー: ${error}`;
			console.error('Error fetching all communities:', error);
		} finally {
			loading = false;
		}
	}
</script>

<div class="container">
	<h1>コミュニティ情報取得デモ</h1>
	
	<div class="search-section">
		<h2>コミュニティIDで検索</h2>
		<div class="input-group">
			<input 
				type="number" 
				bind:value={communityId} 
				placeholder="コミュニティIDを入力"
				on:keydown={(e) => e.key === 'Enter' && fetchCommunityInfo()}
			/>
			<button on:click={fetchCommunityInfo} disabled={loading}>
				{loading ? '取得中...' : '検索'}
			</button>
		</div>
	</div>

	<div class="all-communities-section">
		<button on:click={fetchAllCommunities} disabled={loading}>
			すべてのコミュニティを取得
		</button>
	</div>

	{#if errorMessage}
		<div class="error-message">
			⚠️ {errorMessage}
		</div>
	{/if}

	{#if loading}
		<div class="loading">読み込み中...</div>
	{/if}

	{#if communityData}
		<div class="result-section">
			<h2>コミュニティ情報</h2>
			<div class="community-card">
				<div class="info-row">
					<span class="label">コミュニティID:</span>
					<span class="value">{communityData.community_id}</span>
				</div>
				<div class="info-row">
					<span class="label">名前:</span>
					<span class="value">{communityData.name || '未設定'}</span>
				</div>
				<div class="info-row">
					<span class="label">メンバーID:</span>
					<span class="value">{communityData.member_id || '未設定'}</span>
				</div>
				<div class="info-row">
					<span class="label">メンバー数:</span>
					<span class="value">{communityData.member_count || '0'}</span>
				</div>
				<div class="info-row">
					<span class="label">緯度:</span>
					<span class="value">{communityData.latitude || '未設定'}</span>
				</div>
				<div class="info-row">
					<span class="label">経度:</span>
					<span class="value">{communityData.longitude || '未設定'}</span>
				</div>
				<div class="info-row">
					<span class="label">作成日時:</span>
					<span class="value">{communityData.created_at || '未設定'}</span>
				</div>
			</div>
		</div>
	{/if}

	{#if showAllCommunities && allCommunities.length > 0}
		<div class="result-section">
			<h2>すべてのコミュニティ ({allCommunities.length}件)</h2>
			<div class="communities-list">
				{#each allCommunities as community}
					<div class="community-card">
						<div class="info-row">
							<span class="label">ID:</span>
							<span class="value">{community.community_id}</span>
						</div>
						<div class="info-row">
							<span class="label">名前:</span>
							<span class="value">{community.name || '未設定'}</span>
						</div>
						<div class="info-row">
							<span class="label">メンバー数:</span>
							<span class="value">{community.member_count || '0'}</span>
						</div>
						<div class="info-row">
							<span class="label">位置:</span>
							<span class="value">
								{community.latitude && community.longitude 
									? `(${community.latitude}, ${community.longitude})`
									: '未設定'}
							</span>
						</div>
					</div>
				{/each}
			</div>
		</div>
	{:else if showAllCommunities}
		<div class="no-data">コミュニティが見つかりませんでした</div>
	{/if}
</div>

<style>
	.container {
		max-width: 800px;
		margin: 0 auto;
		padding: 2rem;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
	}

	h1 {
		color: #2c3e50;
		margin-bottom: 2rem;
		text-align: center;
	}

	h2 {
		color: #34495e;
		margin-bottom: 1rem;
		font-size: 1.3rem;
	}

	.search-section, .all-communities-section {
		margin-bottom: 2rem;
	}

	.input-group {
		display: flex;
		gap: 0.5rem;
	}

	input[type="number"] {
		flex: 1;
		padding: 0.75rem;
		font-size: 1rem;
		border: 2px solid #ddd;
		border-radius: 4px;
		transition: border-color 0.3s;
	}

	input[type="number"]:focus {
		outline: none;
		border-color: #3498db;
	}

	button {
		padding: 0.75rem 1.5rem;
		font-size: 1rem;
		background-color: #3498db;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	button:hover:not(:disabled) {
		background-color: #2980b9;
	}

	button:disabled {
		background-color: #95a5a6;
		cursor: not-allowed;
	}

	.error-message {
		padding: 1rem;
		background-color: #fee;
		color: #c33;
		border-left: 4px solid #c33;
		margin-bottom: 1rem;
		border-radius: 4px;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: #7f8c8d;
		font-size: 1.1rem;
	}

	.result-section {
		margin-top: 2rem;
	}

	.community-card {
		background-color: #f8f9fa;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		padding: 1.5rem;
		margin-bottom: 1rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	}

	.info-row {
		display: flex;
		padding: 0.5rem 0;
		border-bottom: 1px solid #e0e0e0;
	}

	.info-row:last-child {
		border-bottom: none;
	}

	.label {
		font-weight: 600;
		color: #555;
		width: 150px;
		flex-shrink: 0;
	}

	.value {
		color: #333;
		flex: 1;
	}

	.communities-list {
		max-height: 600px;
		overflow-y: auto;
	}

	.no-data {
		text-align: center;
		padding: 2rem;
		color: #7f8c8d;
		font-style: italic;
	}

	@media (max-width: 600px) {
		.container {
			padding: 1rem;
		}

		.info-row {
			flex-direction: column;
		}

		.label {
			width: 100%;
			margin-bottom: 0.25rem;
		}
	}
</style>