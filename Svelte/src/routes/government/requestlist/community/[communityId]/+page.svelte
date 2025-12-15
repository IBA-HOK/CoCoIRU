<script lang="ts">
    import { RequestTable } from '$lib';
    import { BackLink } from '$lib';
    import { Button, Surface, Title } from '$lib';
    
    interface Community {
        community_id: number;
        name: string;
        member_count: number;
    }
    interface LoadData {
        community: Community;
        requests: any[];
        specialNotes: string | null;
    }

    export let data: LoadData;

    $: community = data.community;
    $: requests = data.requests || [];
    $: specialNotes = data.specialNotes;

</script>

<div class="detail-container">
    <BackLink detailMode="community" />
    <!-- <a href="/government/requestlist" class="back-link">← 一覧に戻る</a> -->

    <header>
        <h1>要請詳細</h1>
        <!-- <h1>{community.name} の要請詳細</h1> -->
        <!-- <pre>{JSON.stringify(community, null, 2)}</pre> -->
        <div class="info-bar">
            <span><strong>避難人数:</strong> {typeof community.member_count === 'number' ? `${community.member_count} 人` : '—'}</span>
            <span><strong>要請件数:</strong> {requests.length} 件</span>
        </div>
    </header>

    {#if specialNotes}
        <div class="special-notes-card">
            <h3>特記事項 (手入力要請)</h3>
            <p class="note-content">{specialNotes}</p>
        </div>
    {/if}

    
    <RequestTable requests={requests} viewMode="community" />

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

    /* 特記事項のスタイル */
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