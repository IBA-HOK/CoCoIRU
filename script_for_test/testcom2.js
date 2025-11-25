const axios = require('axios');

// =========================================================
// 1. 設定
// =========================================================

// ターゲットAPIのベースURL
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';
const COMMUNITIES_URL = `${API_BASE_URL}/communities/`;
const ITEMS_URL = `${API_BASE_URL}/items/`;
const REQUEST_CONTENT_URL = `${API_BASE_URL}/request_content/`;
const SUPPORT_REQUESTS_URL = `${API_BASE_URL}/support_requests/`;

// 生成するコミュニティの数と要請数
const NUM_COMMUNITIES_TO_CREATE = 10;
const REQUESTS_PER_COMMUNITY = 3; // コミュニティあたりに作成する要請の最大数

// 名古屋市の中心座標 (おおよそ) - ランダムな座標生成に使用
const NAGOYA_CENTER = { lat: 35.1814, lon: 136.9063 };
const COORD_RANDOM_RANGE = 0.1;

// 必須の支援品目リスト
const INITIAL_ITEMS = [
    { item_name: "水 (2L)", unit: "本", category: "食料・飲料", description: "飲料水、大人1日3L目安" },
    { item_name: "毛布", unit: "枚", category: "生活必需品", description: "防寒用" },
    { item_name: "簡易トイレ", unit: "個", category: "衛生用品", description: "5回分セットなど" },
    { item_name: "粉ミルク", unit: "缶", category: "要配慮者向け", description: "乳幼児向け" },
    { item_name: "衛生マスク", unit: "箱", category: "衛生用品", description: "50枚入り" },
];

// =========================================================
// 2. ヘルパー関数
// =========================================================

/**
 * 範囲内のランダムな整数を生成するヘルパー関数
 */
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * 中心の緯度・経度からランダムにずらした座標を生成するヘルパー関数
 */
function getRandomCoordinates(centerLat, centerLon, range) {
    const lat = centerLat + (Math.random() * 2 * range - range);
    const lon = centerLon + (Math.random() * 2 * range - range);
    return { latitude: parseFloat(lat.toFixed(5)), longitude: parseFloat(lon.toFixed(5)) };
}

/**
 * APIへPOSTリクエストを送信し、結果（ID）を返す
 */
async function postToApi(url, data, dataName) {
    try {
        const response = await axios.post(url, data);
        console.log(`[成功] ${dataName}を作成 (ID: ${response.data.items_id || response.data.community_id || response.data.request_content_id || response.data.request_id})`);
        return response.data;
    } catch (error) {
        if (error.response) {
            console.error(`[失敗] ${dataName} - Status: ${error.response.status}`);
            // FastAPIのバリデーションエラー(422)や外部キーエラー(409)の詳細を表示
            console.error('   -> Error Details:', JSON.stringify(error.response.data.detail, null, 2) || error.response.data);
        } else {
            console.error(`[失敗] ${dataName} - ネットワークまたはリクエスト設定のエラー: ${error.message}`);
        }
        return null; // 失敗時はnullを返す
    }
}

// =========================================================
// 3. データ作成関数（CRUDラッパー）
// =========================================================

/**
 * 1. Items を作成し、IDを返す
 */
async function createItem(item) {
    const result = await postToApi(ITEMS_URL, item, `品目: ${item.item_name}`);
    return result ? result.items_id : null;
}

/**
 * 2. Communities を作成し、IDを返す
 */
async function createCommunity(index) {
    const coords = getRandomCoordinates(NAGOYA_CENTER.lat, NAGOYA_CENTER.lon, COORD_RANDOM_RANGE);
    const communityData = {
        name: `災害拠点避難所-コミュニティ${index}`,
        latitude: coords.latitude,
        longitude: coords.longitude,
        member_count: getRandomInt(50, 500),
    };
    const result = await postToApi(COMMUNITIES_URL, communityData, `コミュニティ: ${communityData.name}`);
    return result ? result.community_id : null;
}

/**
 * 3. RequestContent を作成し、IDを返す (Items に依存)
 */
async function createRequestContent(itemId, number) {
    const requestContentData = {
        items_id: itemId, // 必須
        number: number,   // 必須
    };
    const result = await postToApi(REQUEST_CONTENT_URL, requestContentData, `要請内容 (品目ID:${itemId} / 数量:${number})`);
    return result ? result.request_content_id : null;
}

/**
 * 4. SupportRequest を作成し、IDを返す (Communities と RequestContent に依存)
 */
async function createSupportRequest(communityId, requestContentId, status) {
    const supportRequestData = {
        community_id: communityId,          // 必須
        request_content_id: requestContentId, // 必須
        status: status, // pending, processing, completed
        created_at: new Date().toISOString()
    };
    const result = await postToApi(SUPPORT_REQUESTS_URL, supportRequestData, `支援要請 (C:${communityId}, RC:${requestContentId}, Status:${status})`);
    return result ? result.request_id : null;
}

// =========================================================
// 4. メインの実行関数 (testcom2の本体)
// =========================================================
async function runCreationLoop() {
    console.log("========================================");
    console.log(`🤖 testcom2.js: 支援要請リスト用のダミーデータ作成を開始します`);
    console.log("========================================");

    // ----------------------------------------
    // Step 1: Items (支援品目) の作成とIDの収集
    // ----------------------------------------
    console.log("\n--- [Step 1/3] Items (支援品目) の作成 ---");
    const itemCreationPromises = INITIAL_ITEMS.map(item => createItem(item));
    const createdItems = await Promise.all(itemCreationPromises);
    const itemIds = createdItems.filter(id => id !== null);
    if (itemIds.length === 0) {
        console.error("致命的エラー: Items の作成に失敗しました。要請データを作成できません。");
        return;
    }
    console.log(`\n✅ Items (${itemIds.length} 種類) の作成完了。ID: [${itemIds.join(', ')}]`);

    // ----------------------------------------
    // Step 2: Communities (要請元コミュニティ) の作成とIDの収集
    // ----------------------------------------
    console.log("\n--- [Step 2/3] Communities (コミュニティ) の作成 ---");
    const communityPromises = Array.from({ length: NUM_COMMUNITIES_TO_CREATE }, (_, i) => createCommunity(i + 1));
    const communityIds = (await Promise.all(communityPromises)).filter(id => id !== null);
    if (communityIds.length === 0) {
        console.error("致命的エラー: Communities の作成に失敗しました。要請データを作成できません。");
        return;
    }
    console.log(`\n✅ Communities (${communityIds.length} 個) の作成完了。ID: [${communityIds.join(', ')}]`);

    // ----------------------------------------
    // Step 3: SupportRequest (支援要請) の作成 (RequestContentをネストして作成)
    // ----------------------------------------
    console.log("\n--- [Step 3/3] Support Requests (支援要請) の作成 ---");
    let successfulRequests = 0;
    
    for (const communityId of communityIds) {
        const numRequests = getRandomInt(1, REQUESTS_PER_COMMUNITY);
        
        for (let i = 0; i < numRequests; i++) {
            // ランダムに品目と数量、ステータスを選択
            const randomItemId = itemIds[getRandomInt(0, itemIds.length - 1)];
            const randomNumber = getRandomInt(5, 100);
            // pendingが多めになるように設定
            const randomStatus = ['pending', 'pending', 'pending', 'processing', 'completed'][getRandomInt(0, 4)];
            
            // a. RequestContent を作成し、IDを取得
            const rcId = await createRequestContent(randomItemId, randomNumber);
            
            if (rcId) {
                // b. SupportRequest を作成 (外部キーとしてrcIdとcommunityIdを使用)
                const requestId = await createSupportRequest(communityId, rcId, randomStatus);
                if (requestId) {
                    successfulRequests++;
                }
            }
        }
    }

    console.log("\n========================================");
    console.log(`✨ testcom2.js: ダミーデータ作成完了!`);
    console.log(`- 作成された支援要請数: ${successfulRequests} 件`);
    console.log(`- 作成されたコミュニティ数: ${communityIds.length} 個`);
    console.log(`- 作成された品目数: ${itemIds.length} 種類`);
    console.log("========================================");
    console.log("⚠️ 注意: 外部キー制約違反を避けるため、実行前にデータベース (database.db) のデータがクリアされていることを確認してください。");
}

runCreationLoop();

// =========================================================
// uvicorn app.main:app --reload
// node testcom2.js