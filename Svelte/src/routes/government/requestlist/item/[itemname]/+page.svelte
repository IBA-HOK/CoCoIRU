<script lang="ts">
    import { RequestTable } from '$lib';
    import { BackLink } from '$lib';

    export let data: any;

    $: itemName = data.itemName;
    $: requests = data.requests || [];
    
    $: totalPending = requests
        .filter((r: any) => r.status === 'pending')
        .reduce((sum: number, r: any) => sum + (r.number || 0), 0);
    
    $: unit = requests.length > 0 && requests[0].unit ? requests[0].unit : '';
</script>

<div class="item-detail-container">
    <BackLink detailMode="item" />
    <!-- <a href="/government/requestlist" class="back-link">← 一覧に戻る</a> -->

    <h1>{itemName} の要請状況</h1>
    <!-- 📦  -->
    <p class="subtitle">この品目を要請しているコミュニティの一覧です。</p>

    <div class="summary-card">
        <p><strong>総要請コミュニティ数:</strong> {requests.length} コミュニティ</p>
        <p><strong>未対応合計数量:</strong> <span class="total-count">{totalPending} {unit}</span></p>
    </div>

    <RequestTable requests={requests} viewMode="item" />

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
    .back-link:hover { 
        text-decoration: underline; 
    }
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
</style>