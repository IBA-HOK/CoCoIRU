<script lang="ts">
  import { goto } from '$app/navigation';
  import { requestItems } from '$lib/features/request/requestItems';
  import { Button } from '$lib';
  import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
  import type { RequestItem } from '$lib/features/request/requestItems'; // ★追加：型

  // 特記事項
  let notes = '';

  // ★追加：型を付ける
  let selectedItems: RequestItem[] = [];

  // value > 0 の物資のみ抽出
  $: selectedItems = $requestItems.filter(
    (item: RequestItem) => item.value > 0   // ★型を追加
  );

  // ★追加：API URL
  const API_BASE = 'http://localhost:8000/api/v1';

  // ★追加：community_id（ログインしている住民IDなどに置き換え可）
  let communityId = 1;

  // ---------------------------------------------------------
  // ★ 1つの物資を保存する処理（RequestContent → SupportRequest）
  // ---------------------------------------------------------
  async function createOneRequest(item: RequestItem) {
    // (1) RequestContent を保存
    const rcPayload = {
      items_id: item.id,
      number: item.value,
      other_note: notes
    };

    const rcRes = await fetch(`${API_BASE}/request_content/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(rcPayload)
    });

    if (!rcRes.ok) {
      console.error(await rcRes.text());
      throw new Error('RequestContent 作成失敗');
    }

    const rcData = await rcRes.json();
    const request_content_id = rcData.request_content_id;

    // (2) SupportRequest を保存
    const srPayload = {
      community_id: communityId,
      request_content_id,
      status: 'pending'
    };

    const srRes = await fetch(`${API_BASE}/support_requests/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(srPayload)
    });

    if (!srRes.ok) {
      console.error(await srRes.text());
      throw new Error('SupportRequest 作成失敗');
    }

    return await srRes.json(); // request_id などを返す
  }

  // ---------------------------------------------------------
  // ★ 全物資をループして保存
  // ---------------------------------------------------------
  async function saveAllRequests() {
    const results = [];

    for (const item of selectedItems) {
      const result = await createOneRequest(item);
      results.push(result);
    }

    return results;
  }

  // ---------------------------------------------------------
  // ボタン処理
  // ---------------------------------------------------------
  function backButtonClick() {
    goto('/community/request');
  }

  async function orderButtonClick() {
    try {
      const results = await saveAllRequests();
      console.log('保存された申請:', results);

      goto('/community/request/complete');
    } catch (err) {
      console.error(err);
      alert('申請処理中にエラーが発生しました');
    }
  }
</script>

<h1 style="text-align: center;">申請漏れはございませんか？</h1>

<div class="content-container">
  <RequestItemList items={selectedItems} />
  <textarea 
    bind:value={notes} 
    placeholder="特記事項があればお書きください。"
    rows={5}
  ></textarea>
</div>

<div class="request_footer">
  <Button text="戻る" on:click={backButtonClick} />
  <Button text="注文する" on:click={orderButtonClick} />
</div>

<style>
  .content-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 0 1rem;
    max-height: 60vh;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 1rem;
  }

  textarea {
    width: 100%;
    font-size: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    border: 1px solid #ccc;
    resize: vertical;
    box-sizing: border-box;
  }

  .request_footer {
    padding-top: 50px;
    display: flex;
    justify-content: space-evenly;
  }
</style>
