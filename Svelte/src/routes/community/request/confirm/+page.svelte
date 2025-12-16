//　念のため残す

<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  // request/+page.svelte に統合済みのため、このルートは互換用に /community/request へ戻す
  onMount(() => {
    try { sessionStorage.setItem('openRequestConfirmModal', '1'); } catch (e) {}
    goto('/community/request');
  });
</script>
