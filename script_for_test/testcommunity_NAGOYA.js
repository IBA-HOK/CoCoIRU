const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') }); // 親ディレクトリの.envを読み込み

// ## 1. ターゲットAPIのURL (ご自身の環境に合わせてください)
const API_BASE = process.env.API_BASE ?? 'http://127.0.0.1:8000';
const COMMUNITIES_URL = `${API_BASE}/api/v1/communities/`;

// ## 2. 生成するコミュニティの数
const NUM_TO_CREATE = Number(process.env.NUM_TO_CREATE ?? 50);

// ## 3. 名古屋市の中心座標 (おおよそ)
const NAGOYA_CENTER = {
  lat: 35.1814, // 緯度
  lon: 136.9063  // 経度
};

// ## 4. 中心からのバラつき具合 (度単位)
// 0.1度 = 約11km。 0.1に設定すると、中心から +/- 11km の範囲に分散します。
const COORD_RANDOM_RANGE = 0.5;

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
  // ランダムなパスワード生成（英数字8文字）
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let generatedPassword = '';
  for (let i = 0; i < 8; i++) {
    generatedPassword += chars.charAt(Math.floor(Math.random() * chars.length));
  }

  const communityData = {
    name: `名古屋テストコミュニティ ${index}`,
    latitude: latitude,
    longitude: longitude,
    member_count: getRandomInt(5, 500), // メンバー数を5-500でランダム生成
    created_at: new Date().toISOString(), // 現在時刻をISO 8601形式の文字列で
    password: generatedPassword
  };

  // 3. APIへPOSTリクエストを送信（認証不要）
  try {
    const response = await axios.post(COMMUNITIES_URL, communityData);
    
    // 成功した場合
    console.log(
      `[成功 ${index}] ${communityData.name} (ID: ${response.data.community_id}) | password: ${generatedPassword}`
    );
    
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
  console.log(`=== ${COMMUNITIES_URL} に対して ${NUM_TO_CREATE} 件のコミュニティ生成を開始します ===`);
  console.log('');

  const requests = [];

  for (let i = 1; i <= NUM_TO_CREATE; i++) {
    requests.push(createCommunity(i));
  }

  await Promise.all(requests);

  console.log('');
  console.log(`=== ${NUM_TO_CREATE} 件の処理が完了しました ===`);
}

// スクリプトを実行
runCreationLoop();