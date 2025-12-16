<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let editedId = '';

  onMount(() => {
    try {
      const id = sessionStorage.getItem('lastEditedCommunity');
      if (id) editedId = id;
    } catch (e) {}
  });

  function toCommunity() { goto('/community/community_Login/account'); }
</script>

<main style="text-align:center; padding:1rem">
  <h1>編集が完了しました</h1>
  <p>コミュニティ: <strong>{editedId}</strong> の情報を更新しました。</p>
  <div style="margin-top:1rem">
    <button class="btn primary" on:click={toCommunity}>コミュニティ一覧に戻る</button>
  </div>
</main>
