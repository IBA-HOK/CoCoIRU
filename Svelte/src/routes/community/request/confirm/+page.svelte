<script lang="ts">
  import { goto } from '$app/navigation';
  import { requestItems } from '$lib/features/request/requestItems';
  import { Button } from '$lib';
  import RequestItemList from '$lib/features/request/components/RequestItemList.svelte';
  import type { RequestItem } from '$lib/features/request/requestItems'; // ★追加：型
	import RequestNoteInput from '$lib/features/request/components/RequestNoteInput.svelte';
	import Surface from '$lib/components/Surface.svelte';
  import { communityId } from '$lib/stores/auth';

  import { requestNote } from '$lib/features/request/requestNoteStore'; // ★追加
  // 特記事項
  //let notes = '';

  // 現在のコミュニティID（数値、未確定なら null）
  let currentCommunityId: number | null = null;

  // ★追加：型を付ける
  let selectedItems: RequestItem[] = [];

  // value > 0 の物資のみ抽出
  $: selectedItems = $requestItems.filter(
    (item: RequestItem) => item.value > 0   // ★型を追加
  );

  // ★追加：API URL
  const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000';

  // ★ community_id を store から取得（数値でない場合は null として扱う）
  $: currentCommunityId = null;
  $: if (typeof $communityId !== 'undefined' && $communityId !== null) {
    const s = String($communityId);
    currentCommunityId = /^\d+$/.test(s) ? Number(s) : null;
  }

  // ---------------------------------------------------------
  // ★ 1つの物資を保存する処理（RequestContent → SupportRequest）
  // ---------------------------------------------------------
  async function createOneRequest(item: RequestItem) {
    // (1) RequestContent を保存
    const rcPayload = {
      items_id: item.id,
      number: item.value,
      //other_note: notes
      other_note: $requestNote   // ★store の値に置き換え
    };

    const rcRes = await fetch(`${API_BASE}/api/v1/request_content/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(rcPayload)
    });

    if (!rcRes.ok) {
      console.error(await rcRes.text());
      throw new Error('RequestContent 作成失敗');
    }

    const rcData = await rcRes.json();
    const request_content_id = rcData.request_content_id;

    // (2) SupportRequest を保存
    if (!currentCommunityId) {
      throw new Error('コミュニティIDが不正です。コミュニティにログインしてください。');
    }
    const srPayload = {
      community_id: currentCommunityId,
      request_content_id,
      status: 'pending'
    };

    const srRes = await fetch(`${API_BASE}/api/v1/support_requests/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
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

<div class="container">
	<Surface class="confirm-card">
		<div class="header-area">
			<h1 class="page-title">申請内容の確認</h1>
			<p class="page-subtitle">以下の内容で申請します。漏れがないかご確認ください。</p>
		</div>

		<section class="section-card flex-grow-card">
			<h2 class="section-title">申請品目</h2>
			<div class="list-wrapper">
				<RequestItemList items={selectedItems} />
			</div>
		</section>

		<section class="section-card">
			<RequestNoteInput />
		</section>

		<div class="request_footer">
			<div class="btn-area">
				<Button text="戻る" variant="secondary" on:click={backButtonClick} />
			</div>
			<div class="btn-area">
				<Button text="申請" variant="accent" on:click={orderButtonClick} />
			</div>
		</div>
	</Surface>
</div>

<style>
	.container {
		max-width: 600px;
		min-height: 600px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 24px;
		height: calc(100vh - 48px);
	}

	:global(.confirm-card) {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.header-area {
		text-align: center;
		margin-bottom: 0.5rem;
		flex-shrink: 0;
	}

	.page-title {
		margin: 0 0 0.5rem 0;
		color: var(--text);
		font-size: 1.5rem;
	}

	.page-subtitle {
		color: var(--text-sub);
		margin: 0;
		font-size: 0.9rem;
	}

	.flex-grow-card {
		flex: 1;
		min-height: 0;
		display: flex;
		flex-direction: column;
		padding-bottom: 0;
	}

	.section-title {
		margin: 0 0 16px 0;
		font-size: 1.1rem;
		color: var(--text);
		border-bottom: 1px solid var(--outline-sub);
		padding-bottom: 8px;
	}

	.list-wrapper {
		flex: 1;
		overflow-y: auto;
		padding-bottom: 24px;
	}

	.request_footer {
		display: flex;
		justify-content: center;
		gap: 24px;
		margin-top: 0;
		padding-bottom: 0;
		flex-shrink: 0;
	}

	.btn-area {
		flex: 1;
		max-width: 200px;
	}
</style>
