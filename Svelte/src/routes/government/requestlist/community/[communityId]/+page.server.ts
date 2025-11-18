import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
    // 🚨 URLのパスからコミュニティIDを取得
    const communityId = params.communityId;
    
    // 仮データ
    const dummyRequests = [
        { id: 101, item: "水 (2L)", number: 20, status: "pending", created_at: "2025-11-04 10:30" },
        { id: 102, item: "毛布", number: 50, status: "processing", created_at: "2025-11-04 09:15" },
        { id: 103, item: "簡易トイレ", number: 5, status: "completed", created_at: "2025-11-03 18:45" },
    ];
    
    return {
        // 画面側で利用するために渡す
        communityId: communityId,
        requests: dummyRequests
    };
};