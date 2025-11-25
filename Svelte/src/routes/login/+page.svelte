<script lang="ts">
  import { onMount } from 'svelte';

  type Mode = 'create' | 'join';

  let mode: Mode = 'create';
  let step: 'form' | 'confirm' | 'done' = 'form';

  // form fields
  let name = '';
  let age: number | null = null;
  let communityId = '';

  // location (for create)
  let locationText = '';
  let locationError = '';

  // generated ids
  let generatedCommunityId = '';

  let infoMessage = '';

  function toConfirm() {
    infoMessage = '';
    if (!name.trim()) { infoMessage = '名前を入力してください'; return; }
    if (!age) { infoMessage = '年齢を入力してください'; return; }
    if (mode === 'join' && !communityId.trim()) { infoMessage = '参加希望のコミュニティIDを入力してください'; return; }
    if (mode === 'create' && !locationText) { infoMessage = '位置情報を取得してください（位置情報がない場合は手入力可）'; }
    step = 'confirm';
  }

  function backToForm() {
    infoMessage = '';
    step = 'form';
  }

  function generateIds() {
    if (mode === 'create') {
      generatedCommunityId = generateShortId();
    } else {
      generatedCommunityId = communityId;
    }
  }

  function confirmFinish() {
    generateIds();
    step = 'done';
  }

  function generateShortId() {
    return 'comm-' + Math.random().toString(36).slice(2, 8);
  }

  async function copyToClipboard(text: string) {
    try {
      await navigator.clipboard.writeText(text);
      alert('コピーしました: ' + text);
    } catch (e) {
      alert('クリップボードにコピーできませんでした。手動で控えてください: ' + text);
    }
  }

  function getLocation() {
    locationError = '';
    if (!navigator.geolocation) {
      locationError = 'このブラウザは位置情報をサポートしていません';
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude, longitude } = pos.coords;
        locationText = `lat:${latitude.toFixed(6)}, lon:${longitude.toFixed(6)}`;
      },
      (err) => {
        locationError = '位置情報の取得に失敗しました: ' + err.message;
      },
      { enableHighAccuracy: false, timeout: 10000 }
    );
  }

  // reset on mount
  onMount(() => {
    name = '';
    age = null;
    // try to prefill communityId from sessionStorage if navigated from community page
    const pref = typeof sessionStorage !== 'undefined' ? sessionStorage.getItem('selectedCommunityId') : null;
    const prefMode = typeof sessionStorage !== 'undefined' ? sessionStorage.getItem('selectedMode') : null;
    if (prefMode === 'create' || prefMode === 'join') {
      mode = (prefMode as Mode);
      try { sessionStorage.removeItem('selectedMode'); } catch (e) {}
    }
    if (pref) {
      communityId = pref;
      try { sessionStorage.removeItem('selectedCommunityId'); } catch (e) {}
    } else {
      communityId = '';
    }
    locationText = '';
    locationError = '';
    generatedCommunityId = '';
    infoMessage = '';
    step = 'form';
  });
</script>

<main class="page">
  <section class="card">
    <h2>コミュニティ作成 / 参加</h2>

    {#if step === 'form'}
      <div class="modes">
        <label class="mode">
          <input type="radio" bind:group={mode} value="create" />
          コミュニティ作成
        </label>
        <label class="mode">
          <input type="radio" bind:group={mode} value="join" />
          コミュニティ参加
        </label>
      </div>

      <div class="form">
        <label>名前
          <input type="text" bind:value={name} placeholder="例: 山田 太郎" />
        </label>

        <label>年齢
          <input type="number" bind:value={age} min="0" placeholder="年齢" />
        </label>

        {#if mode === 'create'}
          <label>位置情報（作成時に取得）
            <div class="location-row">
              <input type="text" bind:value={locationText} placeholder="取得していない場合は手入力可" />
              <button type="button" on:click={getLocation}>現在地を取得</button>
            </div>
            {#if locationError}
              <div class="error">{locationError}</div>
            {/if}
          </label>
        {:else}
          <label>参加希望コミュニティID
            <input type="text" bind:value={communityId} placeholder="例: comm-abc123" />
          </label>
        {/if}

        {#if infoMessage}
          <div class="info">{infoMessage}</div>
        {/if}

        <div class="actions">
          <button class="btn primary" type="button" on:click={toConfirm}>次へ（確認）</button>
        </div>
      </div>

    {:else if step === 'confirm'}
      <div class="confirm">
        <h3>入力内容の確認</h3>
        <dl>
          <dt>モード</dt>
          <dd>{mode === 'create' ? 'コミュニティ作成' : 'コミュニティ参加'}</dd>

          <dt>名前</dt>
          <dd>{name}</dd>

          <dt>年齢</dt>
          <dd>{age}</dd>

          {#if mode === 'create'}
            <dt>位置情報</dt>
            <dd>{locationText || '（未入力）'}</dd>
          {:else}
            <dt>参加希望コミュニティID</dt>
            <dd>{communityId}</dd>
          {/if}
        </dl>

        <div class="actions">
          <button class="btn" type="button" on:click={backToForm}>戻る</button>
          <button class="btn primary" type="button" on:click={confirmFinish}>完了（IDを生成）</button>
        </div>
      </div>

    {:else}
      <div class="done">
        <h3>完了 — コミュニティID を控えてください</h3>

        <p>コミュニティID:</p>
        <div class="id-row">
          <code>{generatedCommunityId}</code>
          <button class="btn" on:click={() => copyToClipboard(generatedCommunityId)}>コピー</button>
        </div>

        <p class="memo">忘れないようにメモを取ることをおすすめします。</p>

        <div class="actions">
          <button class="btn" on:click={() => { step = 'form'; }}>新しく作る/参加する</button>
        </div>
      </div>
    {/if}
  </section>
</main>

<style>
  .page { padding: 1rem; display: flex; justify-content: center; }
  .card { width: 100%; max-width: 720px; background: #fff; border-radius: 8px; padding: 1.25rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
  h2 { margin: 0 0 1rem 0; }
  .modes { display:flex; gap:1rem; margin-bottom: 1rem }
  .mode { display:flex; align-items:center; gap:0.5rem }
  label { display:block; margin-bottom:0.75rem }
  input[type="text"], input[type="number"] { width:100%; padding:0.5rem; border:1px solid #ddd; border-radius:4px }
  .location-row { display:flex; gap:0.5rem }
  .location-row input { flex:1 }
  .error { color:#c00; font-size:0.9rem; margin-top:0.25rem }
  .info { color:#b55000; margin:0.5rem 0 }
  .actions { display:flex; gap:0.75rem; margin-top:1rem }
  .btn { padding:0.5rem 0.75rem; border-radius:6px; border:1px solid #ccc; background:#f5f5f5; cursor:pointer }
  .btn.primary { background:#2ecc71; border-color: #27b85a; color:white }
  .confirm dl { display:grid; grid-template-columns: 140px 1fr; gap:0.5rem 1rem }
  .id-row { display:flex; gap:0.5rem; align-items:center }
  code { background:#f3f4f6; padding:0.35rem 0.5rem; border-radius:4px }
  .memo { margin-top:1rem; color:#444 }
  @media (max-width:480px) {
    .card { padding: 1rem }
    .confirm dl { grid-template-columns: 1fr }
  }
</style>
