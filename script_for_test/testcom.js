const axios = require('axios');

// ## 1. ターゲットAPIのURL (ご自身の環境に合わせてください)
// FastAPIのデフォルト (http://127.0.0.1:8000) を想定
const API_URL = 'http://127.0.0.1:8000/api/v1/communities/';

// ## 2. 生成するコミュニティの数
const NUM_TO_CREATE = 50;

// ## 3. 名古屋市の中心座標 (おおよそ)
const NAGOYA_CENTER = {
  lat: 35.1814, // 緯度
  lon: 136.9063  // 経度
};

// ## 4. 中心からのバラつき具合 (度単位)
// 0.1度 = 約11km。 0.1に設定すると、中心から +/- 11km の範囲に分散します。
const COORD_RANDOM_RANGE = 0.1;

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
  // -range/2 から +range/2 の間のランダムなオフセットを生成
  const latOffset = (Math.random() - 0.5) * range;
  const lonOffset = (Math.random() - 0.5) * range;

  return {
    latitude: centerLat + latOffset,
    longitude: centerLon + lonOffset
  };
}

/**
 * APIへPOSTリクエストを送信する非同期関数
 */
async function createCommunity(index) {
  
  // 1. ランダムな座標を生成
  const { latitude, longitude } = getRandomCoordinates(
    NAGOYA_CENTER.lat,
    NAGOYA_CENTER.lon,
    COORD_RANDOM_RANGE
  );

  // 2. 送信するリクエストボディを作成
  const communityData = {
    // member_id: getRandomInt(1, 100), // 仮に作成者のIDを1-100でランダム生成
    name: `名古屋テストコミュニティ ${index}`,
    latitude: latitude,
    longitude: longitude,
    member_count: getRandomInt(5, 500), // メンバー数を5-500でランダム生成
    created_at: new Date().toISOString() // 現在時刻をISO 8601形式の文字列で
  };

  // 3. APIへPOSTリクエストを送信
  try {
    const response = await axios.post(API_URL, communityData);
    
    // 成功した場合
    console.log(`[成功 ${index}] ${communityData.name} (ID: ${response.data.community_id})`);
    
  } catch (error) {
    // 失敗した場合
    if (error.response) {
      // APIサーバーからのエラー (422 Validation Errorなど)
      console.error(`[失敗 ${index}] ${communityData.name} - Status: ${error.response.status}`);
      console.error('   -> Error Details:', error.response.data.detail || error.response.data);
    } else {
      // ネットワークエラーなど
      console.error(`[失敗 ${index}] ネットワークまたはリクエスト設定のエラー: ${error.message}`);
    }
  }
}

/**
 * メインの実行関数
 */
async function runCreationLoop() {
  console.log(`--- ${API_URL} に対して ${NUM_TO_CREATE} 件のコミュニティ生成を開始します ---`);

  const requests = [];

  for (let i = 1; i <= NUM_TO_CREATE; i++) {
    // リクエストを（ほぼ）同時に並列実行
    requests.push(createCommunity(i));

    // (オプション) サーバーに負荷をかけすぎないよう、少し待機する場合
    // await new Promise(resolve => setTimeout(resolve, 50)); // 50ms待機
  }

  // すべてのリクエストが完了するのを待つ
  await Promise.all(requests);

  console.log(`--- ${NUM_TO_CREATE} 件の処理が完了しました ---`);
}

// スクリプトを実行
runCreationLoop();