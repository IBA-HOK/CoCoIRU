// @ts-nocheck
import type { PageServerLoad } from './$types';

export const load = async () => {
    // 仮データ
    const dummyCommunities = [
        { 
            id: 1, 
            name: "A地区小学校避難所 (102号室)", 
            latitude: 34.6937, 
            longitude: 135.5023, 
            pending_requests: 5,
        },
        { 
            id: 2, 
            name: "B地区体育館コミュニティ", 
            latitude: 34.7000, 
            longitude: 135.5500, 
            pending_requests: 2,
        },
        { 
            id: 3, 
            name: "C町高齢者グループ", 
            latitude: 34.6500, 
            longitude: 135.4500, 
            pending_requests: 0,
        },
    ];

    return {
        communities: dummyCommunities // 画面側にデータを渡す
    };
};;null as any as PageServerLoad;