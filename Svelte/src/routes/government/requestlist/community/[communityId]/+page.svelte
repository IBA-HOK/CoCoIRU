<script lang="ts">
    import { goto } from '$app/navigation';
    
    interface RequestItem {
        request_id: number;
        community_id: number;
        status: string;
        created_at: string | null;
        // 結合データ
        item_name: string | null;
        number: number | null;
        unit: string | null;
    }

    interface Community {
        community_id: number;
        name: string;
        member_count: number;
        // 必要に応じて latitude, longitude など
    }

    interface LoadData {
        community: Community;
        requests: RequestItem[];
        specialNotes: string | null;
    }

    export let data: LoadData;

    const community = data.community;
    const requests = data.requests || [];
    const specialNotes = data.specialNotes;

    // 日時フォーマット
    function formatDate(dateStr: string | null): string {
        if (!dateStr) return '-';
        return dateStr.substring(5, 16).replace('T', ' ');
    }
    
    // ステータスに応じたラベル
    function getStatusLabel(status: string): string {
        switch(status) {
            case 'pending': return '未対応';
            case 'processing': return '対応中';
            case 'completed': return '完了';
            default: return status;
        }
    }
    
    // 「対応」ボタンのアクション (後で実装するためログ出力のみ)
    function handleAction(req: RequestItem) {
        console.log(`対応開始: Request ID ${req.request_id}`);
        alert(`要請 #${req.request_id} (${req.item_name}) の対応を開始しますか？\n(機能は未実装です)`);
    }

</script>

<div class="detail-container">
    <a href="/government/requestlist" class="back-link">← 一覧に戻る</a>

    <header>
        <h1>{community.name} の要請詳細</h1>
        <div class="info-bar">
            <span><strong>避難人数:</strong> {community.member_count} 人</span>
            <span><strong>要請件数:</strong> {requests.length} 件</span>
        </div>
    </header>

    {#if specialNotes}
        <div class="special-notes-card">
            <h3>⚠️ 特記事項 (手入力要請)</h3>
            <p class="note-content">{specialNotes}</p>
        </div>
    {/if}

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>品目</th>
                <th>個数</th>
                <th>ステータス</th>
                <th>要請日時</th>
                <th class="action-col">操作</th>
            </tr>
        </thead>
        <tbody>
            {#each requests as req (req.request_id)}
            <tr class="status-row">
                <td>{req.request_id}</td>
                <td class="item-name">{req.item_name || '不明'}</td>
                <td class="number-col">
                    {req.number} {req.unit || ''}
                </td>
                <td>
                    <span class="status-tag status-{req.status}">{req.status}</span>
                </td>
                <td>{formatDate(req.created_at)}</td>
                <td class="action-col">
                    <button 
                        class="action-btn" 
                        disabled={req.status !== 'pending'}
                        on:click={() => handleAction(req)}
                    >
                        {getStatusLabel(req.status)}
                    </button>
                </td>
            </tr>
            {/each}
            
            {#if requests.length === 0}
            <tr>
                <td colspan="6" class="no-data">このコミュニティからの要請はありません。</td>
            </tr>
            {/if}
        </tbody>
    </table>
</div>

<style>
    .detail-container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        font-family: sans-serif;
    }
    .back-link {
        display: inline-block;
        margin-bottom: 15px;
        color: #555;
        text-decoration: none;
    }
    .back-link:hover {
        text-decoration: underline;
    }
    header {
        border-bottom: 2px solid #004d40;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    h1 {
        color: #004d40;
        margin: 0 0 10px 0;
    }
    .info-bar span {
        margin-right: 20px;
        font-size: 1.1em;
        color: #444;
    }

    /* テーブル */
    table {
        width: 100%;
        border-collapse: collapse;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    th {
        background-color: #e0f2f1; /* 薄い緑 */
        color: #004d40;
    }
    .item-name {
        font-weight: bold;
        color: #0277bd;
    }
    .number-col {
        font-weight: bold;
    }
    .no-data {
        text-align: center;
        color: #777;
        padding: 30px;
    }

    /* ステータスタグ */
    .status-tag { 
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: bold;
        text-transform: uppercase;
    }
    .status-pending { background-color: #ffcc80; color: #e65100; }
    .status-processing { background-color: #b3e5fc; color: #0277bd; }
    .status-completed { background-color: #c8e6c9; color: #2e7d32; }

    /* ボタン */
    .action-col { text-align: center; }
    .action-btn {
        background-color: #009688;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: bold;
        transition: background 0.2s;
    }
    .action-btn:hover { background-color: #00796b; }
    .action-btn:disabled {
        background-color: #cfd8dc;
        color: #90a4ae;
        cursor: not-allowed;
    }
    .special-notes-card {
        background-color: #fff8e1; /* 薄い黄色 */
        border: 1px solid #ffecb3;
        border-left: 5px solid #ffc107; /* 目立つ黄色 */
        padding: 15px;
        margin-bottom: 25px;
        border-radius: 4px;
    }
    .special-notes-card h3 {
        margin-top: 0;
        color: #f57f17;
        font-size: 1.1em;
        display: flex;
        align-items: center;
    }
    .note-content {
        margin-bottom: 0;
        font-size: 1.1em;
        color: #333;
        font-weight: bold;
    }
</style>