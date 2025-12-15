<script lang="ts">
    // どの詳細ページからの遷移かを示すモード (必須)
    export let detailMode: 'community' | 'item';

    // 戻り先のURLを動的に生成
    $: backUrl = getBackUrl(detailMode);

    function getBackUrl(mode: 'community' | 'item'): string {
        const baseUrl = '/government/requestlist';
        
        // 品目詳細ページ（item）からの遷移であれば、一覧画面のviewMode='item'を付与
        if (mode === 'item') {
            return `${baseUrl}?viewMode=item`;
        }
        
        // コミュニティ詳細ページ（community）からの遷移であれば、viewMode='community'を付与（あるいはクエリパラメータなしでデフォルト動作）
        return `${baseUrl}?viewMode=community`;
    }
</script>

<a href={backUrl} class="back-link">
    ← 一覧に戻る
</a>

<style>
    .back-link { 
        display: inline-block; 
        margin-bottom: 15px; 
        color: #555; 
        text-decoration: none; 
        font-weight: bold;
        padding: 5px 10px;
        border: 1px solid #ccc;
        border-radius: 4px;
        transition: background-color 0.2s, border-color 0.2s;
    }
    .back-link:hover { 
        text-decoration: none; 
        background-color: #eee;
        border-color: #999;
    }
</style>