<script lang="ts">
	import { Title } from '$lib';
	import FeatureCard from '$lib/features/government/components/FeatureCard.svelte';
</script>

<Title
	titleText="🚨 災害支援システム 行政ダッシュボード"
	subtitleText="避難所からの支援要請への迅速な対応を支援します。"
/>
<div class="card-grid">
	<FeatureCard
		href="/government/requestlist"
		titleText="📋 支援要請一覧"
		descriptionText="未対応の要請や対応状況を確認し、優先順位をつけて対応を開始します。"
		linkText="→ 詳細を見る"
	/>
	<FeatureCard
		href="/government/map"
		titleText="📍 避難所マップ"
		descriptionText="すべてのコミュニティの現在位置（避難所）と周辺情報を地図上で確認します。"
		linkText="→ マップを見る"
	/>
</div>

<style>
	.card-grid {
		padding: 20px;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 40px;
	}
</style>
