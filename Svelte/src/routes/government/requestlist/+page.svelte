<script lang="ts">
    // +page.server.ts からデータを受け取りますが、今回は中身は空です
    export let data;
    const requests = data.requests;

    // 表示切り替えのロジック
    let currentView: 'community' | 'item' = 'community';

  // ダミーデータ
    const allRequests = [
        { id: 1, community_id: 1, community_name: "A地区小学校避難所 (102号室)", item_name: "水 (2L)", number: 20, status: "pending", created_at: "2025-11-04 10:30:00" },
        { id: 2, community_id: 2, community_name: "B地区体育館コミュニティ", item_name: "毛布", number: 50, status: "pending", created_at: "2025-11-04 09:15:00" },
        { id: 3, community_id: 1, community_name: "A地区小学校避難所 (102号室)", item_name: "簡易トイレ", number: 5, status: "processing", created_at: "2025-11-04 08:00:00" },
        { id: 4, community_id: 3, community_name: "C町高齢者グループ", item_name: "簡易トイレ", number: 5, status: "processing", created_at: "2025-11-03 18:45:00" },
        { id: 5, community_id: 4, community_name: "D団地住民自主グループ", item_name: "おむつ (大人用)", number: 1, status: "completed", created_at: "2025-11-02 14:00:00" },
        { id: 6, community_id: 2, community_name: "B地区体育館コミュニティ", item_name: "水 (2L)", number: 30, status: "pending", created_at: "2025-11-04 11:00:00" },
    ];

    // コミュニティごとの表示に必要なダミーデータ加工
    const communityRequests = allRequests.reduce((acc, req) => {
        // 現在処理している要請 (req) のコミュニティ名が、すでに集計結果 (acc) の中に存在する場合
        let communityEntry = acc.find(c => c.name === req.community_name);
        // 現在処理している要請 (req) のコミュニティ名が、集計結果 (acc) の中に存在しない場合
        if (!communityEntry) {
            communityEntry = {
                name: req.community_name, 
                total_pending: 0, 
                latest_request_time: req.created_at,
                id: req.community_id
            };
            acc.push(communityEntry);
        }
        // 未対応の要請数のカウント
        if (req.status === 'pending') {
            communityEntry.total_pending += 1;
        }
        return acc;
    }, []);

    // 品目ごとの表示に必要なダミーデータ加工
    const itemRequests = allRequests.reduce((acc, req) => {
        let itemEntry = acc.find(i => i.item_name === req.item_name);
        if (!itemEntry) {
            itemEntry = {
                item_name: req.item_name,
                total_number: 0,
                pending_total_number: 0,
                last_requested_at: req.created_at,
            };
            acc.push(itemEntry);
        }
        itemEntry.total_number += req.number;
        
        if (req.status === 'pending') {
            itemEntry.pending_total_number += req.number;
        }
        return acc;
    }, []);
    
    $: displayData = currentView === 'community' ? communityRequests : itemRequests;
</script>

<div class="request-list-page">
    <h1>📋 支援要請一覧</h1>
    <p class="subtitle">未対応の要請や対応状況を、切り替えて確認できます。</p>

    <div class="view-switch-container">
        <button 
            class="switch-btn" 
            class:active={currentView === 'community'} 
            on:click={() => currentView = 'community'}
        >
            🏢 コミュニティ別リスト
        </button>
    
        <button 
            class="switch-btn" 
            class:active={currentView === 'item'} 
            on:click={() => currentView = 'item'}
        >
            📦 品目別集計
        </button>
    </div>
    
    <div class="list-container">
        {#if currentView === 'community'}
        <h2>🏢 コミュニティ別未対応要請 (全 {communityRequests.length} コミュニティ)</h2>
        <table>
            <thead>
                <tr>
                    <th>コミュニティ名</th>
                    <th>未対応要請数</th>
                    <th>最新の要請日時</th>
                </tr>
            </thead>
            <tbody>
                <!-- displayData 配列の中身を1件ずつ c としてループ処理 (Svelte構文) -->
                {#each displayData as c}
                <tr>
                    <td><a href={`/government/requestlist/community/${c.id}`} class="community-link">{c.name}</a></td>
                    <td><span class="pending-badge">{c.total_pending} 件</span></td>
                    <td>{c.latest_request_time.substring(0, 16)}</td> <!-- 先頭16文字だけ表示 -->
                </tr>
                {/each}
            </tbody>
        </table>

        {:else if currentView === 'item'}
        <h2>📦 品目別 未対応集計 (全 {itemRequests.length} 品目)</h2>
        <table>
            <thead>
                <tr>
                    <th>品目名</th>
                    <th>未対応の合計個数</th>
                    <th>最新の要請日時</th>
                </tr>
            </thead>
            <tbody>
                {#each displayData as i}
                <tr>
                    <td><a href={`/government/requestlist/item/${encodeURIComponent(i.item_name)}`} class="community-link">{i.item_name}</a></td>
                    <td><span class="pending-badge item-pending-count">{i.pending_total_number} 個</span> (総要請: {i.total_number} 個)</td>
                    <td>{i.last_requested_at.substring(0, 16)}</td>
                </tr>
                {/each}
            </tbody>
        </table>
        {/if}
    </div>
</div>

<style>
    /* ページタイトルとサブタイトル */
    h1 {
        color: #00796b;
        border-bottom: 2px solid #00796b;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.1em;
        color: #555;
        margin-bottom: 20px;
    }

    /* 表示切り替えボタンのスタイル */
    .view-switch-container {
        margin-bottom: 20px;
    }
    .switch-btn {
        padding: 10px 20px;
        margin-right: 10px;
        border: 1px solid #ccc;
        background-color: #f9f9f9;
        cursor: pointer;
        border-radius: 4px;
        font-size: 1em;
        transition: background-color 0.2s, color 0.2s;
    }
    .switch-btn:hover {
        background-color: #e0f2f1;
    }
    .switch-btn.active {
        background-color: #00796b; /* Teal */
        color: white;
        border-color: #00796b;
        font-weight: bold;
    }

    /* テーブルの共通スタイル */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px 15px;
        text-align: left;
    }
    th {
        background-color: #e0f7fa;
        color: #004d40;
        font-weight: 600;
    }

    /* リンク */
    .community-link {
        color: #0288d1;
        text-decoration: none;
        font-weight: bold;
    }
    .community-link:hover {
        text-decoration: underline;
    }

    /* ステータスバッジ */
    .pending-badge {
        padding: 4px 8px;
        border-radius: 4px;
        background-color: #ffcc80;
        color: #e65100;
        font-weight: bold;
        display: inline-block;
    }
    /* 色を上書き */
    .item-pending-count { 
        background-color: #ff9800;
        color: white;
    }
</style>