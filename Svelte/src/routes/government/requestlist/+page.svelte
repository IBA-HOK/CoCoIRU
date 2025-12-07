<script lang="ts">
    import { goto } from '$app/navigation';
    import { Button, Surface, Title } from '$lib';
    
    // API (GovernmentRequestItem) のレスポンスに合わせた型定義
    interface RequestItem {
        request_id: number;
        community_id: number;
        status: string; // 'pending' | 'processing' | 'completed'
        created_at: string | null; // null許容
        
        // APIですでに結合されている情報
        community_name: string | null;
        latitude: number | null;
        longitude: number | null;
        number: number | null;
        item_name: string | null;
        unit: string | null;
    }

    // ページに渡されるデータの型
    interface LoadData {
        requests: RequestItem[];
    }

    // コミュニティ別集計用の型
    interface CommunitySummary {
        id: number;
        name: string;
        total_pending: number;
        latest_request_time: string | null;
    }

    // 品目別集計用の型
    interface ItemSummary {
        name: string;
        total_pending: number;
        latest_request_time: string | null;
        unit: string;
        community_ids: Set<number>;
    }

    
    export let data: LoadData; 
    
    // APIからデータが来ているので、空配列チェックだけでOK
    const allRequests: RequestItem[] = data.requests ?? [];

    // 表示切り替えのロジック
    let currentView: 'community' | 'item' = 'community';

    // 並び替え用の状態管理変数
    let sortKey: string = 'pending'; // 初期値: 未対応数
    let sortDesc: boolean = true;    // 初期値: 降順 (大きい/新しい順)


    // コミュニティ別集計
    const communityMap = new Map<number, CommunitySummary>();

    for (const req of allRequests) {
        const cId = req.community_id;
        // 名前がない場合はIDで代用
        const cName = req.community_name || `コミュニティ #${cId}`;

        if (!communityMap.has(cId)) {
            communityMap.set(cId, {
                id: cId,
                name: cName,
                total_pending: 0,
                latest_request_time: null
            });
        }

        const summary = communityMap.get(cId)!;

        // 未対応数をカウント
        if (req.status === 'pending') {
            summary.total_pending += 1;
        }

        // 最終日時を更新 (nullチェック付き)
        if (req.created_at) {
            if (!summary.latest_request_time || req.created_at > summary.latest_request_time) {
                summary.latest_request_time = req.created_at;
            }
        }
    }

    // 品目別集計
    const itemMap = new Map<string, ItemSummary>();

    for (const req of allRequests) {
        const iName = req.item_name || '不明な品目';
        const unit = req.unit || '個';
        const num = req.number || 0;

        if (!itemMap.has(iName)) {
            itemMap.set(iName, {
                name: iName,
                total_pending: 0,
                latest_request_time: null,
                unit: unit,
                community_ids: new Set()
            });
        }

        const summary = itemMap.get(iName)!;

        // 未対応数をカウント
        if (req.status === 'pending') {
            summary.total_pending += num;
        }
        summary.community_ids.add(req.community_id);

        // 最終日時を更新 (nullチェック付き)
        if (req.created_at) {
            if (!summary.latest_request_time || req.created_at > summary.latest_request_time) {
                summary.latest_request_time = req.created_at;
            }
        }
    }

    // ソートハンドラ
    function handleSort(key: string) {
        if (sortKey === key) {
            sortDesc = !sortDesc; // 同じキーなら昇順/降順を反転
        } else {
            sortKey = key;
            sortDesc = true; // 新しいキーなら降順リセット
        }
    }

    // ソートアイコン取得
    function getSortIcon(key: string) {
        if (sortKey !== key) return '↕'; 
        return sortDesc ? '▼' : '▲';
    }

    // コミュニティ一覧 (未対応数が多い順)
    $: communitySummaries = Array.from(communityMap.values())
        .sort((a, b) => {
            let valA: any, valB: any;
            if (sortKey === 'time') {
                valA = a.latest_request_time || '';
                valB = b.latest_request_time || '';
            } else {
                // default: pending (未対応数)
                valA = a.total_pending;
                valB = b.total_pending;
            }
            if (valA < valB) return sortDesc ? 1 : -1;
            if (valA > valB) return sortDesc ? -1 : 1;
            return 0;
        });

    // 品目一覧 (未対応数が多い順)
    $: itemSummaries = Array.from(itemMap.values())
        .sort((a, b) => {
            let valA: any, valB: any;
            if (sortKey === 'count') { // 要請元数
                valA = a.community_ids.size;
                valB = b.community_ids.size;
            } else if (sortKey === 'time') { // 最新日時
                valA = a.latest_request_time || '';
                valB = b.latest_request_time || '';
            } else {
                // default: pending (未対応数)
                valA = a.total_pending;
                valB = b.total_pending;
            }
            if (valA < valB) return sortDesc ? 1 : -1;
            if (valA > valB) return sortDesc ? -1 : 1;
            return 0;
        });

    
    // 日時フォーマット (null安全)
    function formatDate(dateStr: string | null): string {
        if (!dateStr) return '-';
        // "2025-11-20T10:00:00" -> "11-20 10:00"
        return dateStr.substring(5, 16).replace('T', ' ');
    }

    // 詳細ページへの遷移
    function goToDetail(id: number) {
        // 以前のルーティング修正に従い、communityディレクトリへ
        goto(`/government/requestlist/community/${id}`);
    }

</script>

<div class="request-list-container">
    <Title titleText="支援要請一覧" subtitleText="未対応の要請や対応状況を、切り替えて確認できます。"/>
    <Surface>
    <div class="view-switch-container">
        <button 
            class="switch-btn" 
            class:active={currentView === 'community'} 
            on:click={() => { currentView = 'community'; sortKey = 'pending'; sortDesc = true; }}
        >
            🏢 コミュニティ別リスト
        </button>
        
        <button 
            class="switch-btn" 
            class:active={currentView === 'item'} 
            on:click={() => { currentView = 'item'; sortKey = 'pending'; sortDesc = true; }}
        >
            📦 品目別集計
        </button>
    </div>
    <div class="list-container">
        {#if currentView === 'community'}
            <h2>🏢 コミュニティ別 (全 {communitySummaries.length} 件)</h2>
            <table>
                <thead>
                    <tr>
                        <th>コミュニティ名</th>

                        <th class="sortable" on:click={() => handleSort('pending')}>
                            未対応要請数 <span class="sort-icon">{getSortIcon('pending')}</span>
                        </th>
                        
                        <th class="sortable" on:click={() => handleSort('time')}>
                            最新の要請日時 <span class="sort-icon">{getSortIcon('time')}</span>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {#each communitySummaries as c (c.id)}
                        <tr class="clickable-row" on:click={() => goToDetail(c.id)}>
                            <td class="link-text">{c.name}</td>
                            <td>
                                {#if c.total_pending > 0}
                                    <span class="pending-badge">{c.total_pending} 件</span>
                                {:else}
                                    <span class="ok-badge">対応完了</span>
                                {/if}
                            </td>
                            <td>{formatDate(c.latest_request_time)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>

        {:else if currentView === 'item'}
            <h2>📦 品目別 (全 {itemSummaries.length} 品目)</h2>
            <table>
                <thead>
                    <tr>
                        <th>品目名</th>
                        <th class="sortable status-header" on:click={() => handleSort('pending')}>
                            未対応 合計数量 <span class="sort-icon">{getSortIcon('pending')}</span>
                        </th>
                        
                        <th class="sortable" on:click={() => handleSort('count')}>
                            要請元数 <span class="sort-icon">{getSortIcon('count')}</span>
                        </th>
                        
                        <th class="sortable" on:click={() => handleSort('time')}>
                            最新の要請日時 <span class="sort-icon">{getSortIcon('time')}</span>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {#each itemSummaries as i (i.name)}
                        <tr>
                            <td>
                                <a href={`/government/requestlist/item/${encodeURIComponent(i.name)}`} class="link-text">
                                    {i.name}
                                </a>
                            </td>
                            <td>
                                {#if i.total_pending > 0}
                                    <span class="pending-badge item-badge">{i.total_pending} {i.unit}</span>
                                {:else}
                                    <span class="ok-badge">充足</span>
                                {/if}
                            </td>
                            <td>{i.community_ids.size} 箇所</td>
                            <td>{formatDate(i.latest_request_time)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        {/if}
    </div>
    </Surface>
</div>

<style>
    /* ベーススタイル */
    h2 {
        color: var(--primary);
        font-size: 1.25rem;
        margin: 0 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid var(--outline-sub);
    }

    /* 切り替えボタン */
    .view-switch-container {
        margin-bottom: 24px;
        display: flex;
        gap: 12px;
    }

    .switch-btn {
        padding: 10px 20px; 
        margin-right: 10px; 
        border: 1px solid var(--outline);
        background-color: var(--bg); 
        cursor: pointer; 
        border-radius: 4px; 
        font-size: 1em;
        color: var(--on-primary-container);
    }

    .switch-btn:hover { 
        background-color: var(--primary-container);
        border-color: var(--primary-container);
        color: var(--on-primary-container);
    }

    .switch-btn.active { 
        background-color: var(--primary);
        color: var(--on-primary);
        border-color: var(--primary);
        font-weight: bold;
        box-shadow: 0 2px 4px var(--shadow);
    }

    /* テーブル */
    table { 
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 10px;
        border: 1px solid var(--outline-sub);
        border-radius: 8px;
        overflow: hidden;
    }

    th, td { 
        padding: 12px 15px; 
        text-align: left; 
        border-bottom: 1px solid var(--outline-sub);
    }

    tbody tr:last-child td {
        border-bottom: none;
    }

    th { 
        background-color: var(--primary-container);
        color: var(--on-primary-container);
        font-weight: bold;
        font-size: 0.95em;
        white-space: nowrap;
    }

    td {
        color: var(--text);
        background-color: var(--card);
    }

    .status-header {
        width: 180px; 
    }

    /* 行のホバーとリンク */
    .clickable-row { 
        cursor: pointer; 
        transition: background-color 0.1s; 
    }

    .clickable-row:hover { 
        background-color: var(--card-high);
    }

    .link-text { 
        color: var(--primary);
        font-weight: bold; 
        text-decoration: none; 
    }

    .link-text:hover { 
        text-decoration: underline; 
    }

    /* バッジ */
    .pending-badge {
        padding: 4px 10px; 
        border-radius: 12px; 
        background-color: #ffcc80; 
        color: #e65100; 
        font-weight: bold;
        
    }

    .item-badge { 
        background-color: #ff9800; 
        color: white; 
    }

    .ok-badge {
        padding: 4px 10px; 
        border-radius: 12px; 
        background-color: #c8e6c9; 
        color: #2e7d32; 
        font-size: 0.9em;
    }

    .sortable {
        cursor: pointer;
        user-select: none;
        transition: background-color 0.2s;
    }

    .sortable:hover {
        background-color: #b2dfdb;
    }
    
    .sort-icon {
        font-size: 0.8em;
        margin-left: 5px;
        color: #00796b;
    }
</style>