<script lang="ts">
  import { Title, Surface, Button } from '$lib';
  import { mockRequests } from '$lib/features/request/requestStore';

  function approve(id: number) {
    mockRequests.update(list =>
      list.map(r => r.id === id ? { ...r, status: 'approved' } : r)
    );
  }

  function reject(id: number) {
    mockRequests.update(list =>
      list.map(r => r.id === id ? { ...r, status: 'rejected' } : r)
    );
  }
</script>

<Title
  titleText="申請物品項目 受諾 / 拒否（行政）"
  subtitleText="申請内容と特記事項を確認してください"
/>

<div class="list">
  {#each $mockRequests as r (r.id)}
    <Surface>
      <div class="card">

        <!-- ヘッダー -->
        <div class="header">
          <strong>申請ID：{r.id}</strong>
          <span class="status">状態：{r.status}</span>
        </div>

        <!-- 申請品目 -->
        <div class="section">
          <strong>申請品目</strong>
          <ul>
            {#each r.items as item}
              <li>{item}</li>
            {/each}
          </ul>
        </div>

        <!-- 特記事項 -->
        <div class="section">
          <strong>特記事項</strong>
          <div class="note-box">
            {r.note || '（未入力）'}
          </div>
        </div>

        <!-- 操作 -->
        {#if r.status === 'pending'}
          <div class="actions">
            <Button
              text="受諾"
              variant="accent"
              on:click={() => approve(r.id)}
            />
            <Button
              text="拒否"
              variant="secondary"
              on:click={() => reject(r.id)}
            />
          </div>
        {:else}
          <div class="done">処理済み</div>
        {/if}

      </div>
    </Surface>
  {/each}
</div>

<style>
  .list {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .card {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .header {
    display: flex;
    justify-content: space-between;
    font-size: 0.95rem;
  }

  .status {
    color: var(--text-sub);
  }

  .section ul {
    margin: 6px 0 0 16px;
  }

  .note-box {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid var(--outline);
    background: var(--bg);
  }

  .actions {
    display: flex;
    gap: 8px;
  }

  .done {
    color: var(--text-sub);
    font-size: 0.9rem;
  }
</style>
