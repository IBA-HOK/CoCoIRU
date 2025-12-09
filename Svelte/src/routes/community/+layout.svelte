<svelte:head>
  <meta name="robots" content="noindex" />
  <title>コミュニティ</title>
</svelte:head>
<script>
  import '$lib/theme.css';
  import { isLoggedIn } from '$lib/stores/auth';
  import Header from '$lib/features/community/HeaderCommunity.svelte';
</script>

<Header />
<slot />
