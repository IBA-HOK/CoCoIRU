import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const load: PageServerLoad = async ({ params, fetch }) => {
    // URLパラメータからIDを取得
    const communityId = Number(params.communityId);

    try {
        // 1. コミュニティ基本情報の取得 (ヘッダー表示用)
        const communityRes = await fetch(`${API_BASE_URL}/communities/${communityId}`);
        
        if (communityRes.status === 404) {
            throw error(404, 'コミュニティが見つかりません');
        }
        
        // 2. 行政用要請一覧APIから全データを取得 (詳細情報付き)
        const requestsRes = await fetch(`${API_BASE_URL}/government/requests`);
        
        if (!requestsRes.ok) {
            throw error(requestsRes.status, '要請データの取得に失敗しました');
        }

        const community = await communityRes.json();
        const allRequests = await requestsRes.json();

        // 3. このコミュニティの要請だけをフィルタリング
        // (API側でフィルタリング機能を作っていないため、フロントサーバー側で行う)
        const filteredRequests = allRequests.filter((req: any) => req.community_id === communityId);

        // 特記事項 (Special Notes) の取得
        let specialNotes = null;

        // コミュニティに紐付くメンバーがいる場合
        if (community.member_id) {
            try {
                // Memberを取得
                const memberRes = await fetch(`${API_BASE_URL}/members/${community.member_id}`);
                if (memberRes.ok) {
                    const member = await memberRes.json();
                    
                    // SpecialNotesを取得
                    if (member.special_notes_id) {
                        const notesRes = await fetch(`${API_BASE_URL}/special_notes/${member.special_notes_id}`);
                        if (notesRes.ok) {
                            const notesData = await notesRes.json();
                            // JSON文字列の場合はパースし、そうでなければそのまま使う
                            try {
                                const parsed = JSON.parse(notesData.notes_content_json);
                                specialNotes = parsed.text || parsed; // {text: "..."} 形式なら text を使う
                            } catch {
                                specialNotes = notesData.notes_content_json; // パースできない場合は文字列そのまま
                            }
                        }
                    }
                }
            } catch (err) {
                console.error("特記事項の取得に失敗しましたが、続行します", err);
            }
        }

        return {
            community,
            requests: filteredRequests,
            specialNotes
        };

    } catch (e) {
        console.error('Error loading community detail:', e);
        // SvelteKitのエラーを再スロー
        if (e && typeof e === 'object' && 'status' in e) {
            throw e;
        }
        throw error(500, 'データの読み込み中にエラーが発生しました');
    }
};