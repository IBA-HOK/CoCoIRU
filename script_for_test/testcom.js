const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') }); // 親ディレクトリの.envを読み込み

// ## 1. ターゲットAPIのURL (ご自身の環境に合わせてください)
const API_BASE = process.env.API_BASE ?? 'http://127.0.0.1:8000';
const TOKEN_URL = `${API_BASE}/api/v1/token`;
const COMMUNITIES_URL = `${API_BASE}/api/v1/communities/`;

// ## 2. 生成するコミュニティの数
const NUM_TO_CREATE = Number(process.env.NUM_TO_CREATE ?? 50);

// ## 3. 認証に利用する既存コミュニティの資格情報（オプション）
let AUTH_COMMUNITY_ID = process.env.SEED_COMMUNITY_ID;
let AUTH_PASSWORD = process.env.SEED_COMMUNITY_PASSWORD;

// ## 4. 名古屋市の中心座標 (おおよそ)
const NAGOYA_CENTER = {
  lat: 35.1814, // 緯度
  lon: 136.9063  // 経度
};

// ## 5. 中心からのバラつき具合 (度単位)
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
async function createCommunity(index, token) {
  if (!token) {
    throw new Error('APIトークンが取得できていません');
  }
  
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
    // member_id: getRandomInt(1, 100), // 仮に作成者のIDを1-100でランダム生成
    name: `名古屋テストコミュニティ ${index}`,
    latitude: latitude,
    longitude: longitude,
    member_count: getRandomInt(5, 500), // メンバー数を5-500でランダム生成
    created_at: new Date().toISOString(), // 現在時刻をISO 8601形式の文字列で
    password: generatedPassword
  };

  // 3. APIへPOSTリクエストを送信
  try {
    const response = await axios.post(COMMUNITIES_URL, communityData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
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
 * シードコミュニティを自動作成する関数
 */
async function createSeedCommunity() {
  console.log('シードコミュニティが未設定です。自動作成します...');
  
  const seedPassword = 'seed123';
  const seedData = {
    name: 'シードコミュニティ（自動生成）',
    password: seedPassword,
    latitude: 35.1814,
    longitude: 136.9063,
    member_count: 1,
    created_at: new Date().toISOString()
  };

  try {
    const response = await axios.post(COMMUNITIES_URL, seedData);
    AUTH_COMMUNITY_ID = response.data.community_id;
    AUTH_PASSWORD = seedPassword;
    console.log(`✓ シードコミュニティを作成しました (ID: ${AUTH_COMMUNITY_ID}, password: ${AUTH_PASSWORD})`);
    console.log('  ※ 次回以降は .env ファイルに以下を設定してください:');
    console.log(`  SEED_COMMUNITY_ID=${AUTH_COMMUNITY_ID}`);
    console.log(`  SEED_COMMUNITY_PASSWORD=${AUTH_PASSWORD}`);
    console.log('');
    return true;
  } catch (error) {
    console.error('✗ シードコミュニティの作成に失敗しました:', error.response?.data ?? error.message);
    return false;
  }
}

/**
 * メインの実行関数
 */
async function fetchToken() {
  // シードコミュニティが未設定の場合は自動作成
  if (!AUTH_COMMUNITY_ID || !AUTH_PASSWORD) {
    const created = await createSeedCommunity();
    if (!created) {
      throw new Error('シードコミュニティの作成に失敗しました');
    }
  }

  const payload = {
    community_id: Number(AUTH_COMMUNITY_ID),
    password: AUTH_PASSWORD
  };

  const response = await axios.post(TOKEN_URL, payload);
  return response.data.access_token;
}

async function runCreationLoop() {
  console.log(`=== ${COMMUNITIES_URL} に対して ${NUM_TO_CREATE} 件のコミュニティ生成を開始します ===`);
  console.log('');

  let token;
  try {
    token = await fetchToken();
    console.log('✓ 認証トークンを取得しました');
    console.log('');
  } catch (error) {
    console.error('✗ トークン取得に失敗しました:', error.response?.data ?? error.message);
    process.exit(1);
  }

  const requests = [];

  for (let i = 1; i <= NUM_TO_CREATE; i++) {
    requests.push(createCommunity(i, token));
  }

  await Promise.all(requests);

  console.log('');
  console.log(`=== ${NUM_TO_CREATE} 件の処理が完了しました ===`);
}

// スクリプトを実行
runCreationLoop();