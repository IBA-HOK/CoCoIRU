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
	titleText="コミュニティを検知できませんでした。"
	subtitleText="新規コミュニティ作成もしくはログイン処理を行ってください。"
/>