<script lang="ts">
	import { Title } from '$lib';
	import FeatureCard from '$lib/features/government/components/FeatureCard.svelte';
	import alertIcon from '$lib/assets/alert.png';
	import supportIcon from '$lib/assets/support.png';
	import mapIcon from '$lib/assets/map.png';
</script>

<Title
    iconSrc={alertIcon}
	iconAlt="警告アイコン"
	titleText="災害支援システム 行政ダッシュボード"
	subtitleText="避難所からの支援要請への迅速な対応を支援します。"
/>
<div class="card-grid">
	<FeatureCard
		href="/government/requestlist"
		iconSrc={supportIcon}
		iconAlt="支援要請アイコン"
		titleText="支援要請一覧"
		descriptionText="未対応の要請や対応状況を確認し、優先順位をつけて対応を開始します。"
		linkText="→ 詳細を見る"
	/>
	<FeatureCard
		href="/government/map"
		iconSrc={mapIcon}
		iconAlt="地図アイコン"
		titleText="避難所マップ"
		descriptionText="すべてのコミュニティの現在位置（避難所）と周辺情報を地図上で確認します。"
		linkText="→ マップを見る"
	/>
	<FeatureCard
		href="/government/addItem"
		titleText="申請物品項目 受諾 / 拒否"
		descriptionText="申請物品として追加が求められている項目を確認します。"
		linkText="→ 詳細を見る"
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
