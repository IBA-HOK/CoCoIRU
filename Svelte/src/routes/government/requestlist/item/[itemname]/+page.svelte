<script lang="ts">
    interface RequestItem {
        request_id: number;
        community_name: string | null;
        status: string;
        number: number;
        unit: string | null;
        created_at: string | null;
        // ...他のフィールド
    }

    interface LoadData {
        itemName: string;
        requests: RequestItem[];
    }

    export let data: LoadData;

    const itemName = data.itemName;
    const requests = data.requests || [];

    // 集計: 未対応の合計個数を計算
    const totalPending = requests
        .filter(r => r.status === 'pending')
        .reduce((sum, r) => sum + r.number, 0);

    // 集計: 単位の取得 (リストの最初のアイテムから取得、なければ空)
    const unit = requests.length > 0 && requests[0].unit ? requests[0].unit : '';

    function formatDate(dateStr: string | null): string {
        if (!dateStr) return '-';
        return dateStr.substring(5, 16).replace('T', ' ');
    }

</script>

<div class="item-detail-container">
    <a href="/government/requestlist" class="back-link">← 一覧に戻る</a>

    <h1>📦 品目: {itemName} の要請状況</h1>
    <p class="subtitle">この品目を要請しているコミュニティの一覧です。</p>

    <div class="summary-card">
        <p><strong>総要請コミュニティ数:</strong> {requests.length} コミュニティ</p>
        <p><strong>未対応合計数量:</strong> <span class="total-count">{totalPending} {unit}</span></p>
    </div>

    <table>
        <thead>
            <tr>
                <th>コミュニティ名</th>
                <th>要請個数</th>
                <th>ステータス</th>
                <th>最新の要請日時</th>
            </tr>
        </thead>
        <tbody>
            {#each requests as req (req.request_id)}
                <tr>
                    <td class="community-name">{req.community_name || '不明なコミュニティ'}</td>
                    <td>
                        <span class="count-value">{req.number} {req.unit || ''}</span>
                    </td>
                    <td>
                        <span class="status-tag status-{req.status}">{req.status}</span>
                    </td>
                    <td>{formatDate(req.created_at)}</td>
                </tr>
            {/each}
            
            {#if requests.length === 0}
                <tr>
                    <td colspan="4" class="no-data">この品目に対する要請は現在ありません。</td>
                </tr>
            {/if}
        </tbody>
    </table>
</div>

<style>
    .item-detail-container {
        padding: 20px;
        max-width: 1000px;
        margin: 0 auto;
    }
    .back-link {
        display: inline-block;
        margin-bottom: 15px;
        color: #555;
        text-decoration: none;
    }
    .back-link:hover { text-decoration: underline; }

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

    /* テーブル */
    table {
        width: 100%;
        border-collapse: collapse;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px 15px;
        text-align: left;
    }
    th {
        background-color: #fae6d2; /* 薄いオレンジ */
    }
    .community-name {
        font-weight: bold;
        color: #2c3e50;
    }
    .count-value {
        font-weight: bold;
        color: #d35400;
    }
    .no-data {
        text-align: center;
        padding: 30px;
        color: #777;
    }

    /* ステータス */
    .status-tag {
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: bold;
        text-transform: uppercase;
    }
    .status-pending { background-color: #ffcc80; color: #e65100; }
    .status-processing { background-color: #b3e5fc; color: #0277bd; }
    .status-completed { background-color: #c8e6c9; color: #2e7d32; }
</style>