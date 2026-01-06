<script lang="ts">
  import { onMount } from 'svelte';
  import { Title, Surface, Button } from '$lib';

  type ItemAddReq = {
    add_req_id: number;
    community_id: number;
    item_name: string;
    item_unit: string | null;
    reason: string | null;
    timestamp: string;
  };

  let list: ItemAddReq[] = [];
  let loading = false;
  let error = '';
  let message = '';

  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  function getToken(): string | null {
    const raw =
      localStorage.getItem('access_token') ||
      localStorage.getItem('token') ||
      sessionStorage.getItem('access_token');

    // Bearer が付いていてもOKにする
    return raw ? raw.replace(/^Bearer\s+/i, '').trim() : null;
  }

  async function load() {
    loading = true;
    error = '';
    message = '';
    try {
      const token = getToken();
      if (!token) throw new Error('ログインが必要です（トークンがありません）');

      const res = await fetch(`${API_BASE}/api/v1/item_addition_requests/?skip=0&limit=100`, {
        headers: { Authorization: `Bearer ${token}` },
        credentials: 'include'
      });
      if (!res.ok) throw new Error(await res.text());

      list = await res.json();
    } catch (e: any) {
      error = e?.message ?? String(e);
    } finally {
      loading = false;
    }
  }

  onMount(load);

  // ✅ 受諾：PUT（DBに status が無い想定なので reason に承認タグを追記）
  async function approve(r: ItemAddReq) {
    error = '';
    message = '';
    try {
      const token = getToken();
      if (!token) throw new Error('トークンがありません');

      const approvedTag = '【承認済み】';
      const current = (r.reason ?? '').trim();
      const updatedReason = current.includes(approvedTag)
        ? current
        : (current ? `${current}\n${approvedTag}` : approvedTag);

      const payload = {
        community_id: r.community_id,
        item_name: r.item_name,
        item_unit: r.item_unit,
        reason: updatedReason,
        timestamp: r.timestamp // 422対策（必須扱いされる場合がある）
      };

      const res = await fetch(`${API_BASE}/api/v1/item_addition_requests/${r.add_req_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(await res.text());

      message = `申請ID ${r.add_req_id} を受諾しました`;
      await load();
    } catch (e: any) {
      error = e?.message ?? String(e);
    }
  }

  // ✅ 拒否：DELETE（レコード削除）
  async function reject(r: ItemAddReq) {
    error = '';
    message = '';
    try {
      const token = getToken();
      if (!token) throw new Error('トークンがありません');

      // 誤操作防止（不要なら消してOK）
      const ok = confirm(`申請ID ${r.add_req_id} を拒否（削除）しますか？\n※元に戻せません`);
      if (!ok) return;

      const res = await fetch(`${API_BASE}/api/v1/item_addition_requests/${r.add_req_id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
        credentials: 'include'
      });

      if (!res.ok) throw new Error(await res.text());

      message = `申請ID ${r.add_req_id} を拒否しました（削除）`;
      await load();
    } catch (e: any) {
      error = e?.message ?? String(e);
    }
  }
</script>

<Title
  titleText="申請物品項目 受諾 / 拒否（行政）"
  subtitleText="受諾：reasonに【承認済み】を追記して更新 / 拒否：削除"
/>

{#if loading}
  <p>読み込み中...</p>
{:else}
  {#if error}
    <p style="color:red">{error}</p>
  {/if}
  {#if message}
    <p style="color:green">{message}</p>
  {/if}

  <div class="list">
    {#each list as r (r.add_req_id)}
      <Surface>
        <div class="card">
          <div class="header">
            <strong>申請ID：{r.add_req_id}</strong>
            <span class="status">community_id：{r.community_id}</span>
          </div>

          <div class="section">
            <strong>申請品目</strong>
            <ul>
              <li>{r.item_name} {r.item_unit ? `（${r.item_unit}）` : ''}</li>
            </ul>
          </div>

          <div class="section">
            <strong>理由</strong>
            <div class="note-box">{r.reason ?? '（未入力）'}</div>
          </div>

          <div class="section">
            <strong>送信時刻</strong>
            <div class="note-box">{r.timestamp}</div>
          </div>

          <div class="actions">
            <Button text="受諾" variant="accent" on:click={() => approve(r)} />
            <Button text="拒否" variant="secondary" on:click={() => reject(r)} />
          </div>
        </div>
      </Surface>
    {/each}
  </div>
{/if}

<style>
  .list { display:flex; flex-direction:column; gap:16px; }
  .card { display:flex; flex-direction:column; gap:12px; }
  .header { display:flex; justify-content:space-between; font-size:0.95rem; }
  .status { color: var(--text-sub); }
  .section ul { margin: 6px 0 0 16px; }
  .note-box { padding:10px; border-radius:8px; border:1px solid var(--outline); background: var(--bg); }
  .actions { display:flex; gap:8px; }
</style>
