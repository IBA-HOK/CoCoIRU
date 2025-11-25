<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  // draft input and viewed id are separated so editing the input won't change the shown info
  let communityId = '';
  let viewedCommunityId = '';
  let showInfo = false;
  let members: Array<{ name: string; age: number }> = [];

  function seededRandom(seed: number) {
    return function() {
      // mulberry32
      seed |= 0;
      seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function hashStringToInt(s: string) {
    let h = 2166136261 >>> 0;
    for (let i = 0; i < s.length; i++) {
      h = Math.imul(h ^ s.charCodeAt(i), 16777619) >>> 0;
    }
    return h >>> 0;
  }

  const family = ['佐藤','鈴木','高橋','田中','伊藤','山本','中村','小林','加藤','吉田'];
  const given = ['太郎','花子','次郎','美咲','健一','さくら','大輔','舞','拓也','陽菜'];

  function generateMockMembers(id: string) {
    if (!id) return [];
    const seed = hashStringToInt(id);
    const rand = seededRandom(seed);
    const count = 2 + Math.floor(rand() * 4); // 2-5 members
    const out = [];
    for (let i = 0; i < count; i++) {
      const fam = family[Math.floor(rand() * family.length)];
      const giv = given[Math.floor(rand() * given.length)];
      const age = 10 + Math.floor(rand() * 70);
      out.push({ name: `${fam} ${giv}`, age });
    }
    return out;
  }

  function showAccount() {
    // freeze the current input into the viewed id so further edits don't affect the shown info
    viewedCommunityId = communityId;
    showInfo = false;
    members = generateMockMembers(viewedCommunityId);
    showInfo = true;
  }

  function goToSelection(mode: 'create' | 'join') {
    // prefer the viewedCommunityId (the one user confirmed) when available
    const idToUse = viewedCommunityId || communityId;
    try {
      sessionStorage.setItem('selectedCommunityId', idToUse);
      sessionStorage.setItem('selectedMode', mode);
    } catch (e) {}
    goto('/login');
  }

  onMount(() => {
    // try prefill from sessionStorage if present
    try {
      const pref = sessionStorage.getItem('selectedCommunityId');
      if (pref) communityId = pref;
    } catch (e) {}
  });
</script>

<main class="page">
  <section class="card">
    <h2>コミュニティID を入力</h2>

    <div class="top-actions">
      <button class="btn" on:click={() => goto('http://localhost:5173/community/login')}>コミュニティ作成・参加へ</button>
    </div>

    <label>コミュニティID
      <input type="text" bind:value={communityId} placeholder="例: comm-abc123" />
    </label>

    <div class="actions">
      <button class="btn primary" on:click={showAccount} disabled={!communityId}>アカウント情報を表示</button>
    </div>

    {#if showInfo}
      <div class="info-block">
        <h3>コミュニティ情報</h3>
        <p><strong>コミュニティID:</strong> {viewedCommunityId}</p>

        <h4>メンバー</h4>
        {#if members.length === 0}
          <p>メンバーが見つかりません</p>
        {:else}
          <ul>
            {#each members as m}
              <li>{m.name} — {m.age}歳</li>
            {/each}
          </ul>
        {/if}

        <div class="actions">
          <button class="btn" on:click={() => { showInfo = false; }}>戻る</button>
          <button class="btn primary" on:click={() => goToSelection('join')}>このコミュニティに参加する</button>
          <button class="btn" on:click={() => goToSelection('create')}>新しく作る（作成画面へ）</button>
        </div>
      </div>
    {/if}
  </section>
</main>

<style>
  .page { padding: 1rem; display: flex; justify-content: center; }
  .card { width: 100%; max-width: 720px; background: #fff; border-radius: 8px; padding: 1.25rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  label { display:block; margin-bottom:0.75rem }
  input[type="text"] { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color: #27b85a; color:white }
  .info-block { margin-top:1rem; border-top:1px solid #eee; padding-top:1rem }
  ul { margin:0; padding-left:1rem }
</style>