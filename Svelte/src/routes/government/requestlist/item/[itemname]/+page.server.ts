import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const load: PageServerLoad = async ({ params, fetch }) => {
    // URLパラメータから品目名を取得（URLエンコードされている場合があるためデコード）
    const itemName = decodeURIComponent(params.itemname);

    try {
        // 1. 行政用要請一覧APIから全データを取得
        const response = await fetch(`${API_BASE_URL}/government/requests`);
        
        if (!response.ok) {
            throw error(response.status, '要請データの取得に失敗しました');
        }

        const allRequests = await response.json();

        // 2. この品目（itemName）に一致する要請だけをフィルタリング
        const filteredRequests = allRequests.filter((req: any) => req.item_name === itemName);

        return {
            itemName, // 表示用に品目名も返す
            requests: filteredRequests
        };

    } catch (e) {
        console.error('Error loading item detail:', e);
        if (e && typeof e === 'object' && 'status' in e) {
            throw e;
        }
        throw error(500, 'データの読み込み中にエラーが発生しました');
    }
};