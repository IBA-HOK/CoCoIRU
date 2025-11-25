import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; 

export const load: PageServerLoad = async ({ fetch }) => {
    try {
        // 新しく作成した行政専用APIエンドポイントを呼び出す
        const response = await fetch(`${API_BASE_URL}/government/requests`);
        
        if (!response.ok) {
            const errorBody = await response.json();
            console.error('API Error:', errorBody);
            throw error(response.status, `データ取得に失敗: ${errorBody.detail || '不明なエラー'}`);
        }

        // 結合済みのデータを取得
        const requests = await response.json();

        return {
            requests: requests
        };

    } catch (e) {
        console.error('Error fetching government requests:', e);
        throw error(500, 'サーバーからのデータ取得中に予期せぬエラーが発生しました。');
    }
};