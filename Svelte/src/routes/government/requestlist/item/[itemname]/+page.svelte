<script lang="ts">
    import { page } from '$app/stores';

    // URLパラメータから品目名を取得
    const itemName = $page.params.itemname;

    // API連携時に +page.server.ts からデータを受け取る
    export let data;
    const requests = data.requests || [];

    // ダミーデータ
    const dummyCommunities = [
        { name: "A地区小学校避難所 (102号室)", number: 20, status: "pending", latest_request_time: "2025-11-04 10:30" },
        { name: "B地区体育館コミュニティ", number: 30, status: "pending", latest_request_time: "2025-11-04 11:00" },
    ];
</script>

<div class="item-detail-container">    
    <h1>📦 品目: {decodeURIComponent(itemName)} の要請状況</h1>
    <p class="subtitle">この品目を要請しているコミュニティの一覧と、それぞれの未対応個数です。</p>

    <div class="summary-card">
        <p><strong>総要請コミュニティ数:</strong> {requests.length > 0 ? requests.length : dummyCommunities.length} コミュニティ</p>
        <p><strong>未対応合計個数 (ダミー):</strong> <span class="total-count">{dummyCommunities.reduce((sum, c) => sum + c.number, 0)} 個</span></p>
    </div>

    <table>
        <thead>
            <tr>
                <th>コミュニティ名</th>
                <th>要請個数</th>
                <th>ステータス (直近)</th>
                <th>最新の要請日時</th>
            </tr>
        </thead>
        <tbody>
            {#each requests.length > 0 ? requests : dummyCommunities as c}
                <tr>
                    <td>{c.name}</td>
                    <td><span class="count-value">{c.number} 個</span></td>
                    <td><span class="status-tag status-{c.status}">{c.status}</span></td>
                    <td>{c.latest_request_time}</td>
                </tr>
            {/each}
        </tbody>
    </table>
    
    {#if requests.length === 0 && dummyCommunities.length === 0}
        <p class="no-data-msg">この品目に対する要請は現在ありません。（API接続後に動的に反映されます）</p>
    {/if}

</div>

<style>
    h1 {
        color: #d35400; /* Orange/Brown */
        border-bottom: 2px solid #d35400;
        padding-bottom: 10px;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #555;
        margin-bottom: 20px;
    }
    .summary-card {
        background-color: #fff3e0;
        border-left: 5px solid #d35400;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .total-count {
        font-size: 1.2em;
        font-weight: bold;
        color: #d35400;
    }

    /* テーブルの共通スタイル */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px 15px;
        text-align: left;
    }
    th {
        background-color: #fae6d2;
    }
    .count-value {
        font-weight: bold;
        color: #2980b9;
    }

    /* ステータス */
    .status-tag {
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.9em;
        font-weight: bold;
        text-transform: capitalize;
    }
    .status-pending {
        background-color: #ffcc80;
        color: #e65100;
    }
    .status-processing {
        background-color: #b3e5fc;
        color: #0277bd;
    }
</style>