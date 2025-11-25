const axios = require('axios');

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
const COMMUNITIES_URL = `${API_BASE_URL}/communities/`;
const MEMBERS_URL = `${API_BASE_URL}/members/`;
const SPECIAL_NOTES_URL = `${API_BASE_URL}/special_notes/`;

// ダミーの特記事項リスト
const DUMMY_NOTES = [
    "ペット（猫）の餌が必要です。",
    "インスリンが必要です。",
    "アレルギー対応食（卵・乳製品除去）を希望します。",
    "高齢者がいるため、柔らかい食事が必要です。",
    "粉ミルクとおむつ（Mサイズ）が不足しています。",
    "透析患者が1名います。",
    "生理用品が不足しています。",
    "常備薬（降圧剤）が必要です。",
];

async function runSeeding() {
    console.log("=== testcom3.js: 特記事項 (Special Notes) の追加 ===");

    try {
        // 1. 全コミュニティを取得
        const communitiesRes = await axios.get(COMMUNITIES_URL);
        const communities = communitiesRes.data;
        
        console.log(`${communities.length} 件のコミュニティを確認しました。特記事項を追加します...`);

        for (const community of communities) {
            // ランダムに特記事項を追加するか決定 (70%の確率で追加)
            if (Math.random() > 0.3) {
                
                // A. 特記事項 (Special_notes) を作成
                const noteContent = DUMMY_NOTES[Math.floor(Math.random() * DUMMY_NOTES.length)];
                // JSON形式で保存する場合が多いですが、ここではシンプルにオブジェクトをJSON文字列化、または単なる文字列として扱います
                // DB定義はTEXT型なので自由です
                const noteData = {
                    notes_content_json: JSON.stringify({ text: noteContent }),
                    created_at: new Date().toISOString()
                };
                const noteRes = await axios.post(SPECIAL_NOTES_URL, noteData);
                const noteId = noteRes.data.special_notes_id;

                // B. メンバー (Members) を作成し、特記事項を紐付け
                const memberData = {
                    special_notes_id: noteId,
                    created_at: new Date().toISOString()
                };
                const memberRes = await axios.post(MEMBERS_URL, memberData);
                const memberId = memberRes.data.member_id;

                // C. コミュニティ (Communities) を更新し、メンバーを紐付け
                // 更新にはPUTを使いますが、既存のデータを維持しつつ member_id だけ更新します
                const updateData = {
                    name: community.name, // 名前は必須なので維持
                    member_id: memberId,  // ★ここを更新
                    latitude: community.latitude,
                    longitude: community.longitude,
                    member_count: community.member_count
                };
                await axios.put(`${COMMUNITIES_URL}${community.community_id}`, updateData);

                console.log(`[更新] ${community.name} -> 特記事項: "${noteContent}" (MemberID: ${memberId})`);
            }
        }
        console.log("\n=== 完了: 特記事項の紐付けが終了しました ===");

    } catch (error) {
        console.error("エラーが発生しました:", error.message);
    }
}

runSeeding();

// node testcom3.js