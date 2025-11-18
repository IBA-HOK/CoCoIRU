<script lang="ts">
    import { goto } from '$app/navigation';
    export let data;
    
    const communityId = data.communityId;
    const requests = data.requests;
    
    // ダミーのコミュニティ名とメモ
    const communityData = data.communityId == 1 
        ? { name: "A地区小学校避難所 (102号室)", notes: "要配慮者向け食料を優先" }
        : { name: `コミュニティ #${communityId}`, notes: "特記事項なし" };
</script>

<div class="detail-container">
    <h1>{communityData.name} の支援要請一覧</h1>
    <p class="subtitle"><strong>コミュニティID:</strong> {communityId} | <strong>特記事項:</strong> {communityData.notes}</p>

    <table>
        <thead>
            <tr>
                <th>要請ID</th>
                <th>品目</th>
                <th>個数</th>
                <th>ステータス</th>
                <th>要請日時</th>
                <th class="action-col">対応</th>
            </tr>
        </thead>
        <tbody>
            {#each requests as req (req.id)}
            <tr class="status-row">
            <td>{req.id}</td>
            <td>{req.item}</td>
            <td>{req.number}</td>
            <td><span class="status-tag status-{req.status}">{req.status}</span></td>
            <td>{req.created_at}</td>
            <td class="action-col">
                <button class="action-btn process-btn" disabled={req.status !== 'pending'}>対応 ({req.status === 'pending' ? '未' : '済'})</button>
            </td>
            </tr>
        {/each}
        </tbody>
    </table>
</div>

<style>
    .detail-container {
        font-family: sans-serif;
    }
    h1 {
        color: #004d40;
        border-bottom: 2px solid #004d40;
        padding-bottom: 8px;
        margin-top: 10px;
    }
    .subtitle {
        margin-bottom: 20px;
        color: #555;
    }
    
    /* テーブルの共通スタイル */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 10px;
        text-align: left;
    }
    th {
        background-color: #f0f0f0;
    }

    /* ステータ */
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
    .status-completed {
        background-color: #c8e6c9;
        color: #2e7d32;
    }
    
    .action-col {
        text-align: center;
        width: 120px;
    }
    .action-btn {
        background-color: #00bcd4;
        color: white;
        border: none;
        padding: 6px 10px;
        border-radius: 4px;
        cursor: pointer;
    }
    .action-btn:disabled {
        background-color: #ccc;
        cursor: not-allowed;
    }
</style>