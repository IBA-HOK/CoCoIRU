<script lang="ts">
    import { goto } from '$app/navigation';
    import { invalidateAll } from '$app/navigation';
    import { getToken } from '$lib/stores/auth';

    // ------------------------------------
    // 型定義 (共通)
    // ------------------------------------
    interface RequestItem {
        request_id: number;
        community_id: number;
        request_content_id: number;
        community_name: string | null;
        item_name: string | null;
        number: number | null;
        unit: string | null;
        status: string;
        created_at: string | null;
    }

    // ------------------------------------
    // Props
    // ------------------------------------
    export let requests: RequestItem[] = [];
    export let viewMode: 'community' | 'item'; // 表示モード切り替え用

    // ------------------------------------
    // 状態管理: ソート
    // ------------------------------------
    let sortKey: string = 'time'; // 初期値: 日時
    let sortDesc: boolean = true; // 初期値: 降順

    // ソート処理 (リアクティブ)
    $: sortedRequests = [...requests].sort((a, b) => {
        let valA: any, valB: any;

        // モードによってソート対象の「名前」を変える
        if (sortKey === 'name') {
            valA = viewMode === 'community' ? (a.item_name || '') : (a.community_name || '');
            valB = viewMode === 'community' ? (b.item_name || '') : (b.community_name || '');
        } else if (sortKey === 'number') {
            valA = a.number || 0;
            valB = b.number || 0;
        } else if (sortKey === 'status') {
            valA = a.status;
            valB = b.status;
        } else if (sortKey === 'time') {
            valA = a.created_at || '';
            valB = b.created_at || '';
        } else if (sortKey === 'id') {
            valA = a.request_id;
            valB = b.request_id;
        } else {
            valA = 0; valB = 0;
        }

        if (valA < valB) return sortDesc ? 1 : -1;
        if (valA > valB) return sortDesc ? -1 : 1;
        return 0;
    });

    // ------------------------------------
    // ヘルパー関数
    // ------------------------------------
    function handleSort(key: string) {
        if (sortKey === key) {
            sortDesc = !sortDesc;
        } else {
            sortKey = key;
            sortDesc = true; // 新しいキーは降順スタート
            if (key === 'id') sortDesc = false; // IDだけは昇順スタート
        }
    }

    function getSortIcon(key: string) {
        return '↕';
    }

    function formatDate(dateStr: string | null): string {
        if (!dateStr) return '-';
        return dateStr.substring(5, 16).replace('T', ' ');
    }

    function getStatusLabel(status: string): string {
        switch (status) {
            case 'pending': return '未対応';
            case 'processing': return '対応中';
            case 'completed': return '完了';
            default: return status;
        }
    }

    const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

    async function handleAction(req: RequestItem) {
        if (!confirm(`要請 #${req.request_id} の対応を開始しますか？`)) return;

        try {
            // ステータスを 'processing' (対応中) に変更するデータを作成
            const updateData = {
                community_id: req.community_id,
                request_content_id: req.request_content_id, // ここで必要になります
                status: 'processing', // ステータス変更
                created_at: req.created_at // 日時はそのまま維持
            };

            // 既存の PUT API を呼び出す
            const token = getToken();
            const headers: Record<string, string> = { 'Content-Type': 'application/json' };
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch(`${API_BASE_URL}/support_requests/${req.request_id}`, {
                method: 'PUT',
                credentials: 'include', // Cookie を送信する
                headers,
                body: JSON.stringify(updateData)
            });

            // デバッグ: 応答の JSON をログに出す（body は一度しか読めないので clone() を使う）
            try {
                const respJson = await response.clone().json();
                console.log('handleAction response', response.status, respJson);
            } catch (e) {
                console.log('handleAction: response has no JSON body or failed to parse', e);
            }

            if (!response.ok) {
                let errorData: any = null;
                try {
                    errorData = await response.json();
                } catch (e) {
                    console.error('Failed to parse error response JSON', e);
                }
                alert(`エラー: ${errorData?.detail || '更新に失敗しました'}`);
                return;
            }

            // 成功したら画面をリロードせずにデータを最新化
            // (SvelteKitの機能でload関数を再実行させる)
            await invalidateAll();
            
            alert('対応ステータスを「対応中」に更新しました！');

        } catch (error) {
            console.error('Update error:', error);
            alert('通信エラーが発生しました');
        }
    }

    function handleCommunityClick(communityId: number) {
        goto(`/government/requestlist/community/${communityId}`);
    }

    function handleItemClick(itemName: string | null) {
        if (itemName) {
            goto(`/government/requestlist/item/${encodeURIComponent(itemName)}`);
        }
    }
</script>

<table 
    style="--th-bg-color: {viewMode === 'item' ? '#fae6d2' : '#e0f2f1'};
            --th-text-color: {viewMode === 'item' ? '#d35400' : '#004d40'};"
>
    <thead>
        <tr>
            {#if viewMode === 'community'}
                <th class="sortable" on:click={() => handleSort('id')}>
                    ID <span class="sort-icon">{getSortIcon('id')}</span>
                </th>
                <th>
                    品目
                </th>
            {:else}
                <th >
                    コミュニティ名
                </th>
            {/if}

            <th class="sortable" on:click={() => handleSort('number')}>
                要請個数 <span class="sort-icon">{getSortIcon('number')}</span>
            </th>
            <th class="sortable" on:click={() => handleSort('status')}>
                ステータス <span class="sort-icon">{getSortIcon('status')}</span>
            </th>
            <th class="sortable" on:click={() => handleSort('time')}>
                要請日時 <span class="sort-icon">{getSortIcon('time')}</span>
            </th>
            
            {#if viewMode === 'community'}
                <th class="action-col">操作</th>
            {/if}
        </tr>
    </thead>
    <tbody>
        {#each sortedRequests as req (req.request_id)}
            <tr class="status-row">
                {#if viewMode === 'community'}
                    <td>{req.request_id}</td>

                    <td
                        class="item-name item-link"
                        on:click={() => handleItemClick(req.item_name)}
                        role="button"
                        tabindex="0"
                        on:keydown={(e) => e.key === 'Enter' && handleItemClick(req.item_name)}
                    >
                        {req.item_name || '不明'}
                    </td>
                {:else}
                    <td 
                        class="community-link" 
                        on:click={() => handleCommunityClick(req.community_id)}
                        role="button" 
                        tabindex="0"
                        on:keydown={(e) => e.key === 'Enter' && handleCommunityClick(req.community_id)}
                    >
                        {req.community_name || '不明なコミュニティ'}
                    </td>
                {/if}

                <td class="number-col">{req.number} {req.unit || ''}</td>
                
                <td>
                    <span class="status-tag status-{req.status}">{getStatusLabel(req.status)}</span>
                </td>
                
                <td>{formatDate(req.created_at)}</td>

                {#if viewMode === 'community'}
                    <td class="action-col">
                        <button 
                            class="action-btn process-btn" 
                            disabled={req.status !== 'pending'}
                            on:click={() => handleAction(req)} 
                        >
                            対応 ({req.status === 'pending' ? '未' : '済'})
                        </button>
                    </td>
                {/if}
            </tr>
        {/each}

        {#if requests.length === 0}
            <tr>
                <td colspan={viewMode === 'community' ? 6 : 5} class="no-data">データがありません。</td>
            </tr>
        {/if}
    </tbody>
</table>

<style>
    /* 共通スタイルをここに移動 */
    table { 
        width: 100%; 
        border-collapse: collapse; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.05); 

        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
    }
    th, td { 
        /* 上下の線のみを維持し、左右の線を削除 */
        border-top: 1px solid #ddd; 
        border-bottom: 1px solid #ddd; 
        border-left: none; /* 左の縦線を削除 */
        border-right: none; /* 右の縦線を削除 */
        
        padding: 12px; 
        text-align: left;

        padding: 12px; 
        text-align: left; 
    }
    th { 
        background-color: var(--th-bg-color); /* 変数を使用 */
        color: var(--th-text-color);          /* 変数を使用 */
        transition: background-color 0.3s;    /* 色の切り替えを滑らかに（任意） */
    }
    
    .item-name { 
        font-weight: bold; 
        color: #0277bd; 
    }
    .community-link { 
        font-weight: bold; 
        color: #00796b; 
        cursor: pointer; 
        text-decoration: underline; 
    }
    .community-link:hover { 
        color: #004d40; 
    }
    .item-link { 
        cursor: pointer; 
        text-decoration: underline; 
        color: #ff9800; /* オレンジ系統（コミュニティリンクと区別するため） */
        font-weight: bold;
    }
    .item-link:hover { 
        color: #ef6c00; /* ホバーで濃くする */
    }
    
    .number-col { 
        font-weight: bold; 
    }
    .no-data { 
        text-align: center; 
        color: #777; 
        padding: 30px; 
    }

    /* ステータス */
    .status-tag { 
        padding: 4px 10px; 
        border-radius: 15px; 
        font-size: 0.85em; 
        font-weight: bold; 
        text-transform: uppercase; 
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

    /* ソートヘッダー */
    .sortable { 
        cursor: pointer; 
        user-select: none; 
        transition: background-color 0.2s; 
    }
    /* .sortable:hover { 
        background-color: #b2dfdb; 
    }
    .sort-icon { 
        font-size: 0.8em; 
        margin-left: 5px; 
        color: #00796b; 
    } */

    /* ボタン */
    .action-col { 
        text-align: center; 
    }
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
    .action-btn:hover { 
        background-color: #00796b; 
    }
    .action-btn:disabled { 
        background-color: #cfd8dc; 
        color: #90a4ae; 
        cursor: not-allowed; 
    }
</style>